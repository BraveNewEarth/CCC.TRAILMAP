const CACHE_NAME = 'calcagnini-trails-v2';
const TILE_CACHE_NAME = 'calcagnini-tiles-v2';  // Separate cache for tiles (never deleted)

// Core app files to cache immediately
const CORE_FILES = [
    './',
    './index.html',
    './manifest.json',
    './obverlay.png',
    './header-icon.jpg',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
    'https://unpkg.com/leaflet-imageoverlay-rotated@0.2.1/Leaflet.ImageOverlay.Rotated.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@700;800&display=swap'
];


// Install event - cache core files
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Caching core files');
                return cache.addAll(CORE_FILES);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean up old caches (but keep tile cache)
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    // Keep the current app cache and tile cache
                    if (cacheName !== CACHE_NAME && cacheName !== TILE_CACHE_NAME) {
                        console.log('Removing old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - aggressive tile caching for offline use
self.addEventListener('fetch', event => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    // Special handling for map tiles - cache aggressively
    if (event.request.url.includes('tile.openstreetmap.org')) {
        console.log('[SW] Intercepting tile request:', event.request.url);
        event.respondWith(
            caches.open(TILE_CACHE_NAME).then(cache => {
                return cache.match(event.request).then(cachedResponse => {
                    // Return cached tile if available
                    if (cachedResponse) {
                        console.log('[SW] Serving tile from cache:', event.request.url);
                        return cachedResponse;
                    }

                    // Fetch from network and cache
                    console.log('[SW] Fetching tile from network:', event.request.url);
                    return fetch(event.request).then(networkResponse => {
                        // Cache successful responses
                        if (networkResponse && networkResponse.status === 200) {
                            console.log('[SW] Caching tile:', event.request.url);
                            cache.put(event.request, networkResponse.clone());
                        }
                        return networkResponse;
                    }).catch(() => {
                        // Return blank tile if offline and not cached
                        console.log('[SW] Tile fetch failed (offline):', event.request.url);
                        return new Response('', { status: 404 });
                    });
                });
            })
        );
        return;
    }

    // Standard caching for other resources
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // Return cached response if found
                if (response) {
                    return response;
                }

                // Otherwise fetch from network
                return fetch(event.request).then(networkResponse => {
                    // Don't cache non-successful responses
                    if (!networkResponse || networkResponse.status !== 200) {
                        return networkResponse;
                    }

                    // Clone and cache the response
                    const responseToCache = networkResponse.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseToCache);
                    });

                    return networkResponse;
                }).catch(() => {
                    // For HTML pages, try to return cached index
                    if (event.request.headers.get('accept')?.includes('text/html')) {
                        return caches.match('/index.html');
                    }
                });
            })
    );
});
