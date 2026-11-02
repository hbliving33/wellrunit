// Bernie: fills out the contact form for the visitor through a short chat, then hands them to a real person.
// Never asks for the same thing twice.  Never prices, troubleshoots or solves.  "Talk to a person" is always one click away.
// Nothing is stored in the browser or on the server: a finished chat becomes one email to support@wellrunit.com.
(() => {
  const API = '/api/bernie/';
  const SUPPORT = 'support@wellrunit.com';
  const MAX_Q = 3;
  const STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming','Outside the United States'];
  // Main time zone for each state, used only to show callback times in the visitor's local time.
  const EAST = 'America/New_York', CENT = 'America/Chicago', MTN = 'America/Denver', PAC = 'America/Los_Angeles';
  const ZONE = { Alabama: CENT, Alaska: 'America/Anchorage', Arizona: 'America/Phoenix', Arkansas: CENT, California: PAC, Colorado: MTN, Connecticut: EAST, Delaware: EAST,
    'District of Columbia': EAST, Florida: EAST, Georgia: EAST, Hawaii: 'Pacific/Honolulu', Idaho: MTN, Illinois: CENT, Indiana: EAST, Iowa: CENT, Kansas: CENT, Kentucky: EAST,
    Louisiana: CENT, Maine: EAST, Maryland: EAST, Massachusetts: EAST, Michigan: EAST, Minnesota: CENT, Mississippi: CENT, Missouri: CENT, Montana: MTN, Nebraska: CENT,
    Nevada: PAC, 'New Hampshire': EAST, 'New Jersey': EAST, 'New Mexico': MTN, 'New York': EAST, 'North Carolina': EAST, 'North Dakota': CENT, Ohio: EAST, Oklahoma: CENT,
    Oregon: PAC, Pennsylvania: EAST, 'Rhode Island': EAST, 'South Carolina': EAST, 'South Dakota': CENT, Tennessee: CENT, Texas: CENT, Utah: MTN, Vermont: EAST, Virginia: EAST,
    Washington: PAC, 'West Virginia': EAST, Wisconsin: CENT, Wyoming: MTN };

  let ui, log, foot, session = null, sitekey = null, ready = null, opened = false;
  const lead = { need: '', type: '', name: '', company: '', email: '', phone: '', state: '', times: [], emergency: false };
  const transcript = [];   // goes into the email, then it's gone
  const history = [];      // quick-question chat for the AI
  let qCount = 0;

  // ---------- small helpers ----------
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const scroll = () => { log.scrollTop = log.scrollHeight; };
  function say(text, who = 'bernie') {
    const m = el('div', 'bm ' + who, text); log.appendChild(m); scroll();
    transcript.push({ who: who === 'bernie' ? 'bernie' : 'visitor', text });
    return m;
  }
  function typing() { const t = el('div', 'bm bernie typing'); t.innerHTML = '<i></i><i></i><i></i>'; log.appendChild(t); scroll(); return t; }
  function setFoot(...nodes) { foot.replaceChildren(...nodes); }
  function btn(label, onClick, cls = '') { const b = el('button', 'bb ' + cls, label); b.type = 'button'; b.addEventListener('click', onClick); return b; }
  function choices(list) { const w = el('div', 'bchoices'); list.forEach(([label, fn, cls]) => w.appendChild(btn(label, fn, cls))); return w; }
  function personBtn() { return btn('Talk to a person', () => { say('Talk to a person', 'visitor'); startForm(); }, 'ghost'); }

  // A typed answer with simple checks; never re-asks once an answer is accepted.
  function ask(question, { type = 'text', placeholder = '', check, done, area = false }) {
    say(question);
    const f = el('form', 'binput');
    const inp = area ? el('textarea') : el('input');
    if (!area) inp.type = type;
    inp.placeholder = placeholder; inp.maxLength = area ? 3000 : 200; inp.setAttribute('aria-label', question);
    const send = btn('Send', () => f.requestSubmit(), 'send'); send.type = 'submit';
    const err = el('div', 'berr'); err.hidden = true;
    f.append(inp, send);
    f.addEventListener('submit', (e) => {
      e.preventDefault();
      const v = inp.value.trim();
      const problem = !v ? 'This one is needed.' : check ? check(v) : '';
      if (problem) { err.textContent = problem; err.hidden = false; inp.focus(); return; }
      say(v, 'visitor'); done(v);
    });
    if (area) inp.addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); f.requestSubmit(); } });
    setFoot(f, err, personBtnIfAsking());
    setTimeout(() => inp.focus(), 50);
  }
  let inForm = false;
  const personBtnIfAsking = () => (inForm ? el('span') : personBtn());

  // ---------- open / close ----------
  function build() {
    ui = el('div', 'bpanel'); ui.setAttribute('role', 'dialog'); ui.setAttribute('aria-label', 'Bernie'); ui.hidden = true;
    ui.innerHTML = `<div class="bhead"><div><b>Bernie</b><span>Fills out the form for you, then hands you to a real person.</span></div><button type="button" class="bx" aria-label="Close">Close</button></div>
<p class="bwink">Not a fan of chatbots?  Neither are we.  No endless loops, no "I didn't quite get that."  Bernie just fills out the form for you.</p>
<div class="blog" aria-live="polite"></div><div class="bfoot"></div><div class="bturn"></div>`;
    document.body.appendChild(ui);
    log = ui.querySelector('.blog'); foot = ui.querySelector('.bfoot');
    ui.querySelector('.bx').addEventListener('click', close);
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !ui.hidden) close(); });
  }
  function close() { ui.hidden = true; launcher.setAttribute('aria-expanded', 'false'); launcher.hidden = false; }

  function open(prefill) {
    if (!ui) build();
    ui.hidden = false; launcher.hidden = true; launcher.setAttribute('aria-expanded', 'true');
    if (prefill && !lead.need) lead.need = prefill;
    if (opened) return;
    opened = true;
    ready = connect();
    ready.then((ok) => { if (!ok && !transcript.some((m) => m.who === 'visitor')) { log.replaceChildren(); transcript.length = 0; offline(); } });
    say("Hi, I'm Bernie.  What would you like to do?");
    setFoot(choices([
      ['Talk to a person', () => { say('Talk to a person', 'visitor'); startForm(); }],
      ['Ask a quick question', () => { say('Ask a quick question', 'visitor'); question(); }, 'ghost'],
      ["Something's down right now", () => { say("Something's down right now", 'visitor'); lead.emergency = true; startForm(); }, 'warn'],
    ]));
  }

  // ---------- bot check and session (Cloudflare Turnstile) ----------
  async function connect() {
    try {
      const c = await fetch(API + 'config', { cache: 'no-store' });
      if (!c.ok) throw new Error('offline');
      sitekey = (await c.json()).sitekey;
      await new Promise((res, rej) => {
        if (window.turnstile) return res();
        const s = document.createElement('script');
        s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'; s.async = true; s.onload = res; s.onerror = rej;
        document.head.appendChild(s);
      });
      const token = await new Promise((res, rej) => {
        window.turnstile.render(ui.querySelector('.bturn'), { sitekey, appearance: 'interaction-only', callback: res, 'error-callback': () => rej(new Error('turnstile')) });
      });
      const r = await fetch(API + 'session', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ token }) });
      const d = await r.json();
      if (!d.ok) throw new Error('session');
      session = d.session;
      return true;
    } catch (e) { return false; }
  }
  function offline() {
    say(`Sorry, I can't send messages right now.  Please email ${SUPPORT} and a real person will reply.`);
    const a = el('a', 'bb', 'Email ' + SUPPORT); a.href = 'mailto:' + SUPPORT; setFoot(a);
  }

  // ---------- quick questions (up to three) ----------
  function question() {
    ask(qCount ? 'What else would you like to know?' : 'Sure.  What would you like to know?', { area: true, placeholder: 'Type your question', done: async (q) => {
      qCount++; history.push({ role: 'user', content: q });
      if (!lead.need) lead.need = q; else lead.need += '\n' + q;
      setFoot(el('span'));
      const t = typing();
      let reply = '';
      if (await ready) {
        try {
          const r = await fetch(API + 'ask', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ session, history }) });
          const d = await r.json(); if (d.ok) reply = d.reply;
        } catch (e) {}
      }
      t.remove();
      if (!reply) reply = "That's a good one for our team.  Want me to pass it along?";
      history.push({ role: 'assistant', content: reply }); say(reply);
      const list = [['Pass this to our team', () => { say('Pass this to our team', 'visitor'); startForm(); }]];
      if (qCount < MAX_Q) list.push(['Ask something else', () => { say('Ask something else', 'visitor'); question(); }, 'ghost']);
      setFoot(choices(list));
    } });
  }

  // ---------- the form, one question at a time ----------
  const steps = [];
  function startForm() {
    inForm = true;
    steps.length = 0;
    if (!lead.need) steps.push(stepNeed);
    steps.push(stepType, stepName, stepCompany, stepEmail, stepPhone, stepState);
    if (!lead.emergency) steps.push(stepTimes);
    steps.push(review);
    if (lead.emergency) say('Got it.  A few quick details and I\'ll alert our team right away.');
    else say('Happy to.  A few quick questions and a real person will take it from there.');
    next();
  }
  const next = () => { const s = steps.shift(); if (s) s(); };

  function stepNeed() { ask(lead.emergency ? "What's down?" : 'What can we help with?', { area: true, placeholder: 'A sentence or two is plenty', done: (v) => { lead.need = v; next(); } }); }
  function stepType() {
    say('Are you a new or existing customer?');
    setFoot(choices([['New customer', () => { lead.type = 'New customer'; say('New customer', 'visitor'); next(); }], ['Existing customer', () => { lead.type = 'Existing customer'; say('Existing customer', 'visitor'); next(); }, 'ghost']]));
  }
  function stepName() { ask("What's your name?", { placeholder: 'First and last name', done: (v) => { lead.name = v; next(); } }); }
  function stepCompany() { ask('And your company?', { placeholder: 'Company name', done: (v) => { lead.company = v; next(); } }); }
  function stepEmail() { ask('Best email to reach you?', { type: 'email', placeholder: 'name@company.com', check: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : "That email doesn't look right."), done: (v) => { lead.email = v; next(); } }); }
  function stepPhone() { ask('Best phone number?', { type: 'tel', placeholder: 'Phone number', check: (v) => (v.replace(/\D/g, '').length >= 7 ? '' : "That number doesn't look right."), done: (v) => { lead.phone = v; next(); } }); }
  function stepState() {
    say('Which state are you in?');
    const f = el('form', 'binput');
    const sel = el('select'); sel.setAttribute('aria-label', 'State');
    sel.appendChild(new Option('Choose your state', ''));
    STATES.forEach((s) => sel.appendChild(new Option(s, s)));
    const send = btn('Send', () => {}, 'send'); send.type = 'submit';
    f.append(sel, send);
    f.addEventListener('submit', (e) => { e.preventDefault(); if (!sel.value) return; lead.state = sel.value; say(sel.value, 'visitor'); next(); });
    setFoot(f); setTimeout(() => sel.focus(), 50);
  }

  // Callback times: weekdays, 7 a.m. to 4 p.m. Pacific, shown in the visitor's local time.
  function ptInstant(y, m, d, h, min) {   // the moment it is h:min on y-m-d in Los Angeles
    let t = Date.UTC(y, m - 1, d, h + 8, min);
    for (let i = 0; i < 2; i++) {
      const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: PAC, hourCycle: 'h23', year: 'numeric', month: 'numeric', day: 'numeric', hour: 'numeric', minute: 'numeric' }).formatToParts(new Date(t)).map((x) => [x.type, x.value]));
      const shown = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute);
      t += Date.UTC(y, m - 1, d, h, min) - shown;
    }
    return new Date(t);
  }
  function stepTimes() {
    const zone = ZONE[lead.state] || PAC;
    const local = (dt, opts) => new Intl.DateTimeFormat('en-US', { timeZone: zone, ...opts }).format(dt);
    const pt = (dt, opts) => new Intl.DateTimeFormat('en-US', { timeZone: PAC, ...opts }).format(dt);
    // next 10 weekdays in Pacific time, starting tomorrow
    const days = []; const now = new Date();
    for (let i = 1; days.length < 10 && i < 20; i++) {
      const p = Object.fromEntries(new Intl.DateTimeFormat('en-US', { timeZone: PAC, year: 'numeric', month: 'numeric', day: 'numeric', weekday: 'short' }).formatToParts(new Date(now.getTime() + i * 864e5)).map((x) => [x.type, x.value]));
      if (p.weekday !== 'Sat' && p.weekday !== 'Sun') days.push([+p.year, +p.month, +p.day]);
    }
    const slots = []; for (let h = 7; h < 16; h++) for (const mm of [0, 30]) slots.push([h, mm]);
    const zoneName = local(new Date(), { timeZoneName: 'short' }).split(' ').pop();
    say(`Pick three times that work for a callback.  Times are shown in your time zone (${zoneName}).`);
    const f = el('form', 'btimes');
    const rows = [0, 1, 2].map((i) => {
      const r = el('div', 'btrow');
      const ds = el('select'); ds.setAttribute('aria-label', `Choice ${i + 1} day`);
      ds.appendChild(new Option(`Choice ${i + 1}: day`, ''));
      days.forEach(([y, m, d], k) => ds.appendChild(new Option(local(ptInstant(y, m, d, 12, 0), { weekday: 'short', month: 'short', day: 'numeric' }), k)));
      const ts = el('select'); ts.setAttribute('aria-label', `Choice ${i + 1} time`);
      const label = () => {   // label the times for the chosen day, so daylight saving differences come out right
        const day = days[ds.value === '' ? 0 : +ds.value], keep = ts.value;
        ts.replaceChildren(new Option('Time', ''));
        slots.forEach(([h, mm], k) => ts.appendChild(new Option(local(ptInstant(...day, h, mm), { hour: 'numeric', minute: '2-digit' }), k)));
        ts.value = keep;
      };
      label(); ds.addEventListener('change', label);
      r.append(ds, ts); f.appendChild(r); return [ds, ts];
    });
    const err = el('div', 'berr'); err.hidden = true;
    const send = btn('Send these times', () => {}, 'send wide'); send.type = 'submit';
    f.append(err, send);
    f.addEventListener('submit', (e) => {
      e.preventDefault();
      const picked = rows.map(([ds, ts]) => (ds.value === '' || ts.value === '' ? null : ptInstant(...days[+ds.value], ...slots[+ts.value])));
      if (picked.includes(null)) { err.textContent = 'Please pick a day and time for all three.'; err.hidden = false; return; }
      if (new Set(picked.map((d) => d.getTime())).size < 3) { err.textContent = 'Please pick three different times.'; err.hidden = false; return; }
      picked.sort((a, b) => a - b);
      const fmt = (dt) => `${local(dt, { weekday: 'short', month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit', timeZoneName: 'short' })}` + (zone === PAC ? '' : `  (${pt(dt, { hour: 'numeric', minute: '2-digit', timeZoneName: 'short' })})`);
      lead.times = picked.map(fmt);
      say(lead.times.join('\n'), 'visitor');
      next();
    });
    setFoot(f);
  }

  // Review: everything at once, change any one thing without starting over.
  function review() {
    const fields = [['need', 'What you need'], ['type', 'Customer'], ['name', 'Name'], ['company', 'Company'], ['email', 'Email'], ['phone', 'Phone'], ['state', 'State']];
    if (!lead.emergency) fields.push(['times', 'Callback times']);
    say("Here's what I'll send.  Tap anything to change it.");
    const box = el('div', 'breview');
    fields.forEach(([k, label]) => {
      const row = el('button', 'brow'); row.type = 'button';
      row.append(el('span', '', label), el('b', '', Array.isArray(lead[k]) ? lead[k].join('\n') : lead[k]));
      row.addEventListener('click', () => {
        const map = { need: stepNeed, type: stepType, name: stepName, company: stepCompany, email: stepEmail, phone: stepPhone, state: stepState, times: stepTimes };
        steps.length = 0; steps.push(review);
        if (k === 'state' && !lead.emergency) steps.unshift(stepTimes);   // local times depend on the state
        map[k]();
      });
      box.appendChild(row);
    });
    log.appendChild(box); scroll();
    const p = el('p', 'bnote'); p.innerHTML = 'We only use this to reply to you.  <a href="privacy.html">Privacy</a>';
    setFoot(btn(lead.emergency ? 'Send and alert the team' : 'Send it', submit, 'send wide' + (lead.emergency ? ' warn' : '')), p);
  }

  async function submit() {
    setFoot(el('span'));
    const t = typing();
    let ok = false;
    if (await ready) {
      try {
        const r = await fetch(API + 'submit', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ session, lead, transcript }) });
        ok = (await r.json()).ok === true;
      } catch (e) {}
    }
    t.remove();
    if (!ok) return offline();
    if (lead.emergency) say("Thanks, I've flagged this as an emergency and sent an alert to our team right away.  We'll be in touch as fast as we can.");
    else say("All set.  A real person has everything and will reach out to confirm one of your times.  You won't have to repeat any of this.");
    setFoot(btn('Close', close, 'ghost'));
    inForm = false;
  }

  // ---------- launcher, and every "Contact us" link opens Bernie ----------
  const launcher = el('button', 'blaunch', 'Ask Bernie');
  launcher.type = 'button'; launcher.setAttribute('aria-expanded', 'false');
  launcher.addEventListener('click', () => open());
  document.body.appendChild(launcher);

  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href^="contact.html"], [data-bernie]');
    if (!a) return;
    e.preventDefault();
    let prefill = '';
    try {
      const u = new URL(a.getAttribute('href') || '', location.href);
      const topic = u.searchParams.get('topic'), msg = u.searchParams.get('msg');
      prefill = [topic && `Interested in: ${topic}`, msg].filter(Boolean).join('\n');
    } catch (err) {}
    open(prefill);
  });
  if (/contact\.html$/.test(location.pathname)) {
    const q = new URLSearchParams(location.search);
    open([q.get('topic') && `Interested in: ${q.get('topic')}`, q.get('msg')].filter(Boolean).join('\n'));
  }
})();
