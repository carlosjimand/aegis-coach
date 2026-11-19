from playwright.sync_api import sync_playwright

def test_v3():
    console_errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. MOBILE TEST (390 x 844)
        print("=== 1. MOBILE SUITE (390 x 844) ===")
        context_m = browser.new_context(viewport={'width': 390, 'height': 844}, permissions=['clipboard-read', 'clipboard-write'])
        page_m = context_m.new_page()
        page_m.on("console", lambda msg: console_errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page_m.on("pageerror", lambda exc: console_errors.append(f"PAGEERROR: {exc}"))
        
        page_m.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_m.wait_for_timeout(1000)
        page_m.screenshot(path='cloudflare/v3_mobile_01_dashboard_top.png')
        print("Saved: v3_mobile_01_dashboard_top.png (Hero Sesión de Hoy arriba)")
        
        # Scroll to see chart and reference cards
        page_m.evaluate('window.scrollTo(0, 500)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v3_mobile_02_dashboard_chart.png')
        print("Saved: v3_mobile_02_dashboard_chart.png")

        page_m.evaluate('window.scrollTo(0, 950)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v3_mobile_03_dashboard_references.png')
        print("Saved: v3_mobile_03_dashboard_references.png")
        
        # Pestaña Entrenos (Calendario Mensual)
        print("\n--- Testing Tab Entrenos & Calendario ---")
        page_m.locator('#dock-btn-workouts').click()
        page_m.wait_for_timeout(800)
        page_m.screenshot(path='cloudflare/v3_mobile_04_calendar.png')
        print("Saved: v3_mobile_04_calendar.png")
        
        # Test clicking on Day 8 (10K Ávila)
        print("Clicking on Day 8 in calendar...")
        page_m.evaluate("() => selectCalendarDay('2026-11-08')")
        page_m.wait_for_timeout(400)
        detail_title_8 = page_m.locator('#detail-title').inner_text()
        print(f"Day 8 Detail Title: {detail_title_8}")
        page_m.screenshot(path='cloudflare/v3_mobile_05_calendar_detail_day8.png')
        print("Saved: v3_mobile_05_calendar_detail_day8.png")

        # Test clicking on Day 14 (6x800m Parque del Soto)
        print("Clicking on Day 14 in calendar...")
        page_m.evaluate("() => selectCalendarDay('2026-11-14')")
        page_m.wait_for_timeout(400)
        detail_title_14 = page_m.locator('#detail-title').inner_text()
        print(f"Day 14 Detail Title: {detail_title_14}")

        # Pestaña Gimnasio
        print("\n--- Testing Tab Gimnasio (Reordered Columns & Exercises) ---")
        page_m.locator('#dock-btn-gym').click()
        page_m.wait_for_timeout(800)
        page_m.evaluate('window.scrollTo(0, 0)')
        page_m.wait_for_timeout(300)
        page_m.screenshot(path='cloudflare/v3_mobile_06_gym_header.png')
        print("Saved: v3_mobile_06_gym_header.png")

        # Scroll to Hip Thrust
        page_m.evaluate('window.scrollTo(0, 520)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v3_mobile_07_gym_exercise_order.png')
        print("Saved: v3_mobile_07_gym_exercise_order.png (Checking Serie - Reps - Carga)")

        # Test dynamic add set
        print("Testing '+ Añadir Serie' on Exercise 1...")
        add_btn = page_m.locator('#add-set-btn-1')
        add_btn.click()
        page_m.wait_for_timeout(400)

        # Scroll to Markdown Summary Box
        page_m.evaluate('window.scrollTo(0, 4800)')
        page_m.wait_for_timeout(500)
        page_m.screenshot(path='cloudflare/v3_mobile_08_gym_markdown.png')
        print("Saved: v3_mobile_08_gym_markdown.png")

        # Click copy button
        copy_btn = page_m.locator('#copy-gym-btn')
        copy_btn.click()
        page_m.wait_for_timeout(300)
        print("Copy button clicked!")

        # Pestaña Objetivos
        print("\n--- Testing Tab Objetivos ---")
        page_m.locator('#dock-btn-goals').click()
        page_m.wait_for_timeout(600)
        page_m.screenshot(path='cloudflare/v3_mobile_09_goals.png')
        print("Saved: v3_mobile_09_goals.png")

        # Pestaña Perfil & IMC
        print("\n--- Testing Tab Perfil & IMC ---")
        page_m.locator('#dock-btn-profile').click()
        page_m.wait_for_timeout(600)
        page_m.screenshot(path='cloudflare/v3_mobile_10_profile_bmi.png')
        print("Saved: v3_mobile_10_profile_bmi.png")

        # Test editing weight in Profile
        print("Testing weight input & dynamic BMI recalculation...")
        weight_input = page_m.locator('#profile-weight')
        weight_input.fill('62.5')
        page_m.wait_for_timeout(300)
        bmi_new = page_m.locator('#bmi-display-value').inner_text()
        print(f"Recalculated BMI for 62.5 kg: {bmi_new} kg/m²")
        page_m.screenshot(path='cloudflare/v3_mobile_11_profile_recalculated.png')
        print("Saved: v3_mobile_11_profile_recalculated.png")

        # Click save profile
        page_m.locator('#save-profile-btn').click()
        page_m.wait_for_timeout(400)

        # 2. DESKTOP TEST (1280 x 800)
        print("\n=== 2. DESKTOP SUITE (1280 x 800) ===")
        context_d = browser.new_context(viewport={'width': 1280, 'height': 800}, permissions=['clipboard-read', 'clipboard-write'])
        page_d = context_d.new_page()
        page_d.on("console", lambda msg: console_errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page_d.on("pageerror", lambda exc: console_errors.append(f"PAGEERROR: {exc}"))

        page_d.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_d.wait_for_timeout(800)
        page_d.screenshot(path='cloudflare/v3_desktop_01_dashboard.png')
        print("Saved: v3_desktop_01_dashboard.png")

        # Desktop Calendar
        page_d.locator('#nav-desktop-workouts').click()
        page_d.wait_for_timeout(800)
        page_d.screenshot(path='cloudflare/v3_desktop_02_calendar.png')
        print("Saved: v3_desktop_02_calendar.png")

        # Desktop Gym
        page_d.locator('#nav-desktop-gym').click()
        page_d.wait_for_timeout(800)
        page_d.evaluate('window.scrollTo(0, 300)')
        page_d.wait_for_timeout(400)
        page_d.screenshot(path='cloudflare/v3_desktop_03_gym.png')
        print("Saved: v3_desktop_03_gym.png")

        # Desktop Profile
        page_d.locator('#nav-desktop-profile').click()
        page_d.wait_for_timeout(800)
        page_d.screenshot(path='cloudflare/v3_desktop_04_profile.png')
        print("Saved: v3_desktop_04_profile.png")

        browser.close()

    print("\n=== CONSOLE ERRORS CHECK ===")
    if console_errors:
        print(f"Errors found ({len(console_errors)}):")
        for err in console_errors:
            print("  ", err)
    else:
        print("ZERO errors! 100% flawless execution.")

if __name__ == '__main__':
    test_v3()
