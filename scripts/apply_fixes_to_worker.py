import re

with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update sw.js in index.ts
old_sw_pattern = r'const swCode = `// Aegis Coach — Service Worker PWA Offline.*?`;'
new_sw = """const swCode = `// Aegis Coach — Service Worker PWA v6
const CACHE_NAME = 'aegis-coach-v6';
const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/favicon.ico',
  '/img/icon-192.png?v=20261116b',
  '/img/icon-512.png?v=20261116b',
  '/img/apple-touch-icon.png?v=20261116b'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        PRECACHE_ASSETS.map((url) => {
          return fetch(url, { cache: 'no-cache' }).then((response) => {
            if (response && response.status === 200) {
              return cache.put(url, response);
            }
          }).catch((err) => {
            console.warn('Precache skip: ' + url, err);
          });
        })
      );
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Purging old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const requestUrl = new URL(req.url);

  // Bypass cache for API and Webhook requests
  if (requestUrl.pathname.startsWith('/api/') || requestUrl.pathname.startsWith('/webhook')) {
    return;
  }

  // Network-First for HTML navigation documents so updates apply immediately
  if (req.mode === 'navigate' || req.destination === 'document' || requestUrl.pathname === '/') {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // Same-origin static assets: Stale-While-Revalidate
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      const fetchPromise = fetch(req)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
`;"""

content = re.sub(old_sw_pattern, new_sw, content, flags=re.DOTALL)

# 2. Update Manifest
old_manifest_pattern = r'if \(url\.pathname === "/manifest\.json"\) \{.*?return new Response\(JSON\.stringify\(manifest\), \{'
new_manifest = """if (url.pathname === "/manifest.json") {
      const manifest = {
        name: "Aegis Coach",
        short_name: "Aegis",
        description: "Sistema de Inteligencia y Coaching de Carlos Jiménez Andrino",
        start_url: "/",
        display: "standalone",
        background_color: "#171821",
        theme_color: "#171821",
        orientation: "portrait-primary",
        icons: [
          {
            src: "/img/icon-192.png?v=20261116b",
            sizes: "192x192",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/img/icon-512.png?v=20261116b",
            sizes: "512x512",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/img/icon-192.png?v=20261116b",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable"
          },
          {
            src: "/img/icon-512.png?v=20261116b",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable"
          }
        ]
      };
      return new Response(JSON.stringify(manifest), {"""

content = re.sub(old_manifest_pattern, new_manifest, content, flags=re.DOTALL)

# 3. Add direct handlers for apple-touch-icon and favicon.png before /img/ handler
old_favicon_route = """    // Favicon oficial (.ico) servido desde KV con no-cache
    if (url.pathname === "/favicon.ico") {
      try {
        const icoData = await env.AEGIS_KV.get("img_favicon", { type: "arrayBuffer" });
        if (icoData) {
          return new Response(icoData, {
            headers: {
              "Content-Type": "image/x-icon",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }"""

new_favicon_route = """    // Favicon oficial (.ico) servido desde KV con no-cache
    if (url.pathname === "/favicon.ico") {
      try {
        const icoData = await env.AEGIS_KV.get("img_favicon", { type: "arrayBuffer" });
        if (icoData) {
          return new Response(icoData, {
            headers: {
              "Content-Type": "image/x-icon",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }

    // Favicon PNG oficial en raíz
    if (url.pathname === "/favicon.png" || url.pathname === "/favicon-64.png") {
      try {
        const pngData = await env.AEGIS_KV.get("img_favicon_png", { type: "arrayBuffer" });
        if (pngData) {
          return new Response(pngData, {
            headers: {
              "Content-Type": "image/png",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }

    // Apple Touch Icon oficial en raíz (iOS Safari / PWA shortcuts)
    if (url.pathname === "/apple-touch-icon.png" || url.pathname === "/apple-touch-icon-precomposed.png") {
      try {
        const appleData = await env.AEGIS_KV.get("img_apple-touch-icon", { type: "arrayBuffer" });
        if (appleData) {
          return new Response(appleData, {
            headers: {
              "Content-Type": "image/png",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }"""

content = content.replace(old_favicon_route, new_favicon_route)

# 4. Improve /img/ handler for png vs jpeg
old_img_handler = """      if (cleanPath.startsWith("vector_")) {
        key = cleanPath.replace(".png", "");
        contentType = "image/png";
      } else if (cleanPath.startsWith("icon-")) {
        key = "img_" + cleanPath.replace(".png", "");
        contentType = "image/png";
      } else {
        key = "img_" + cleanPath.replace(".jpg", "").replace(".png", "");
        contentType = "image/jpeg";
      }"""

new_img_handler = """      if (cleanPath.startsWith("vector_")) {
        key = cleanPath.replace(".png", "");
        contentType = "image/png";
      } else if (cleanPath.startsWith("icon-")) {
        key = "img_" + cleanPath.replace(".png", "");
        contentType = "image/png";
      } else if (cleanPath.startsWith("apple-touch-icon")) {
        key = "img_apple-touch-icon";
        contentType = "image/png";
      } else if (cleanPath.startsWith("favicon")) {
        key = cleanPath.includes("32") ? "img_favicon_32" : "img_favicon_png";
        contentType = "image/png";
      } else {
        key = "img_" + cleanPath.replace(".jpg", "").replace(".png", "");
        contentType = cleanPath.endsWith(".png") ? "image/png" : "image/jpeg";
      }"""

content = content.replace(old_img_handler, new_img_handler)

# 5. Fix <head> icons tags
old_head_icons = """  <link rel="manifest" href="/manifest.json?v=6">
  <link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png?v=6">
  <link rel="icon" type="image/svg+xml" href="' + favicon_data_uri + '">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/icon-192.png?v=6">
  <link rel="shortcut icon" href="/favicon.ico?v=6">"""

new_head_icons = """  <link rel="manifest" href="/manifest.json?v=20261116b">
  <link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v=20261116b">
  <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png?v=20261116b">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png?v=20261116b">
  <link rel="shortcut icon" href="/favicon.ico?v=20261116b">"""

content = content.replace(old_head_icons, new_head_icons)

# 6. Add Critical CSS in <style>
critical_css = """
    /* ================================================================= */
    /* CRITICAL FALLBACK CSS (Defensa Estricta Anti-Fallo CDN / Brave)   */
    /* ================================================================= */
    *, ::before, ::after { box-sizing: border-box; }
    .hidden { display: none !important; }
    @media (min-width: 1024px) {
      .hidden.lg\\:flex { display: flex !important; }
      .lg\\:flex { display: flex !important; }
      .lg\\:block { display: block !important; }
      aside#desktop-sidebar { display: flex !important; }
    }
    aside#desktop-sidebar {
      display: none !important;
    }
    @media (min-width: 1024px) {
      aside#desktop-sidebar {
        display: flex !important;
        width: 6rem !important;
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        z-index: 30 !important;
      }
    }
    /* Limites estrictos para SVG: NUNCA pueden superar su contenedor */
    svg {
      max-width: 100%;
      height: auto;
    }
    .logo-container-aside {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
      min-width: 48px !important;
      min-height: 48px !important;
      overflow: hidden !important;
    }
    .logo-container-aside svg {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
    }
    .logo-container-topbar {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      overflow: hidden !important;
    }
    .logo-container-topbar svg {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
    }
    @media (min-width: 640px) {
      .logo-container-topbar {
        width: 44px !important;
        height: 44px !important;
        max-width: 44px !important;
        max-height: 44px !important;
      }
      .logo-container-topbar svg {
        width: 44px !important;
        height: 44px !important;
      }
    }
    .logo-container-profile {
      width: 56px !important;
      height: 56px !important;
      max-width: 56px !important;
      max-height: 56px !important;
      min-width: 56px !important;
      min-height: 56px !important;
      overflow: hidden !important;
    }
    .logo-container-profile svg {
      width: 56px !important;
      height: 56px !important;
    }
"""

content = content.replace("  <style>\n    :root {", f"  <style>{critical_css}\n    :root {{")

# 7. Add defensive attributes and classes to aside and SVGs
old_aside_tag = '<aside class="hidden lg:flex w-24 flex-col items-center py-6 border-r border-[#4d3e50] bg-[#171821] fixed top-0 bottom-0 left-0 z-30">'
new_aside_tag = '<aside id="desktop-sidebar" style="display: none;" class="hidden lg:flex w-24 flex-col items-center py-6 border-r border-[#4d3e50] bg-[#171821] fixed top-0 bottom-0 left-0 z-30">'
content = content.replace(old_aside_tag, new_aside_tag)

old_aside_logo = """      <!-- Monograma Logo SVG -->
      <div onclick="switchTab('dashboard')" class="w-12 h-12 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 mb-8">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

new_aside_logo = """      <!-- Monograma Logo SVG -->
      <div onclick="switchTab('dashboard')" class="logo-container-aside w-12 h-12 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 mb-8" style="width: 48px; height: 48px; max-width: 48px; max-height: 48px;">
        <svg width="48" height="48" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

content = content.replace(old_aside_logo, new_aside_logo)

old_topbar_logo = """          <!-- Monograma Logo -->
          <div onclick="switchTab('dashboard')" class="w-8 h-8 sm:w-11 sm:h-11 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

new_topbar_logo = """          <!-- Monograma Logo -->
          <div onclick="switchTab('dashboard')" class="logo-container-topbar w-8 h-8 sm:w-11 sm:h-11 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0" style="width: 32px; height: 32px; max-width: 44px; max-height: 44px;">
            <svg width="32" height="32" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

content = content.replace(old_topbar_logo, new_topbar_logo)

old_profile_logo = """                <div class="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

new_profile_logo = """                <div class="logo-container-profile w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0" style="width: 56px; height: 56px; max-width: 56px; max-height: 56px;">
                  <svg width="56" height="56" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">"""

content = content.replace(old_profile_logo, new_profile_logo)

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied all fixes to cloudflare/src/index.ts successfully!")
