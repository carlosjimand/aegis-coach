import sys, re
from pathlib import Path
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

clean_mds = sorted(list(Path("data/papers/markdown").glob("*.md")))

for m in clean_mds:
    text = m.read_text(encoding="utf-8")
    lines = text.splitlines()
    table_lines = [l for l in lines if l.strip().startswith("|") and l.strip().endswith("|")]
    
    # Check for squished words like "painwhenpalpating" or "Injurysituation" (words with >20 letters without spaces or camelCase)
    long_squished = re.findall(r'\b[a-z]{18,}\b', text)
    
    # Check for running header/footer artifacts
    headers_footers = []
    for l in lines:
        if "Downloaded from" in l or "first published as" in l or "Protected by copyright" in l:
            headers_footers.append(l)
        if re.search(r'Page \d+ of \d+', l, re.IGNORECASE):
            headers_footers.append(l)
    
    print(f"=== {m.name} ===")
    print(f"  Total lines: {len(lines)} | Pipe lines: {len(table_lines)}")
    print(f"  Long squished words: {len(long_squished)} (e.g. {long_squished[:3]})")
    print(f"  Header/Footer artifacts found: {len(headers_footers)} (e.g. {headers_footers[:2]})")
