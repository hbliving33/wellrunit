// Bernie app (app.html): tap, talk, tap again.  Bernie writes it out, the client checks and fixes the text,
// then taps Submit.  It becomes one email to support@wellrunit.com, text only.
// The recording goes to the server once to be written out, and is not kept or emailed.
// The client's name, company and phone are saved only on their own device, so they type them once.
(() => {
  const API = '/api/bernie/';
  const SUPPORT = 'support@wellrunit.com';
  const MAX_SECONDS = 120;
  const KEY = 'bernie-app-contact';
  const $ = (id) => document.getElementById(id);
  const screens = ['setup', 'home', 'working', 'review', 'done', 'failed'];
  let who = null;
  try { who = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { who = null; }
  const ready = () => !!(who && who.name && who.company && who.phone);
  function show(name) {
    screens.forEach((s) => { $(s).hidden = s !== name; });
    document.querySelector('.foot').hidden = name !== 'home' || !ready();
    const h = $(name).querySelector('h1');
    if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
  }
  function working(title, text) { $('workTitle').textContent = title; $('workText').textContent = text; show('working'); }

  // ---------- who is sending (kept on this device only) ----------
  function showWho() { $('who').textContent = ready() ? who.name : ''; }
  $('setupForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const v = (id) => $(id).value.trim();
    const next = { name: v('s-name'), company: v('s-company'), phone: v('s-phone'), email: v('s-email') };
    let problem = '';
    if (!next.name || !next.company) problem = 'Please fill in your name and company.';
    else if (next.phone.replace(/\D/g, '').length < 7) problem = "That phone number doesn't look right.";
    else if (next.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(next.email)) problem = "That email doesn't look right.";
    if (problem) { $('setupErr').textContent = problem; $('setupErr').hidden = false; return; }
    who = next;
    try { localStorage.setItem(KEY, JSON.stringify(who)); } catch (err) {}
    showWho(); show('home');
  });
  function editWho() {
    ['name', 'company', 'phone', 'email'].forEach((k) => { $('s-' + k).value = (who && who[k]) || ''; });
    $('setupErr').hidden = true; show('setup');
  }
  $('changeWho').addEventListener('click', editWho);

  // ---------- recording ----------
  let rec = null, stream = null, chunks = [], started = 0, tick = null;
  const pickType = () => {
    if (!window.MediaRecorder || !MediaRecorder.isTypeSupported) return '';
    return ['audio/mp4', 'audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus'].find((t) => MediaRecorder.isTypeSupported(t)) || '';
  };
  const fmt = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;
  function release() {   // always let go of the microphone (iPhone home-screen apps need this to record again)
    if (stream) stream.getTracks().forEach((t) => t.stop());
    stream = null; rec = null; clearInterval(tick);
  }
  async function start() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) return micProblem("This browser can't record.  You can type it instead.");
    try { stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); }
    catch (e) { return micProblem('Bernie needs the microphone.  Allow it in your settings, or type it instead.'); }
    const type = pickType();
    try { rec = new MediaRecorder(stream, type ? { mimeType: type, audioBitsPerSecond: 32000 } : { audioBitsPerSecond: 32000 }); }
    catch (e) { release(); return micProblem("Recording didn't start.  You can type it instead."); }
    chunks = [];
    rec.ondataavailable = (e) => { if (e.data && e.data.size) chunks.push(e.data); };
    rec.onstop = () => {
      const blob = new Blob(chunks, { type: (rec && rec.mimeType) || type || 'audio/mp4' });
      release(); setTalk(false);
      if (!blob.size) return micProblem('Nothing was recorded.  Try again, or type it instead.');
      writeOut(blob);
    };
    rec.start(1000);
    started = Date.now(); setTalk(true);
    tick = setInterval(() => {
      const s = Math.round((Date.now() - started) / 1000);
      $('timer').textContent = fmt(s);
      if (s >= MAX_SECONDS) stop();
    }, 250);
  }
  function stop() { if (rec && rec.state !== 'inactive') rec.stop(); else release(); }
  function setTalk(on) {
    const b = $('talk');
    b.classList.toggle('rec', on);
    b.setAttribute('aria-pressed', on ? 'true' : 'false');
    $('talkLabel').textContent = on ? 'Tap to stop' : 'Tap to talk';
    $('talkSub').hidden = !on;
    $('timer').textContent = '0:00';
    $('homeHint').textContent = on ? `Talking.  Tap again when you're done (up to ${MAX_SECONDS / 60} minutes).` : "Tap again when you're done.  You'll see what Bernie heard before it's sent.";
  }
  function micProblem(msg) { release(); setTalk(false); $('homeErr').textContent = msg; $('homeErr').hidden = false; }
  $('talk').addEventListener('click', () => { $('homeErr').hidden = true; if (rec) stop(); else start(); });
  document.addEventListener('visibilitychange', () => { if (document.hidden && rec) stop(); });

  // ---------- review: check and fix the text, then submit ----------
  let how = 'typed';
  function review(text, note, source) {
    how = source;
    $('r-text').value = text;
    $('reviewNote').textContent = note;
    $('reviewErr').hidden = true;
    show('review');
    if (!text) setTimeout(() => $('r-text').focus(), 50);
  }
  async function writeOut(blob) {
    working('Writing it out.', 'One moment.');
    let text = '';
    try {
      const f = new FormData();
      f.append('token', await botToken());
      f.append('audio', blob, 'recording.' + (blob.type.includes('webm') ? 'webm' : blob.type.includes('ogg') ? 'ogg' : 'm4a'));
      const d = await (await fetch(API + 'transcribe', { method: 'POST', body: f })).json();
      if (d.ok) text = (d.text || '').trim();
    } catch (e) { text = ''; }
    if (text) review(text, "Here's what Bernie heard.  Fix anything that's off, then tap Submit.", 'voice');
    else review('', "Bernie couldn't make that out.  Type it here, or start over and try again.", 'typed');
  }
  $('typeIt').addEventListener('click', () => review('', 'Tell us in a sentence or two, then tap Submit.', 'typed'));
  $('redo').addEventListener('click', () => show('home'));
  $('reviewForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const text = $('r-text').value.trim();
    if (text.length < 3) { $('reviewErr').textContent = "Tell us a little about what's going on."; $('reviewErr').hidden = false; return; }
    send(text);
  });

  // ---------- bot check (Cloudflare Turnstile), a fresh token for each call ----------
  let sitekey = null, widget = null, pending = null;
  async function botToken() {
    if (!sitekey) {
      const c = await fetch(API + 'config', { cache: 'no-store' });
      if (!c.ok) throw new Error('offline');
      sitekey = (await c.json()).sitekey;
    }
    if (!window.turnstile) {
      await new Promise((res, rej) => {
        const s = document.createElement('script');
        s.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'; s.async = true; s.onload = res; s.onerror = rej;
        document.head.appendChild(s);
      });
    }
    return new Promise((res, rej) => {
      pending = { res, rej };
      if (widget === null) {
        widget = window.turnstile.render('#botcheck', {
          sitekey, appearance: 'interaction-only', execution: 'execute',
          callback: (t) => { if (pending) pending.res(t); pending = null; },
          'error-callback': () => { if (pending) pending.rej(new Error('turnstile')); pending = null; },
        });
      } else window.turnstile.reset(widget);
      window.turnstile.execute(widget);
    });
  }

  // ---------- send ----------
  let lastText = '';
  async function send(text) {
    lastText = text;
    working('Sending.', 'One moment.');
    let ok = false;
    try {
      const f = new FormData();
      f.append('token', await botToken());
      ['name', 'company', 'phone', 'email'].forEach((k) => f.append(k, (who && who[k]) || ''));
      f.append('text', text); f.append('how', how);
      ok = (await (await fetch(API + 'ticket', { method: 'POST', body: f })).json().catch(() => ({}))).ok === true;
    } catch (e) { ok = false; }
    if (ok) { $('r-text').value = ''; lastText = ''; show('done'); }
    else show('failed');
  }
  $('retry').addEventListener('click', () => { if (lastText) send(lastText); else show('home'); });
  $('failedBack').addEventListener('click', () => review(lastText, "Fix anything that's off, then tap Submit.", how));
  $('again').addEventListener('click', () => show('home'));
  $('mailLink').href = 'mailto:' + SUPPORT;

  // ---------- putting it on the home screen or desktop ----------
  const standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const ua = navigator.userAgent;
  const iOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  const macSafari = !iOS && /Macintosh/.test(ua) && /Safari/.test(ua) && !/Chrome|Chromium|Edg|Firefox/.test(ua);
  let deferred = null;
  function installTip(text, withButton) { $('installText').textContent = text; $('installBtn').hidden = !withButton; $('install').hidden = false; }
  if (!standalone) {
    if (iOS) installTip('Put Bernie on your home screen: tap the Share button (on newer iPhones, tap the three dots first), then Add to Home Screen.', false);
    else if (macSafari) installTip('Put Bernie in your Dock: in Safari, choose File, then Add to Dock.', false);
    else installTip("Put Bernie on your desktop or home screen: use Install in your browser's address bar or menu.", false);
  }
  window.addEventListener('beforeinstallprompt', (e) => { e.preventDefault(); deferred = e; installTip("Put Bernie on your home screen or desktop, so it's one tap away.", true); });
  $('installBtn').addEventListener('click', async () => {
    if (!deferred) return;
    deferred.prompt(); await deferred.userChoice.catch(() => null);
    deferred = null; $('install').hidden = true;
  });
  window.addEventListener('appinstalled', () => { $('install').hidden = true; });
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/app-sw.js', { scope: '/app' }).catch(() => {});

  // ---------- start ----------
  showWho();
  if (ready()) show('home'); else editWho();
})();
