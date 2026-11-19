import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_TS_PATH = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
PROTOTYPE_DIR = os.path.join(BASE_DIR, 'prototype')
PROTOTYPE_HTML_PATH = os.path.join(PROTOTYPE_DIR, 'index.html')

with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract DEFAULT_PLAN from index.ts
plan_match = re.search(r'const DEFAULT_PLAN: any = (\{.*?\n\};)', content, re.DOTALL)
if not plan_match:
    print("Could not find DEFAULT_PLAN")
    exit(1)

# Extract getLuxuryDashboardHtml function content
func_match = re.search(r'function getLuxuryDashboardHtml\(planData: any\): string \{(.*?)\n\/\*\* FIN DEL WORKER \*\/', content, re.DOTALL)
if not func_match:
    # Try finding the return `<!DOCTYPE html>
    html_match = re.search(r'return `(<!DOCTYPE html>.*?)`;\s*\}', content, re.DOTALL)
    if not html_match:
        print("Could not find HTML template")
        exit(1)
    raw_html = html_match.group(1)
else:
    raw_html = func_match.group(1)

# We want to create a standalone HTML prototype with the UI/UX & Frontend enhancements:
# 1. Compact header (h-14 instead of h-20, removing redundant buttons)
# 2. Stepper buttons in gym sets ([-2.5] [+] [-] [+])
# 3. Rest timer widget (90s / 2m)
# 4. Tactical T-12 Cross del Soto countdown card
# 5. Debounce & safeStorage wrapper

print(f"Extracted template of {len(raw_html)} chars.")
