import pypdf
reader = pypdf.PdfReader("data/papers/pdfs/millet_2011_ultra_trail_fatigue.pdf")
print("Num pages:", len(reader.pages))
print("Page 1 text:")
print(reader.pages[0].extract_text()[:600])
