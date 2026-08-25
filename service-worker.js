const CACHE_NAME = "deportes-ciudad-v1";

self.addEventListener("install", event => {
    console.log("Service Worker instalado");

    self.skipWaiting();
});

self.addEventListener("activate", event => {
    console.log("Service Worker activado");

    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => cacheName !== CACHE_NAME)
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );

    self.clients.claim();
});