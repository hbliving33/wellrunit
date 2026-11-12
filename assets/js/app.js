// Bernie app (app.html): tap, talk, tap again, send.  It becomes one email to support@wellrunit.com.
// The client's name, company and phone are saved only on their own device, so they type them once.
// The recording goes to the server once and is not kept there.
(() => {
  const API = '/api/bernie/';
  const SUPPORT = 'support@wellrunit.com';
  const MAX_SECONDS = 120;
  const KEY = 'bernie-app-contact';
  const $ = (id) => document.getElementById(id);
  const screens = ['setup', 'home', 'review', 'typed', 'sending', 'done', 'failed'];
  const show = (name) => { screens.forEach((s) => { $(s).hidden = s !== name; }); document.querySelector('.foot').hidden = name !== 'home' || !ready(); const h = $(name).querySelector('h1'); if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } };

  // ---------- who is sending (kept on this device only) ----------
  let who = null;
  try { who = JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { who = null; }
  const ready = () => who && who.name && who.company && who.phone;
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
  let rec = null, stream = null, chunks = [], started = 0, tick = null, blob = null, seconds = 0;
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
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || !window.MediaRecorder) return micProblem('This browser can\'t record.  You can type it instead.');
    try { stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); }
    catch (e) { return micProblem('Bernie needs the microphone.  Allow it in your settings, or type it instead.'); }
    const type = pickType();
    try { rec = new MediaRecorder(stream, type ? { mimeType: type, audioBitsPerSecond: 32000 } : { audioBitsPerSecond: 32000 }); }
    catch (e) { release(); return micProblem('Recording didn\'t start.  You can type it instead.'); }
    chunks = [];
    rec.ondataavailable = (e) => { if (e.data && e.data.size) chunks.push(e.data); };
    rec.onstop = () => {
      seconds = Math.max(1, Math.round((Date.now() - started) / 1000));
      blob = new Blob(chunks, { type: (rec && rec.mimeType) || type || 'audio/mp4' });
      release(); setTalk(false);
      if (!blob.size) return micProblem('Nothing was recorded.  Try again, or type it instead.');
      $('reviewLen').textContent = fmt(seconds);
      show('review');
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
    $('homeHint').textContent = on ? `Talking.  Tap again when you're done (up to ${MAX_SECONDS / 60} minutes).` : 'Tap again when you\'re done.  It goes straight to our support team.';
  }
  function micProblem(msg) { release(); setTalk(false); $('homeErr').textContent = msg; $('homeErr').hidden = false; }

  $('talk').addEventListener('click', () => { $('homeErr').hidden = true; if (rec) stop(); else start(); });
  $('redo').addEventListener('click', () => { blob = null; show('home'); });
  $('sendVoice').addEventListener('click', () => send({ audio: blob }));
  document.addEventListener('visibilitychange', () => { if (document.hidden && rec) stop(); });

  // ---------- typing instead ----------
  $('typeIt').addEventListener('click', () => { $('typedErr').hidden = true; show('typed'); setTimeout(() => $('t-text').focus(), 50); });
  $('typedBack').addEventListener('click', () => show('home'));
  $('typedForm').addEventListener('submit', (e) => {
    e.preventDefault();
    const text = $('t-text').value.trim();
    if (text.length < 3) { $('typedErr').textContent = 'Tell us a little about what\'s going on.'; $('typedErr').hidden = false; return; }
    send({ text });
  });

  // ---------- bot check (Cloudflare Turnstile), then send ----------
  let sitekey = null, widget = null, pending = null;
  async function turnstileToken() {
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

  let last = null;
  async function send(payload) {
    last = payload;
    show('sending');
    let ok = false;
    try {
      const token = await turnstileToken();
      const f = new FormData();
      f.append('token', token);
      ['name', 'company', 'phone', 'email'].forEach((k) => f.append(k, (who && who[k]) || ''));
      if (payload.text) f.append('text', payload.text);
      if (payload.audio) f.append('audio', payload.audio, 'ticket.' + (payload.audio.type.includes('webm') ? 'webm' : payload.audio.type.includes('ogg') ? 'ogg' : 'm4a'));
      const r = await fetch(API + 'ticket', { method: 'POST', body: f });
      ok = (await r.json().catch(() => ({}))).ok === true;
    } catch (e) { ok = false; }
    if (ok) { blob = null; $('t-text').value = ''; last = null; show('done'); }
    else show('failed');
  }
  $('retry').addEventListener('click', () => { if (last) send(last); else show('home'); });
  $('failedBack').addEventListener('click', () => show('home'));
  $('again').addEventListener('click', () => show('home'));
  $('mailLink').href = 'mailto:' + SUPPORT;

  // ---------- putting it on the home screen or desktop ----------
  const standalone = window.matchMedia('(display-mode: standalone)').matches || navigator.standalone === true;
  const ua = navigator.userAgent;
  const iOS = /iPhone|iPad|iPod/.test(ua) || (/Macintosh/.test(ua) && navigator.maxTouchPoints > 1);
  const macSafari = !iOS && /Macintosh/.test(ua) && /Safari/.test(ua) && !/Chrome|Chromium|Edg|Firefox/.test(ua);
  let deferred = null;
  function installTip(text, withButton) {
    $('installText').textContent = text;
    $('installBtn').hidden = !withButton;
    $('install').hidden = false;
  }
  if (!standalone) {
    if (iOS) installTip('Put Bernie on your home screen: tap the Share button (on newer iPhones, tap the three dots first), then Add to Home Screen.', false);
    else if (macSafari) installTip('Put Bernie in your Dock: in Safari, choose File, then Add to Dock.', false);
    else installTip('Put Bernie on your desktop or home screen: use Install in your browser\'s address bar or menu.', false);
  }
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault(); deferred = e;
    installTip('Put Bernie on your home screen or desktop, so it\'s one tap away.', true);
  });
  $('installBtn').addEventListener('click', async () => {
    if (!deferred) return;
    deferred.prompt();
    await deferred.userChoice.catch(() => null);
    deferred = null; $('install').hidden = true;
  });
  window.addEventListener('appinstalled', () => { $('install').hidden = true; });

  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/app-sw.js', { scope: '/app' }).catch(() => {});

  // ---------- start ----------
  showWho();
  if (ready()) show('home'); else editWho();
})();
