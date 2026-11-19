with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update sw.js version and precache list
code = code.replace("const CACHE_NAME = 'aegis-coach-v6';", "const CACHE_NAME = 'aegis-coach-v8';")
code = code.replace("const CACHE_NAME = 'aegis-coach-v7';", "const CACHE_NAME = 'aegis-coach-v8';")

old_precache = """const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/favicon.ico',
  '/img/logo.svg',
  '/img/icon-192.png?v=20261116b',
  '/img/icon-512.png?v=20261116b',
  '/img/apple-touch-icon.png?v=20261116b'
];"""

new_precache = """const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/favicon.ico',
  '/css/app.css?v=20261116c',
  '/img/logo.svg',
  '/img/icon-192.png?v=20261116b',
  '/img/icon-512.png?v=20261116b',
  '/img/apple-touch-icon.png?v=20261116b'
];"""

code = code.replace(old_precache, new_precache)

# 2. Add /css/app.css route before /manifest.json
css_route = """    // Hoja de Estilos Tailwind Precompilada desde KV (Self-Contained & Inmune a bloqueos)
    if (url.pathname === "/css/app.css") {
      try {
        const cssData = await env.AEGIS_KV.get("css_app");
        if (cssData) {
          return new Response(cssData, {
            headers: {
              "Content-Type": "text/css; charset=utf-8",
              "Cache-Control": "public, max-age=31536000, immutable"
            }
          });
        }
      } catch (e) {
        console.error("Error leyendo css_app de KV:", e);
      }
      return new Response("/* CSS no disponible */", {
        headers: { "Content-Type": "text/css" },
        status: 404
      });
    }

    // Web App Manifest para Android Chrome y PWA"""

code = code.replace("    // Web App Manifest para Android Chrome y PWA", css_route)

# 3. Add link rel stylesheet in <head>
old_head_link = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>"""

new_head_link = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Hoja de Estilos Propia Compilada (Carga Inmediata y Offline) -->
  <link rel="stylesheet" href="/css/app.css?v=20261116c">
  
  <script src="https://cdn.tailwindcss.com"></script>"""

code = code.replace(old_head_link, new_head_link)

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(code)

print("Applied /css/app.css route and head link successfully!")
