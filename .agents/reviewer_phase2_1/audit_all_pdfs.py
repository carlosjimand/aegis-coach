import sys, pypdf
from pathlib import Path
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

pdfs = sorted(list(Path("data/papers/pdfs").glob("*.pdf")))

for p in pdfs:
    try:
        reader = pypdf.PdfReader(str(p))
        num_pages = len(reader.pages)
        p1 = reader.pages[0].extract_text()[:400].replace("\n", " ")
        print(f"=== {p.name} ({num_pages} pages) ===")
        print(f"Snippet: {p1}")
        print()
    except Exception as e:
        print(f"=== {p.name} ERROR: {e} ===")
