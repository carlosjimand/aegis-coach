from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 420, 'height': 900})
    page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev')
    page.wait_for_timeout(1000)
    page.click('#tab-btn-gym')
    page.wait_for_timeout(800)
    
    page.evaluate("document.getElementById('gym-exercises-container')?.scrollIntoView({ behavior: 'instant', block: 'start' });")
    page.wait_for_timeout(800)
    page.screenshot(path='live_pwa_scrolled_exercises.png')
    print('Captured live_pwa_scrolled_exercises.png')
    browser.close()
