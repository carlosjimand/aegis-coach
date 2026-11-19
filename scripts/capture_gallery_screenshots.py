import os
from playwright.sync_api import sync_playwright

abs_path = os.path.abspath('docs/ejercicios_anatomicos_2d.html')
file_url = f"file:///{abs_path.replace(os.sep, '/')}"

print(f"Opening gallery at: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 1800})
    page.goto(file_url)
    
    # Capturar Rutina 1
    page.click('#tab-1')
    page.wait_for_timeout(300)
    page.screenshot(path='gallery_rutina_1.png', full_page=False)
    print("Captured gallery_rutina_1.png")
    
    # Capturar Rutina 2
    page.click('#tab-2')
    page.wait_for_timeout(300)
    page.screenshot(path='gallery_rutina_2.png', full_page=False)
    print("Captured gallery_rutina_2.png")

    # Capturar Rutina 3
    page.click('#tab-3')
    page.wait_for_timeout(300)
    page.screenshot(path='gallery_rutina_3.png', full_page=False)
    print("Captured gallery_rutina_3.png")

    # Capturar Rutina 4
    page.click('#tab-4')
    page.wait_for_timeout(300)
    page.screenshot(path='gallery_rutina_4.png', full_page=False)
    print("Captured gallery_rutina_4.png")

    browser.close()

print("All gallery screenshots captured successfully!")
