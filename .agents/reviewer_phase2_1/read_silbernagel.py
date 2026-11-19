import sys, pypdf
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

reader = pypdf.PdfReader("data/papers/pdfs/silbernagel_2015_achilles_rehab.pdf")
print("Page 1 full text:")
print(reader.pages[0].extract_text()[:1000])
