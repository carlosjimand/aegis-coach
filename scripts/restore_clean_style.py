with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

# The compiled css was inserted after <style>
# Let's find <style> and :root {
idx_style = text.find('<style>')
idx_root = text.find(':root {', idx_style)

# Between <style> and :root { was the original critical CSS
# Let's inspect what is between them
print("Distance between <style> and :root {:", idx_root - idx_style)
original_between = """
    /* ================================================================= */
    /* CRITICAL FALLBACK CSS (Defensa Estricta Anti-Fallo CDN / Brave)   */
    /* ================================================================= */
    *, ::before, ::after { box-sizing: border-box; }
    .hidden { display: none !important; }
    @media (min-width: 1024px) {
      .hidden.lg\\:flex { display: flex !important; }
      .lg\\:flex { display: flex !important; }
      .lg\\:block { display: block !important; }
      aside#desktop-sidebar { display: flex !important; }
    }
    aside#desktop-sidebar {
      display: none !important;
    }
    @media (min-width: 1024px) {
      aside#desktop-sidebar {
        display: flex !important;
        width: 6rem !important;
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        z-index: 30 !important;
      }
    }
    /* Limites estrictos para SVG: NUNCA pueden superar su contenedor */
    svg {
      max-width: 100%;
      height: auto;
    }
    .logo-container-aside {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
      min-width: 48px !important;
      min-height: 48px !important;
      overflow: hidden !important;
    }
    .logo-container-aside svg {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
    }
    .logo-container-topbar {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      overflow: hidden !important;
    }
    .logo-container-topbar svg {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
    }
    @media (min-width: 640px) {
      .logo-container-topbar {
        width: 44px !important;
        height: 44px !important;
        max-width: 44px !important;
        max-height: 44px !important;
      }
      .logo-container-topbar svg {
        width: 44px !important;
        height: 44px !important;
      }
    }
    .logo-container-profile {
      width: 56px !important;
      height: 56px !important;
      max-width: 56px !important;
      max-height: 56px !important;
      min-width: 56px !important;
      min-height: 56px !important;
      overflow: hidden !important;
    }
    .logo-container-profile svg {
      width: 56px !important;
      height: 56px !important;
    }
  """

text = text[:idx_style + len('<style>')] + original_between + "\n    " + text[idx_root:]
with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(text)

print("Restored cleanly!")
