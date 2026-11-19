from playwright.sync_api import sync_playwright

def test_luxury_dashboard():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # ==========================================
        # 1. TEST MÓVIL (390 x 844)
        # ==========================================
        print("--- Testing Mobile View (390 x 844) ---")
        page_m = browser.new_page(viewport={'width': 390, 'height': 844})
        
        page_m.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_m.wait_for_timeout(600)
        page_m.screenshot(path='cloudflare/screenshot_luxury_mobile_dashboard.png')
        
        # Scroll to see chart
        page_m.evaluate('window.scrollTo(0, 480)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/screenshot_luxury_mobile_chart.png')
        
        # Tab Workouts
        page_m.locator('#dock-btn-workouts').click()
        page_m.wait_for_timeout(500)
        page_m.screenshot(path='cloudflare/screenshot_luxury_mobile_workouts.png')
        
        # Tab Gym
        page_m.locator('#dock-btn-gym').click()
        page_m.wait_for_timeout(500)
        page_m.evaluate('window.scrollTo(0, 320)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/screenshot_luxury_mobile_gym.png')

        # Tab Goals
        page_m.locator('#dock-btn-goals').click()
        page_m.wait_for_timeout(500)
        page_m.screenshot(path='cloudflare/screenshot_luxury_mobile_goals.png')

        # ==========================================
        # 2. TEST ESCRITORIO (1280 x 800)
        # ==========================================
        print("--- Testing Desktop View (1280 x 800) ---")
        page_d = browser.new_page(viewport={'width': 1280, 'height': 800})
        
        page_d.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_d.wait_for_timeout(600)
        page_d.screenshot(path='cloudflare/screenshot_luxury_desktop_dashboard.png')
        
        # Tab Gym Desktop
        page_d.locator('#nav-desktop-gym').click()
        page_d.wait_for_timeout(500)
        page_d.evaluate('window.scrollTo(0, 150)')
        page_d.wait_for_timeout(400)
        page_d.screenshot(path='cloudflare/screenshot_luxury_desktop_gym.png')
        
        browser.close()
        print("=== ALL SCREENSHOTS GENERATED SUCCESSFULLY! ===")

if __name__ == '__main__':
    test_luxury_dashboard()
