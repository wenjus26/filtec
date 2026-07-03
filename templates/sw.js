const CACHE_NAME = 'filtec-cache-v1';
const STATIC_ASSETS = [
  '/',
  '/about/',
  '/why-us/',
  '/products/',
  '/events/',
  '/contact/',
  '/partner/',
  '{% static "css/style.css" %}',
  '{% static "js/main.js" %}',
  '{% static "images/logo.png" %}',
  '{% static "images/favicon/favicon.ico" %}'
];

// Install Event - cache core pages and assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      console.log('[Service Worker] Pre-caching offline assets');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// Activate Event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cache => {
          if (cache !== CACHE_NAME) {
            console.log('[Service Worker] Removing old cache:', cache);
            return caches.delete(cache);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Network first with cache fallback
self.addEventListener('fetch', event => {
  // Only handle GET requests and local requests
  if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then(networkResponse => {
        // If successful response, clone and update the cache
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // If network request fails (offline), return matching asset from cache
        return caches.match(event.request).then(cachedResponse => {
          if (cachedResponse) {
            return cachedResponse;
          }
          // Optional: Return an offline fallback page if available
          return caches.match('/');
        });
      })
  );
});
