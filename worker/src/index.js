// Well Run IT edge Worker (wellrunit.com/*)
// 1. Adds security headers to every page served from GitHub Pages.
// 2. Runs Bernie's back end under /api/bernie/: bot check, then the lead email to support@wellrunit.com.  The chat is form only, no AI.
// 3. The Bernie app (app.html): speech to text with Workers AI, the client checks the text, then one email.  Recordings are never kept or emailed.
// Emergencies go out as the same email, marked URGENT and high importance.  No text or push alerts (Nov 2026: email only).
// Nothing a visitor types is stored here.  A lead becomes one email, then it's gone.

const SITE = 'https://wellrunit.com';
const SESSION_MINUTES = 30;
const APP_FRESH = new Set(['/app.html', '/app', '/app-sw.js', '/app.webmanifest']);

const SECURITY_HEADERS = {
  'Strict-Transport-Security': 'max-age=15552000; includeSubDomains',   // matches the HSTS setting already on in Cloudflare
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()',
  'Cross-Origin-Opener-Policy': 'same-origin',
  'Content-Security-Policy': [
    "default-src 'self'",
    "script-src 'self' https://challenges.cloudflare.com",
    "frame-src https://challenges.cloudflare.com",
    "connect-src 'self' https://mefvxxoytleyfjbwtxix.supabase.co",   // anonymous visit counter
    "img-src 'self' data:",
    "style-src 'self' 'unsafe-inline'",
    "font-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
    'upgrade-insecure-requests',
  ].join('; '),
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname === 'www.wellrunit.com') return Response.redirect(SITE + url.pathname + url.search, 301);
    if (url.pathname.startsWith('/api/bernie/')) {
      try { return withHeaders(await api(request, env, url)); }
      catch (e) { console.log('bernie error', e && e.message); return withHeaders(json({ ok: false, error: 'server' }, 500)); }
    }
    // The Bernie app's page, service worker and manifest are never cached, so a phone always gets the latest version.
    if (APP_FRESH.has(url.pathname)) {
      const r = withHeaders(await fetch(request, { cache: 'no-store' }), url.pathname);
      r.headers.set('Cache-Control', 'no-cache');
      return r;
    }
    return withHeaders(await fetch(request), url.pathname);   // the page itself, from GitHub Pages
  },
};

function withHeaders(res, path = '') {
  const r = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) r.headers.set(k, v);
  // The Bernie app is the only page allowed to use the microphone.
  if (path === '/app.html' || path === '/app') r.headers.set('Permissions-Policy', SECURITY_HEADERS['Permissions-Policy'].replace('microphone=()', 'microphone=(self)'));
  r.headers.delete('x-github-request-id');
  return r;
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
}

async function api(request, env, url) {
  const route = url.pathname.slice('/api/bernie/'.length);
  const ip = request.headers.get('CF-Connecting-IP') || 'unknown';

  if (route === 'config' && request.method === 'GET') return json({ ok: true, sitekey: env.TURNSTILE_SITEKEY });
  if (request.method !== 'POST') return json({ ok: false, error: 'method' }, 405);
  if (request.headers.get('Origin') !== SITE) return json({ ok: false, error: 'origin' }, 403);
  if (route === 'transcribe') return transcribe(request, env, ip);   // the Bernie app (app.html)
  if (route === 'ticket') return ticket(request, env, ip);
  const body = await request.json().catch(() => null);
  if (!body) return json({ ok: false, error: 'bad request' }, 400);

  if (route === 'session') {
    if (!(await env.RL_SESSION.limit({ key: ip })).success) return json({ ok: false, error: 'slow down' }, 429);
    if (!(await turnstileOk(env, body.token, ip))) return json({ ok: false, error: 'bot check' }, 403);
    return json({ ok: true, session: await makeSession(env, ip) });
  }

  if (!(await sessionOk(env, body.session, ip))) return json({ ok: false, error: 'session' }, 401);

  if (route === 'submit') {
    if (!(await env.RL_SUBMIT.limit({ key: ip })).success) return json({ ok: false, error: 'slow down' }, 429);
    const lead = cleanLead(body.lead);
    if (!lead) return json({ ok: false, error: 'missing details' }, 400);
    const transcript = cleanTranscript(body.transcript);
    try { await sendLeadEmail(env, lead, transcript); }
    catch (e) { console.log('email failed', e && e.message); return json({ ok: false, error: 'send failed' }, 502); }
    return json({ ok: true });
  }
  return json({ ok: false, error: 'not found' }, 404);
}

// ---------- bot check and session ----------
async function turnstileOk(env, token, ip) {
  if (!token || typeof token !== 'string' || token.length > 2048) return false;
  const form = new FormData();
  form.append('secret', env.TURNSTILE_SECRET); form.append('response', token); form.append('remoteip', ip);
  const r = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', { method: 'POST', body: form });
  const d = await r.json().catch(() => ({}));
  return d.success === true && (!d.hostname || d.hostname === 'wellrunit.com');
}

const enc = new TextEncoder();
const b64u = (buf) => btoa(String.fromCharCode(...new Uint8Array(buf))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
async function hmac(env, text) {
  const key = await crypto.subtle.importKey('raw', enc.encode(env.SESSION_KEY), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return b64u(await crypto.subtle.sign('HMAC', key, enc.encode(text)));
}
async function makeSession(env, ip) {
  const payload = `${Date.now() + SESSION_MINUTES * 60000}.${(await hmac(env, 'ip:' + ip)).slice(0, 16)}`;
  return `${payload}.${await hmac(env, payload)}`;
}
async function sessionOk(env, session, ip) {
  if (typeof session !== 'string' || session.length > 200) return false;
  const [exp, iph, sig] = session.split('.');
  if (!exp || !iph || !sig || Number(exp) < Date.now()) return false;
  if (iph !== (await hmac(env, 'ip:' + ip)).slice(0, 16)) return false;
  return sig === (await hmac(env, `${exp}.${iph}`));
}

// ---------- lead ----------
const STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming','Outside the United States'];

function str(v, max) { return typeof v === 'string' ? v.replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max) : ''; }
function cleanLead(l) {
  if (!l || typeof l !== 'object') return null;
  const lead = {
    type: l.type === 'Existing customer' ? 'Existing customer' : 'New customer',
    name: str(l.name, 120), company: str(l.company, 160), email: str(l.email, 200), phone: str(l.phone, 40),
    state: STATES.includes(l.state) ? l.state : '', need: str(l.need, 3000), emergency: l.emergency === true,
    times: Array.isArray(l.times) ? l.times.slice(0, 3).map((t) => str(t, 120)).filter(Boolean) : [],
  };
  if (!lead.name || lead.phone.replace(/\D/g, '').length < 7) return null;
  if (lead.emergency) return lead;   // emergency: name and phone are all we ask for
  if (!lead.company || !lead.state || !lead.need) return null;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(lead.email)) return null;
  if (lead.times.length < 1) return null;   // one to three callback times
  return lead;
}
function cleanTranscript(t) {
  if (!Array.isArray(t)) return [];
  return t.slice(0, 60).map((m) => ({ who: m && m.who === 'bernie' ? 'Bernie' : 'Visitor', text: str(m && m.text, 1200) })).filter((m) => m.text);
}

function esc(s) { return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

async function graphToken(env) {
  const form = new URLSearchParams({ client_id: env.GRAPH_CLIENT_ID, client_secret: env.GRAPH_CLIENT_SECRET, scope: 'https://graph.microsoft.com/.default', grant_type: 'client_credentials' });
  const r = await fetch(`https://login.microsoftonline.com/${env.GRAPH_TENANT}/oauth2/v2.0/token`, { method: 'POST', body: form });
  const d = await r.json();
  if (!d.access_token) throw new Error('graph token: ' + (d.error || r.status));
  return d.access_token;
}

// The email always has the same subject format and the same rows in the same order.
async function sendLeadEmail(env, lead, transcript) {
  const subject = lead.emergency ? `URGENT | Call ${lead.name}, ${lead.phone} | Website emergency` : `${lead.company}, ${lead.state} | Website request`;
  const rows = lead.emergency ? [
    ['Emergency', 'YES, the visitor says something is down right now'],
    ['Name', lead.name],
    ['Phone', lead.phone],
  ] : [
    ['Emergency', lead.emergency ? 'YES, the visitor says something is down right now' : 'No'],
    ['Customer', lead.type],
    ['Company', lead.company],
    ['Name', lead.name],
    ['Email', lead.email],
    ['Phone', lead.phone],
    ['State', lead.state + (lead.state === 'California' ? '  (local)' : '  (remote)')],
    ['Callback times', lead.emergency ? 'Emergency, contact as soon as possible' : lead.times.map(esc).join('<br>')],
    ['What they need', lead.need],
  ];
  const table = rows.map(([k, v]) => `<tr><td style="padding:8px 14px 8px 0;color:#6b7787;vertical-align:top;white-space:nowrap">${k}</td><td style="padding:8px 0;color:#1b2430">${k === 'Callback times' ? v : esc(v).replace(/\n/g, '<br>')}</td></tr>`).join('');
  const chat = transcript.length ? transcript.map((m) => `<p style="margin:0 0 8px"><b>${m.who}:</b> ${esc(m.text)}</p>`).join('') : '<p style="margin:0">No chat, form only.</p>';
  const html = `<div style="font:15px/1.5 Segoe UI,Arial,sans-serif;max-width:680px">
<h2 style="margin:0 0 4px;font-size:20px;color:${lead.emergency ? '#b42318' : '#1b2430'}">${lead.emergency ? 'URGENT: ' : ''}New website request</h2>
<p style="margin:0 0 16px;color:#6b7787">Sent by Bernie on wellrunit.com.  ${lead.emergency ? "Emergency: call them now." : "Reply to this email to answer the customer directly."}</p>
<table style="border-collapse:collapse">${table}</table>
<h3 style="margin:22px 0 8px;font-size:16px;color:#1b2430">Full chat</h3>${chat}</div>`;
  const token = await graphToken(env);
  const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(env.SUPPORT_MAILBOX)}/sendMail`, {
    method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message: {
        subject, importance: lead.emergency ? 'high' : 'normal',
        body: { contentType: 'HTML', content: html },
        toRecipients: [{ emailAddress: { address: env.SUPPORT_MAILBOX } }],
        ...(lead.email ? { replyTo: [{ emailAddress: { address: lead.email, name: lead.name } }] } : {}),   // emergencies have no email
      },
      saveToSentItems: false,
    }),
  });
  if (r.status !== 202) throw new Error('sendMail ' + r.status + ' ' + (await r.text()).slice(0, 300));
}

// ---------- the Bernie app ----------
// 1. /transcribe: the client's recording comes here once, is written out with Workers AI, and the text goes back
//    to the app.  The recording is not kept or emailed.
// 2. /ticket: the client checks and edits that text, taps Submit, and it goes to the support mailbox as one email.
const MAX_AUDIO = 4_000_000;   // the app stops recording at 2 minutes, well under this
const AUDIO_TYPES = ['audio/mp4', 'audio/x-m4a', 'audio/aac', 'audio/webm', 'audio/ogg', 'audio/mpeg', 'audio/wav'];

async function transcribe(request, env, ip) {
  if (!(await env.RL_SESSION.limit({ key: ip })).success) return json({ ok: false, error: 'slow down' }, 429);
  const form = await request.formData().catch(() => null);
  if (!form) return json({ ok: false, error: 'bad request' }, 400);
  if (!(await turnstileOk(env, form.get('token'), ip))) return json({ ok: false, error: 'bot check' }, 403);
  const file = form.get('audio');
  if (!file || typeof file !== 'object' || !file.size) return json({ ok: false, error: 'no recording' }, 400);
  const type = String(file.type || '').split(';')[0].trim().toLowerCase();
  if (file.size > MAX_AUDIO || !AUDIO_TYPES.includes(type)) return json({ ok: false, error: 'recording too long' }, 413);
  if (!env.AI) return json({ ok: true, text: '' });
  try {
    const r = await env.AI.run('@cf/openai/whisper-large-v3-turbo', { audio: toBase64(new Uint8Array(await file.arrayBuffer())), language: 'en' });
    return json({ ok: true, text: str(r && r.text, 5000) });
  } catch (e) { console.log('transcribe failed', e && e.message); return json({ ok: true, text: '' }); }   // the app asks them to type it
}

async function ticket(request, env, ip) {
  if (!(await env.RL_SUBMIT.limit({ key: ip })).success) return json({ ok: false, error: 'slow down' }, 429);
  const form = await request.formData().catch(() => null);
  if (!form) return json({ ok: false, error: 'bad request' }, 400);
  if (!(await turnstileOk(env, form.get('token'), ip))) return json({ ok: false, error: 'bot check' }, 403);
  const who = { name: str(form.get('name'), 120), company: str(form.get('company'), 160), phone: str(form.get('phone'), 40), email: str(form.get('email'), 200) };
  if (!who.name || !who.company || who.phone.replace(/\D/g, '').length < 7) return json({ ok: false, error: 'missing details' }, 400);
  if (who.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(who.email)) who.email = '';
  const text = typeof form.get('text') === 'string' ? form.get('text').replace(/[\u0000-\u0008\u000b-\u001f\u007f]/g, ' ').trim().slice(0, 5000) : '';
  if (text.length < 3) return json({ ok: false, error: 'nothing to send' }, 400);
  const how = form.get('how') === 'voice' ? 'Bernie app, spoken and checked by the customer' : 'Bernie app, typed';
  try { await sendTicketEmail(env, who, text, how); }
  catch (e) { console.log('ticket email failed', e && e.message); return json({ ok: false, error: 'send failed' }, 502); }
  return json({ ok: true });
}

function toBase64(bytes) {
  let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

async function sendTicketEmail(env, who, text, how) {
  const first = text.replace(/\s+/g, ' ').slice(0, 60) + (text.length > 60 ? '...' : '');
  const subject = `${who.company} | ${who.name} | App ticket: ${first}`;
  const rows = [['Company', who.company], ['Name', who.name], ['Phone', who.phone], ['Email', who.email || 'Not given'], ['Sent from', how]]
    .map(([k, v]) => `<tr><td style="padding:8px 14px 8px 0;color:#6b7787;vertical-align:top;white-space:nowrap">${k}</td><td style="padding:8px 0;color:#1b2430">${esc(v)}</td></tr>`).join('');
  const html = `<div style="font:15px/1.5 Segoe UI,Arial,sans-serif;max-width:680px">
<h2 style="margin:0 0 4px;font-size:20px;color:#1b2430">New ticket from the Bernie app</h2>
<p style="margin:0 0 16px;color:#6b7787">${who.email ? 'Reply to this email to answer the customer directly.' : 'No email given.  Call the customer back.'}</p>
<table style="border-collapse:collapse">${rows}</table>
<h3 style="margin:22px 0 8px;font-size:16px;color:#1b2430">What they need</h3><p style="margin:0;white-space:pre-wrap">${esc(text)}</p></div>`;
  const token = await graphToken(env);
  const r = await fetch(`https://graph.microsoft.com/v1.0/users/${encodeURIComponent(env.SUPPORT_MAILBOX)}/sendMail`, {
    method: 'POST', headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: {
      subject, importance: 'normal', body: { contentType: 'HTML', content: html },
      toRecipients: [{ emailAddress: { address: env.SUPPORT_MAILBOX } }],
      ...(who.email ? { replyTo: [{ emailAddress: { address: who.email, name: who.name } }] } : {}),
    }, saveToSentItems: false }),
  });
  if (r.status !== 202) throw new Error('sendMail ' + r.status + ' ' + (await r.text()).slice(0, 300));
}
