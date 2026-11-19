with open('cloudflare/src/index.ts', 'r', encoding='utf-8') as f:
    text = f.read()

marker_start = "/* === SELF-CONTAINED TAILWIND PRODUCTION BUNDLE === */"
marker_end = "/* ================================================================="

if marker_start in text and marker_end in text:
    p1 = text.find(marker_start)
    p2 = text.find(marker_end, p1)
    text = text[:p1] + "\n    " + text[p2:]
    print(f"Removed embedded CSS block ({p2 - p1} chars)!")
    with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
        f.write(text)
else:
    print("Markers not found!")
