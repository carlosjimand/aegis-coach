from playwright.sync_api import sync_playwright

def test_v4():
    console_errors = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        
        # 1. MOBILE SUITE (390 x 844)
        print("=== 1. MOBILE SUITE (390 x 844) ===")
        context_m = browser.new_context(viewport={'width': 390, 'height': 844}, permissions=['clipboard-read', 'clipboard-write'])
        page_m = context_m.new_page()
        page_m.on("console", lambda msg: console_errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page_m.on("pageerror", lambda exc: console_errors.append(f"PAGEERROR: {exc}"))
        
        page_m.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_m.wait_for_timeout(1000)

        # Check Aero-Aegis Header Logo
        header_svg = page_m.locator('header svg').first
        print(f"Header Aero-Aegis Logo visible: {header_svg.is_visible()}, box: {header_svg.bounding_box()}")
        assert header_svg.is_visible(), "Header logo must be visible"

        page_m.screenshot(path='cloudflare/v4_mobile_01_hero_dashboard.png')
        print("Saved: v4_mobile_01_hero_dashboard.png")

        # Scroll to volume chart
        page_m.evaluate('window.scrollTo(0, 520)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v4_mobile_02_volume_chart.png')
        print("Saved: v4_mobile_02_volume_chart.png")

        # Test Tab Entrenos & Subviews
        print("\n--- Testing Tab Entrenos & Subviews ---")
        page_m.locator('#dock-btn-workouts').click()
        page_m.wait_for_timeout(800)
        page_m.screenshot(path='cloudflare/v4_mobile_03_calendar_view.png')
        print("Saved: v4_mobile_03_calendar_view.png")

        # Test click on day 14 (6x800m)
        print("Clicking day 14...")
        page_m.locator('div[data-date="2026-11-14"]').click()
        page_m.wait_for_timeout(400)
        detail_14 = page_m.locator('#detail-title').inner_text()
        print(f"Day 14 Title: {detail_14}")
        page_m.screenshot(path='cloudflare/v4_mobile_04_calendar_day14.png')
        print("Saved: v4_mobile_04_calendar_day14.png")

        # Test switching to Microciclo subview
        print("Switching to Próximos Entrenos subview...")
        page_m.locator('#subview-btn-microcycle').click()
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v4_mobile_05_microcycle_view.png')
        print("Saved: v4_mobile_05_microcycle_view.png")

        # Switch back to calendar
        page_m.locator('#subview-btn-calendar').click()
        page_m.wait_for_timeout(300)

        # Test Tab Gimnasio
        print("\n--- Testing Tab Gimnasio (Muscle Subtitles & No Blindaje) ---")
        page_m.locator('#dock-btn-gym').click()
        page_m.wait_for_timeout(800)
        page_m.evaluate('window.scrollTo(0, 0)')
        page_m.wait_for_timeout(300)

        # Verify Blindaje Articular card is GONE
        blindaje_count = page_m.locator('text=Blindaje Articular & Rodilla Izquierda').count()
        print(f"Blindaje Articular cards count (should be 0): {blindaje_count}")
        assert blindaje_count == 0, "Blindaje Articular card must be completely removed"

        # Check Routine chips subtitles
        chip1_text = page_m.locator('#gym-chip-1').inner_text()
        chip2_text = page_m.locator('#gym-chip-2').inner_text()
        chip3_text = page_m.locator('#gym-chip-3').inner_text()
        chip4_text = page_m.locator('#gym-chip-4').inner_text()
        print(f"Chip 1: {chip1_text.replace(chr(10), ' | ')}")
        print(f"Chip 2: {chip2_text.replace(chr(10), ' | ')}")
        print(f"Chip 3: {chip3_text.replace(chr(10), ' | ')}")
        print(f"Chip 4: {chip4_text.replace(chr(10), ' | ')}")

        page_m.screenshot(path='cloudflare/v4_mobile_06_gym_chips.png')
        print("Saved: v4_mobile_06_gym_chips.png")

        # Select Routine 1 to inspect Bulgarian split squat
        print("Selecting Routine 1 (Pierna 1)...")
        page_m.locator('#gym-chip-1').click()
        page_m.wait_for_timeout(500)
        page_m.evaluate('window.scrollTo(0, 1800)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v4_mobile_07_bulgarian_squat.png')
        print("Saved: v4_mobile_07_bulgarian_squat.png")

        # Select Routine 4 to inspect Unilateral Triceps
        print("Selecting Routine 4 (Torso Empuje)...")
        page_m.evaluate('window.scrollTo(0, 0)')
        page_m.wait_for_timeout(300)
        page_m.locator('#gym-chip-4').click()
        page_m.wait_for_timeout(500)
        page_m.evaluate('window.scrollTo(0, 1800)')
        page_m.wait_for_timeout(400)
        page_m.screenshot(path='cloudflare/v4_mobile_08_tricep_unilateral.png')
        print("Saved: v4_mobile_08_tricep_unilateral.png")

        # Test Tab Perfil & Edit Mode Toggle
        print("\n--- Testing Tab Perfil (Locked Inputs & Edit Toggle) ---")
        page_m.locator('#dock-btn-profile').click()
        page_m.wait_for_timeout(800)
        page_m.evaluate('window.scrollTo(0, 0)')
        page_m.wait_for_timeout(300)

        weight_input = page_m.locator('#profile-weight')
        is_disabled_init = weight_input.is_disabled()
        print(f"Weight input initially disabled: {is_disabled_init}")
        assert is_disabled_init, "Weight input must be disabled initially"

        page_m.screenshot(path='cloudflare/v4_mobile_09_profile_locked.png')
        print("Saved: v4_mobile_09_profile_locked.png")

        # Click Editar Perfil
        print("Clicking 'Editar Perfil'...")
        edit_btn = page_m.locator('#profile-edit-btn')
        edit_btn.click()
        page_m.wait_for_timeout(300)

        is_disabled_after = weight_input.is_disabled()
        btn_text_after = edit_btn.inner_text()
        print(f"Weight input disabled after edit click: {is_disabled_after}")
        print(f"Button text after edit click: {btn_text_after}")
        assert not is_disabled_after, "Weight input must be enabled when editing"

        # Edit weight
        weight_input.fill('62.5')
        page_m.wait_for_timeout(300)
        bmi_val = page_m.locator('#bmi-display-value').inner_text()
        print(f"Dynamic BMI with 62.5 kg: {bmi_val}")

        page_m.screenshot(path='cloudflare/v4_mobile_10_profile_editing.png')
        print("Saved: v4_mobile_10_profile_editing.png")

        # Click Guardar Cambios
        print("Clicking 'Guardar Cambios'...")
        edit_btn.click()
        page_m.wait_for_timeout(400)
        is_disabled_saved = weight_input.is_disabled()
        print(f"Weight input disabled after saving: {is_disabled_saved}")
        assert is_disabled_saved, "Weight input must be re-locked after saving"

        page_m.screenshot(path='cloudflare/v4_mobile_11_profile_saved.png')
        print("Saved: v4_mobile_11_profile_saved.png")

        # 2. DESKTOP TEST (1280 x 800)
        print("\n=== 2. DESKTOP SUITE (1280 x 800) ===")
        context_d = browser.new_context(viewport={'width': 1280, 'height': 800}, permissions=['clipboard-read', 'clipboard-write'])
        page_d = context_d.new_page()
        page_d.on("console", lambda msg: console_errors.append(f"CONSOLE {msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page_d.on("pageerror", lambda exc: console_errors.append(f"PAGEERROR: {exc}"))

        page_d.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
        page_d.wait_for_timeout(800)
        page_d.screenshot(path='cloudflare/v4_desktop_01_dashboard.png')
        print("Saved: v4_desktop_01_dashboard.png")

        browser.close()

    print("\n=== CONSOLE ERRORS CHECK ===")
    if console_errors:
        print(f"Errors found ({len(console_errors)}):")
        for err in console_errors:
            print("  ", err)
    else:
        print("ZERO errors! 100% flawless execution across all suites!")

if __name__ == '__main__':
    test_v4()
