// Bernie app service worker (scope /app).  Always tries the network first, so the app is never out of date;
// the saved copy only shows the app screen when the phone is offline.  Tickets are never cached or queued.
const CACHE = 'bernie-app-v2';
const SHELL = ['/app.html', '/assets/css/app.css', '/assets/js/app.js', '/assets/brand/app-192.png'];
self.addEventListener('install', (e) => { e.waitUntil(caches.open(CACHE).then((c) => c.addAll(SHELL)).catch(() => {})); self.skipWaiting(); });
self.addEventListener('activate', (e) => { e.waitUntil(caches.keys().then((k) => Promise.all(k.filter((n) => n !== CACHE).map((n) => caches.delete(n)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', (e) => {
  const u = new URL(e.request.url);
  if (e.request.method !== 'GET' || u.origin !== location.origin || u.pathname.startsWith('/api/')) return;
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request, { ignoreSearch: true })));
});
