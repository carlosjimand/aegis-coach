import os
from playwright.sync_api import sync_playwright

def render_logos():
    with open('cloudflare/public_exercises/logo_concept_1.svg', 'r') as f:
        svg1 = f.read()
    with open('cloudflare/public_exercises/logo_concept_2.svg', 'r') as f:
        svg2 = f.read()
    with open('cloudflare/public_exercises/logo_concept_3.svg', 'r') as f:
        svg3 = f.read()
    with open('cloudflare/public_exercises/logo_concept_4.svg', 'r') as f:
        svg4 = f.read()

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800;900&display=swap" rel="stylesheet">
  <style>body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #141522; color: white; }}</style>
</head>
<body class="p-8 space-y-8">
  <h1 class="text-2xl font-black tracking-tight">AEGIS COACH — EXPLORACIÓN DE LOGOTIPOS VECTORIALES</h1>
  
  <div class="grid grid-cols-4 gap-6">
    <!-- Concept 1 -->
    <div class="p-6 rounded-3xl bg-[#1D1E2C] border border-[#2D2F45] flex flex-col items-center">
      <span class="text-xs font-bold text-[#FF5E80] uppercase tracking-wider mb-4">Concepto 1: Aero-Shield</span>
      <div class="w-24 h-24 p-2 flex items-center justify-center bg-[#141522] rounded-2xl border border-[#2D2F45]/50 mb-4">
        {svg1}
      </div>
      <div class="flex items-center gap-3">
        <div class="w-8 h-8">{svg1}</div>
        <span class="font-extrabold text-sm tracking-wide">AEGIS COACH</span>
      </div>
    </div>

    <!-- Concept 2 -->
    <div class="p-6 rounded-3xl bg-[#1D1E2C] border border-[#2D2F45] flex flex-col items-center">
      <span class="text-xs font-bold text-[#FF5E80] uppercase tracking-wider mb-4">Concepto 2: Fluid 'A' Wing</span>
      <div class="w-24 h-24 p-2 flex items-center justify-center bg-[#141522] rounded-2xl border border-[#2D2F45]/50 mb-4">
        {svg2}
      </div>
      <div class="flex items-center gap-3">
        <div class="w-8 h-8">{svg2}</div>
        <span class="font-extrabold text-sm tracking-wide">AEGIS COACH</span>
      </div>
    </div>

    <!-- Concept 3 -->
    <div class="p-6 rounded-3xl bg-[#1D1E2C] border border-[#2D2F45] flex flex-col items-center">
      <span class="text-xs font-bold text-[#FF5E80] uppercase tracking-wider mb-4">Concepto 3: Bio-Kinetic Armor</span>
      <div class="w-24 h-24 p-2 flex items-center justify-center bg-[#141522] rounded-2xl border border-[#2D2F45]/50 mb-4">
        {svg3}
      </div>
      <div class="flex items-center gap-3">
        <div class="w-8 h-8">{svg3}</div>
        <span class="font-extrabold text-sm tracking-wide">AEGIS COACH</span>
      </div>
    </div>

    <!-- Concept 4 -->
    <div class="p-6 rounded-3xl bg-[#1D1E2C] border border-[#2D2F45] flex flex-col items-center">
      <span class="text-xs font-bold text-[#FF5E80] uppercase tracking-wider mb-4">Concepto 4: Apex Velocity</span>
      <div class="w-24 h-24 p-2 flex items-center justify-center bg-[#141522] rounded-2xl border border-[#2D2F45]/50 mb-4">
        {svg4}
      </div>
      <div class="flex items-center gap-3">
        <div class="w-8 h-8">{svg4}</div>
        <span class="font-extrabold text-sm tracking-wide">AEGIS COACH</span>
      </div>
    </div>
  </div>
</body>
</html>"""

    with open('scripts/test_logos.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 1200, 'height': 500})
        abs_path = os.path.abspath('scripts/test_logos.html').replace('\\', '/')
        page.goto(f'file:///{abs_path}')
        page.wait_for_timeout(500)
        page.screenshot(path='cloudflare/screenshot_logo_comparison.png')
        browser.close()
        print("Captured cloudflare/screenshot_logo_comparison.png")

if __name__ == '__main__':
    render_logos()
