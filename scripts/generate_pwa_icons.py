from playwright.sync_api import sync_playwright
from PIL import Image

def generate_icons():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 512, 'height': 512})
        svg_content = """
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="512" height="512" fill="none">
          <rect width="100" height="100" rx="22" fill="#0d0e15"/>
          <defs>
            <linearGradient id="fav_blue" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#38BDF8"/>
              <stop offset="50%" stop-color="#7B88FF"/>
              <stop offset="100%" stop-color="#4F46E5"/>
            </linearGradient>
            <linearGradient id="fav_coral" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#FF758C"/>
              <stop offset="50%" stop-color="#FF5E80"/>
              <stop offset="100%" stop-color="#D946EF"/>
            </linearGradient>
            <linearGradient id="fav_core" x1="50%" y1="0%" x2="50%" y2="100%">
              <stop offset="0%" stop-color="#FFFFFF"/>
              <stop offset="60%" stop-color="#FF5E80"/>
              <stop offset="100%" stop-color="#7B88FF"/>
            </linearGradient>
            <linearGradient id="fav_wing" x1="0%" y1="50%" x2="100%" y2="50%">
              <stop offset="0%" stop-color="#38BDF8"/>
              <stop offset="50%" stop-color="#FFFFFF"/>
              <stop offset="100%" stop-color="#FF5E80"/>
            </linearGradient>
          </defs>
          <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#fav_blue)"/>
          <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#fav_coral)"/>
          <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#fav_core)"/>
          <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#fav_wing)"/>
        </svg>
        """
        page.set_content(f'<body style="margin:0;padding:0;background:#0d0e15;">{svg_content}</body>')
        page.screenshot(path='cloudflare/public_exercises/icon-512.png', clip={'x': 0, 'y': 0, 'width': 512, 'height': 512})
        browser.close()

    im512 = Image.open('cloudflare/public_exercises/icon-512.png')
    im192 = im512.resize((192, 192), Image.Resampling.LANCZOS)
    im192.save('cloudflare/public_exercises/icon-192.png')
    im192.save('cloudflare/public_exercises/favicon.ico', format='ICO')
    print('Generated icon-512.png, icon-192.png, and favicon.ico!')

if __name__ == '__main__':
    generate_icons()
