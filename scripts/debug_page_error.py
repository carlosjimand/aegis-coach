from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    def on_page_error(exc):
        print("PAGE ERROR OCCURRED:")
        print("Message:", exc)
        if hasattr(exc, 'stack'):
            print("Stack:", exc.stack)
            
    page.on("pageerror", on_page_error)
    page.on("console", lambda m: print(f"CONSOLE {m.type}: {m.text}"))
    
    res = page.goto('https://aegis-intervals-sync.uranuslabs.workers.dev')
    content = page.content()
    
    # Save the exact HTML received by the browser to examine
    with open('cloudflare/live_rendered.html', 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Saved cloudflare/live_rendered.html")
    browser.close()
