import os
from playwright.sync_api import sync_playwright

def render_svg_to_png(svg_str, output_png_path, width=800, height=380):
    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 0; background: #000; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
  svg {{ width: {width}px; height: {height}px; display: block; }}
</style>
</head>
<body>
{svg_str}
</body>
</html>"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height})
        page.set_content(html)
        page.screenshot(path=output_png_path)
        browser.close()
    print(f"Rendered {output_png_path}")

print("Rendering helper ready.")
