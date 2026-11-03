// Well Run IT edge Worker (wellrunit.com/*)
// 1. Adds security headers to every page served from GitHub Pages.
// 2. Runs Bernie's back end under /api/bernie/: bot check, then the lead email to support@wellrunit.com.  Form only, no AI.
// Nothing a visitor types is stored here.  A lead becomes one email (and, for an emergency, one phone alert), then it's gone.

const SITE = 'https://wellrunit.com';
const SESSION_MINUTES = 30;

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
    return withHeaders(await fetch(request));   // the page itself, from GitHub Pages
  },
};

function withHeaders(res) {
  const r = new Response(res.body, res);
  for (const [k, v] of Object.entries(SECURITY_HEADERS)) r.headers.set(k, v);
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
    // Emergency: the phone alert goes first and doesn't wait on email.  If either one gets through, the visitor is told it worked.
    if (lead.emergency) {
      const [alert, mail] = await Promise.allSettled([alertPhones(env, lead), sendLeadEmail(env, lead, transcript)]);
      if (alert.status === 'rejected') console.log('pushover failed', alert.reason && alert.reason.message);
      if (mail.status === 'rejected') console.log('email failed', mail.reason && mail.reason.message);
      if (alert.status === 'rejected' && mail.status === 'rejected') return json({ ok: false, error: 'send failed' }, 502);
      return json({ ok: true });
    }
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

// Emergency alert to Eric's phone through Pushover (limits are per account, not per IP, so Cloudflare's shared IPs don't matter).
// Priority 2 repeats every 60 seconds for up to 30 minutes until it's acknowledged in the app.
async function alertPhones(env, lead) {
  const form = new URLSearchParams({
    token: env.PUSHOVER_TOKEN, user: env.PUSHOVER_USER,
    title: `URGENT: call ${lead.name} at ${lead.phone}`.slice(0, 250),
    message: `Emergency through Bernie on wellrunit.com.  Call ${lead.name} at ${lead.phone}.  A copy is in the support mailbox.`,
    priority: '2', retry: '60', expire: '1800',
  });
  const r = await fetch('https://api.pushover.net/1/messages.json', { method: 'POST', body: form });
  if (!r.ok) throw new Error('pushover ' + r.status + ' ' + (await r.text()).slice(0, 200));
}
