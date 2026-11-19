from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    
    # Catch all errors
    page.on("console", lambda m: print(f"[{m.type}] {m.text}"))
    page.on("pageerror", lambda e: print(f"[PAGE ERROR] {e}"))
    
    page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    # Check classes
    print("Tab dashboard hidden?", page.evaluate("() => document.getElementById('tab-dashboard').classList.contains('hidden')"))
    print("Tab workouts hidden?", page.evaluate("() => document.getElementById('tab-workouts').classList.contains('hidden')"))
    print("Tab gym hidden?", page.evaluate("() => document.getElementById('tab-gym').classList.contains('hidden')"))
    
    print("\nClicking #dock-btn-gym directly via JS...")
    page.evaluate("() => switchTab('gym')")
    page.wait_for_timeout(1000)
    
    print("Tab dashboard hidden after switch?", page.evaluate("() => document.getElementById('tab-dashboard').classList.contains('hidden')"))
    print("Tab gym hidden after switch?", page.evaluate("() => document.getElementById('tab-gym').classList.contains('hidden')"))
    
    # Screenshot of gym
    page.screenshot(path='cloudflare/diag_gym.png')
    
    # Check if gym exercises container has content
    has_content = page.evaluate("() => document.getElementById('gym-exercises-container').innerHTML.length")
    print(f"Gym exercises container HTML length: {has_content}")
    
    # Check buttons inside gym
    btn_texts = page.evaluate("() => Array.from(document.querySelectorAll('#tab-gym button')).map(b => b.innerText.trim())")
    print("Buttons inside gym tab:", btn_texts[:10])
    
    browser.close()
