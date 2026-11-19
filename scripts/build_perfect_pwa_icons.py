import os
from playwright.sync_api import sync_playwright
from PIL import Image

def generate_icons():
    # Dimensions: 512x512
    # In viewBox="0 0 100 100", center is at (50, 50).
    # Scaled logo inside safe zone (scale 0.62)
    # Background: #171821 (solid, square 1:1, extends to all edges)
    svg_artwork = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
      <!-- Fondo Solido 1:1 River Styx -->
      <rect width="512" height="512" fill="#171821"/>
      
      <defs>
        <!-- Middy's Purple Gradient -->
        <linearGradient id="pwa_purple" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#c5abde"/>
          <stop offset="50%" stop-color="#a887ce"/>
          <stop offset="100%" stop-color="#70559f"/>
        </linearGradient>
        
        <!-- Mulberry Mix Gradient -->
        <linearGradient id="pwa_mulberry" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#e885a6"/>
          <stop offset="50%" stop-color="#d86991"/>
          <stop offset="100%" stop-color="#9c526d"/>
        </linearGradient>
        
        <!-- Core Luminescent Gradient -->
        <linearGradient id="pwa_core" x1="50%" y1="0%" x2="50%" y2="100%">
          <stop offset="0%" stop-color="#FFFFFF"/>
          <stop offset="50%" stop-color="#f5d0fe"/>
          <stop offset="100%" stop-color="#a887ce"/>
        </linearGradient>
        
        <!-- Cross Wing Gradient -->
        <linearGradient id="pwa_wing" x1="0%" y1="50%" x2="100%" y2="50%">
          <stop offset="0%" stop-color="#c5abde"/>
          <stop offset="50%" stop-color="#FFFFFF"/>
          <stop offset="100%" stop-color="#e885a6"/>
        </linearGradient>

        <!-- Sutil resplandor central para impacto estético -->
        <radialGradient id="pwa_glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#a887ce" stop-opacity="0.25"/>
          <stop offset="60%" stop-color="#9c526d" stop-opacity="0.10"/>
          <stop offset="100%" stop-color="#171821" stop-opacity="0"/>
        </radialGradient>
      </defs>

      <!-- Resplandor de fondo -->
      <circle cx="256" cy="256" r="220" fill="url(#pwa_glow)"/>

      <!-- Logo centrado en la Safe-Zone (Escala 3.3x sobre viewBox 100x100) -->
      <!-- Original viewBox 100x100: centro ~ (50, 52). Desplazamos a (256, 256) -->
      <g transform="translate(256, 256) scale(3.3) translate(-50, -52)">
        <!-- Ala Izquierda (Middy's Purple) -->
        <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" 
              fill="url(#pwa_purple)" filter="drop-shadow(0 4px 12px rgba(168,135,206,0.35))"/>
        
        <!-- Ala Derecha (Mulberry Mix) -->
        <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" 
              fill="url(#pwa_mulberry)" filter="drop-shadow(0 4px 12px rgba(156,82,109,0.35))"/>
        
        <!-- Núcleo Central 'A' -->
        <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" 
              fill="url(#pwa_core)"/>
        
        <!-- Travesaño Aero Wing -->
        <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" 
              fill="url(#pwa_wing)"/>
      </g>
    </svg>
    """

    out_dir = "cloudflare/public_exercises"
    os.makedirs(out_dir, exist_ok=True)
    
    html = f"""<!DOCTYPE html>
    <html>
    <head><style>body,html {{ margin:0; padding:0; background:#171821; overflow:hidden; width:512px; height:512px; }}</style></head>
    <body>{svg_artwork}</body>
    </html>"""

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 512, 'height': 512})
        page.set_content(html)
        page.wait_for_timeout(200)
        
        path_512 = os.path.join(out_dir, 'icon-512.png')
        page.screenshot(path=path_512, clip={'x': 0, 'y': 0, 'width': 512, 'height': 512})
        browser.close()

    # Abrir con Pillow para generar tamaños derivados con interpolación Lanczos
    im512 = Image.open(path_512).convert("RGBA")
    
    # 192x192
    im192 = im512.resize((192, 192), Image.Resampling.LANCZOS)
    im192.save(os.path.join(out_dir, 'icon-192.png'), 'PNG')
    
    # Apple Touch Icon 180x180
    im180 = im512.resize((180, 180), Image.Resampling.LANCZOS)
    im180.save(os.path.join(out_dir, 'apple-touch-icon.png'), 'PNG')
    
    # Favicon PNG 64x64 y 32x32
    im64 = im512.resize((64, 64), Image.Resampling.LANCZOS)
    im64.save(os.path.join(out_dir, 'favicon-64.png'), 'PNG')
    
    im32 = im512.resize((32, 32), Image.Resampling.LANCZOS)
    im32.save(os.path.join(out_dir, 'favicon-32.png'), 'PNG')

    # Favicon ICO multi-resolución (16, 32, 48, 64)
    im16 = im512.resize((16, 16), Image.Resampling.LANCZOS)
    im48 = im512.resize((48, 48), Image.Resampling.LANCZOS)
    
    ico_path = os.path.join(out_dir, 'favicon.ico')
    im64.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    
    print("SUCCESS: Generated icon-512.png, icon-192.png, apple-touch-icon.png, favicon-64.png, favicon-32.png, and favicon.ico!")

if __name__ == "__main__":
    generate_icons()
