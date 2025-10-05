const CACHE_NAME = 'make-amsmk2';
const urlsToCache = [
    '/',
    '/static/manifest.webmanifest',
    '/static/icons/icon-192.png',
    '/static/icons/icon-512.png',
    '/static/jquery.min.js',
    '/static/qrcode.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.7/dist/js/bootstrap.bundle.min.js'
];

self.addEventListener("install", (e) => {
    console.log("[Service Worker] installed", e);
    e.waitUntil(
        Promise.resolve().then(() => {
            console.log('Service Worker installed');
        })
    );
});

self.addEventListener("activate", (e) => {
    console.log("[Service Worker] activated", e)
});

self.addEventListener("fetch", (e) => {
    if (e.request.method !== 'GET') {
        return;
    }
    
    if (e.request.mode === 'navigate') {
        return;
    }
    
    if (e.request.url.includes('/api/') || e.request.url.includes('/user/') || e.request.url.includes('/admin/')) {
        return;
    }
    
    console.log("[Service Worker] fetched resource " + e.request.url);
    e.respondWith(
        fetch(e.request).then((response) => {
            if (response.status === 200 && urlsToCache.some(url => e.request.url.includes(url))) {
                const responseToCache = response.clone();
                caches.open(CACHE_NAME).then(cache => {
                    cache.put(e.request, responseToCache);
                });
            }
            return response;
        }).catch(() => {
            return caches.match(e.request).then(response => {
                if (response) {
                    return response;
                }
                return fetch(e.request);
            });
        })
    );
});

self.addEventListener('push', (e) => {
    if (e.data) {
        const data = e.data.json();
        const options = {
            body: data.body,
            icon: '/static/icons/icon-192.png',
            badge: '/static/icons/icon-96.png',
            vibrate: [100, 50, 100],
            data: {
                dateOfArrival: Date.now(),
                primaryKey: 1
            }
        };

        e.waitUntil(
            self.registration.showNotification(data.title, options)
        );
    }
});

self.addEventListener('notificationclick', (e) => {
    e.notification.close();
    e.waitUntil(
        clients.openWindow('/')
    );
});