// The Bernie app was removed (Nov 12 2026).  This clears it off any device that installed it.
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => {
  e.waitUntil(caches.keys().then((k) => Promise.all(k.map((n) => caches.delete(n))))
    .then(() => self.registration.unregister())
    .then(() => self.clients.matchAll()).then((cs) => cs.forEach((c) => c.navigate('/index.html'))));
});
