from playwright.sync_api import sync_playwright

def run_test():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        
        # 1. Gym tab scrolled
        page.locator('button[onclick*="gym"]').first.click()
        page.wait_for_timeout(300)
        page.evaluate('window.scrollTo(0, 900)')
        page.wait_for_timeout(300)
        page.screenshot(path='cloudflare/screenshot_gym_scrolled.png')
        
        # 2. Gym tab bottom
        page.evaluate('window.scrollTo(0, 2200)')
        page.wait_for_timeout(300)
        page.screenshot(path='cloudflare/screenshot_gym_bottom.png')

        # 3. Workouts tab scrolled
        page.locator('button[onclick*="workouts"]').click()
        page.wait_for_timeout(300)
        page.evaluate('window.scrollTo(0, 800)')
        page.wait_for_timeout(300)
        page.screenshot(path='cloudflare/screenshot_workouts_scrolled.png')

        print("SCROLLED SCREENSHOTS READY!")
        browser.close()

if __name__ == '__main__':
    run_test()
