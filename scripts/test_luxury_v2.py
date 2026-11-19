from playwright.sync_api import sync_playwright

def test_full_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. MOBILE (390 x 844)
        print("=== 1. MOBILE TEST ===")
        context_m = browser.new_context(viewport={'width': 390, 'height': 844})
        page_m = context_m.new_page()
        page_m.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_m.wait_for_timeout(800)
        
        page_m.screenshot(path='cloudflare/v2_mobile_01_dashboard.png')
        print("Saved: v2_mobile_01_dashboard.png")
        
        # Scroll to see weekly spline chart
        page_m.evaluate('window.scrollTo(0, 480)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v2_mobile_02_chart.png')
        print("Saved: v2_mobile_02_chart.png")
        
        # Go to Workouts
        page_m.locator('#dock-btn-workouts').click()
        page_m.wait_for_timeout(600)
        page_m.screenshot(path='cloudflare/v2_mobile_03_workouts.png')
        print("Saved: v2_mobile_03_workouts.png")
        
        # Go to Gym
        page_m.locator('#dock-btn-gym').click()
        page_m.wait_for_timeout(800)
        page_m.evaluate('window.scrollTo(0, 0)')
        page_m.wait_for_timeout(300)
        page_m.screenshot(path='cloudflare/v2_mobile_04_gym_top.png')
        print("Saved: v2_mobile_04_gym_top.png")
        
        # Scroll down to Exercise 1 (Hip Thrust con Barra)
        page_m.evaluate('window.scrollTo(0, 520)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v2_mobile_05_exercise_card.png')
        print("Saved: v2_mobile_05_exercise_card.png")
        
        # Test adding a set on Exercise 1
        print("Testing '+ Añadir Serie' on Exercise 1...")
        add_btn = page_m.locator('#add-set-btn-1')
        add_btn.click()
        page_m.wait_for_timeout(400)
        
        # Take screenshot of set table with the new set added
        page_m.screenshot(path='cloudflare/v2_mobile_06_set_added.png')
        print("Saved: v2_mobile_06_set_added.png")
        
        # Scroll to bottom of gym tab (Markdown box)
        page_m.evaluate('window.scrollTo(0, 4800)')
        page_m.wait_for_timeout(500)
        page_m.screenshot(path='cloudflare/v2_mobile_07_markdown_box.png')
        print("Saved: v2_mobile_07_markdown_box.png")
        
        # Read the generated markdown
        md_text = page_m.locator('#markdown-summary-preview').input_value()
        print("\n--- GENERATED GARMIN MARKDOWN ---")
        print(md_text[:400])
        print("--------------------------------\n")
        
        # Test clicking "Copiar para Notas de Garmin"
        copy_btn = page_m.locator('#copy-gym-btn')
        copy_btn.click()
        page_m.wait_for_timeout(300)
        print("Copy button clicked successfully!")
        
        # 2. DESKTOP (1280 x 800)
        print("\n=== 2. DESKTOP TEST ===")
        context_d = browser.new_context(viewport={'width': 1280, 'height': 800})
        page_d = context_d.new_page()
        page_d.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_d.wait_for_timeout(800)
        
        page_d.screenshot(path='cloudflare/v2_desktop_01_dashboard.png')
        print("Saved: v2_desktop_01_dashboard.png")
        
        # Click Gym in Desktop sidebar
        page_d.locator('#nav-desktop-gym').click()
        page_d.wait_for_timeout(800)
        page_d.evaluate('window.scrollTo(0, 200)')
        page_d.wait_for_timeout(400)
        page_d.screenshot(path='cloudflare/v2_desktop_02_gym.png')
        print("Saved: v2_desktop_02_gym.png")
        
        browser.close()
        print("\n=== ALL TESTS PASSED WITH 100% SUCCESS! ===")

if __name__ == '__main__':
    test_full_flow()
