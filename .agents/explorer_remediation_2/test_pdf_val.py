import pypdf
from pathlib import Path
import re
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
PDFS_DIR = PROJECT_ROOT / "data" / "papers" / "pdfs"

FORBIDDEN_PATTERNS = [
    (r"\bracecadotril\b", "Pediatric Diarrhea / Racecadotril"),
    (r"\bdiarrhoea\s+in\s+children\b", "Pediatric Diarrhea"),
    (r"\b6-hydroxydopamine\b", "Rat Parkinson's / 6-OHDA"),
    (r"\bl-dopa-induced\s+dyskinesia\b", "Rat Parkinson's / Dyskinesia"),
    (r"\bmurine\s+bone\s+marrow\b", "Mouse Immunology"),
    (r"\bratingg\b", "Mouse Immunology"),
]

def validate_pdf_content(pdf_path: Path, paper: dict) -> tuple[bool, str]:
    if not pdf_path.exists() or pdf_path.stat().st_size < 10000:
        return False, "File missing or too small"
        
    try:
        reader = pypdf.PdfReader(str(pdf_path))
        if len(reader.pages) == 0:
            return False, "0 pages in PDF"
            
        # Extract text from first 2 pages
        extracted_text = ""
        for i in range(min(2, len(reader.pages))):
            page_txt = reader.pages[i].extract_text() or ""
            extracted_text += " " + page_txt
            
        lower_txt = extracted_text.lower()
        
        # Check forbidden patterns
        for pattern, domain in FORBIDDEN_PATTERNS:
            if re.search(pattern, lower_txt):
                return False, f"Detected forbidden foreign domain text: {domain}"
                
        # Check title/domain keywords
        title = paper.get("title", "")
        title_keywords = [w.lower() for w in re.findall(r"\b[a-zA-Z]{4,}\b", title) if w.lower() not in {"with", "than", "from", "that", "this", "their", "have", "more", "into"}]
        matched = [w for w in title_keywords if w in lower_txt]
        match_ratio = len(matched) / len(title_keywords) if title_keywords else 0
        
        # Check first author surname
        authors = paper.get("authors", [])
        author_ok = False
        if authors:
            surname = authors[0].split()[-1].lower()
            clean_surname = re.sub(r"[^a-zA-Z]", "", surname)
            if clean_surname in lower_txt or surname in lower_txt:
                author_ok = True
                
        if match_ratio < 0.35 and not author_ok:
            return False, f"Title/author keyword match failed (ratio={match_ratio:.2f}, author_found={author_ok})"
            
        return True, f"Verified authentic (match_ratio={match_ratio:.2f}, author_found={author_ok})"
    except Exception as e:
        return False, f"PDF read error: {e}"

if __name__ == '__main__':
    from scripts.ingest_papers import PAPER_CATALOG
    
    for paper in PAPER_CATALOG:
        pdf_file = PDFS_DIR / paper["pdf_filename"]
        ok, msg = validate_pdf_content(pdf_file, paper)
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {paper['id']:<35} : {msg}")
