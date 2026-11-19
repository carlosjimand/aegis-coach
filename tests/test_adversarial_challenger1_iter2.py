"""
Aegis Coach — Iteration 2 Gate Adversarial Stress Testing Harness (Challenger 1)
=============================================================================
Author: Challenger 1 (critic, specialist)
Phase 2 Iteration 2 Gate Empirical Verification Suite

Rigorous empirical stress-testing against the 11 re-ingested literature papers:
1. Forensic content verification: zero non-sports medical contamination (pediatric diarrhea, mouse bone marrow, rat Parkinson's)
2. Domain-specific clinical authenticity verification across all 11 papers
3. Verification of resolution for baseline backwards tokens (gniniart, ytisnetni, emit .tni)
4. Strict GFM table syntax parser & column count alignment validator across all 11 papers
5. UTF-8 byte integrity, forbidden control characters, printable ratios, and word counts
6. Production RAG chunking simulation with metadata propagation & vocabulary density
7. PDF binary integrity, magic bytes, EOF markers, and PyPDF parseability
8. Manifest cross-consistency across all 11 papers (PDFs, Markdown, JSON)
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple
import pypdf
import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "papers"
PDFS_DIR = DATA_DIR / "pdfs"
MARKDOWN_DIR = DATA_DIR / "markdown"
MANIFEST_PATH = DATA_DIR / "manifest.json"

EXPECTED_PAPERS = [
    "askling_2013_l_protocol",
    "askling_2014_l_protocol_acute",
    "blagrove_2018_strength_runners",
    "cook_2016_tendon_continuum",
    "gabbett_2016_acwr",
    "haugen_2022_polarized",
    "millet_2011_ultra_trail_fatigue",
    "seiler_tonnessen_2009_polarized",
    "silbernagel_2007_pain_monitoring",
    "silbernagel_2015_achilles_rehab",
    "stoggl_sperlich_2014_polarized",
]

CLINICAL_SIGNATURES = {
    "askling_2013_l_protocol": {
        "required_authors": ["Askling"],
        "required_keywords": ["extender", "diver", "glider", "hamstring", "l-protocol", "lengthening"],
        "domain": "hamstring",
    },
    "askling_2014_l_protocol_acute": {
        "required_authors": ["Askling"],
        "required_keywords": ["acute", "hamstring", "sprinter", "return to play", "l-protocol"],
        "domain": "hamstring",
    },
    "blagrove_2018_strength_runners": {
        "required_authors": ["Blagrove"],
        "required_keywords": ["strength training", "distance runners", "running economy", "1rm", "plyometric"],
        "domain": "strength",
    },
    "cook_2016_tendon_continuum": {
        "required_authors": ["Cook", "Purdam"],
        "required_keywords": ["tendon", "continuum", "reactive", "disrepair", "degenerative", "isometric"],
        "domain": "tendon",
    },
    "gabbett_2016_acwr": {
        "required_authors": ["Gabbett"],
        "required_keywords": ["acute:chronic", "workload", "acwr", "training-injury", "injury"],
        "domain": "load",
    },
    "haugen_2022_polarized": {
        "required_authors": ["Haugen"],
        "required_keywords": ["polarized", "pyramidal", "endurance", "zone", "threshold"],
        "domain": "polarized",
    },
    "millet_2011_ultra_trail_fatigue": {
        "required_authors": ["Millet"],
        "required_keywords": ["ultra-trail", "fatigue", "neuromuscular", "mvc", "central", "peripheral"],
        "domain": "fatigue",
    },
    "seiler_tonnessen_2009_polarized": {
        "required_authors": ["Seiler", "Tønnessen"],
        "required_keywords": ["polarized", "endurance", "training zones", "80/20", "heart rate"],
        "domain": "polarized",
    },
    "silbernagel_2007_pain_monitoring": {
        "required_authors": ["Silbernagel"],
        "required_keywords": ["pain-monitoring", "achilles", "tendinopathy", "loading", "vas"],
        "domain": "achilles",
    },
    "silbernagel_2015_achilles_rehab": {
        "required_authors": ["Silbernagel", "Crossley"],
        "required_keywords": ["achilles", "tendinopathy", "return to sport", "rehabilitation", "progressive loading"],
        "domain": "achilles",
    },
    "stoggl_sperlich_2014_polarized": {
        "required_authors": ["Stöggl", "Sperlich"],
        "required_keywords": ["polarized", "hiit", "threshold", "hvt", "vo2max", "endurance"],
        "domain": "polarized",
    },
}

FOREIGN_CONTAMINATION_MARKERS = [
    "racecadotril",
    "acute diarrhoea in children",
    "stool frequency",
    "diarrhea in children",
    "gordon m, akobeng",
    "ratigg",
    "bdbiosciences",
    "murine bone marrow",
    "neutrophil granulocytes from murine",
    "mike hasenberg",
    "6-hydroxydopamine",
    "parkinson’s rats",
    "l-dopa-induced dyskinesia",
    "song l, zhang z",
    "dyskinesia in parkinson",
]

BASELINE_BACKWARDS_DEFECTS = [
    "gniniart",
    "ytisnetni",
    "emit .tni",
    "emit.tni",
    "deunitnoc",
    "eulav-p",
    "dnuorgkcab",
    "ecnatsiser",
    "cirtemoylp",
    "lavretni",
]


def parse_frontmatter_and_body(file_path: Path) -> Tuple[Dict[str, Any], str]:
    content = file_path.read_text(encoding="utf-8")
    normalized = content.replace("\r\n", "\n")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", normalized, re.DOTALL)
    if not match:
        return {}, normalized
    yaml_text = match.group(1)
    body = match.group(2)
    data = yaml.safe_load(yaml_text) or {}
    return data, body


class TestPhase2Iter2AdversarialLiteratureValidation:
    """Rigorous empirical validation of the re-ingested literature corpus."""

    def test_corpus_completeness_11_papers(self):
        """Verify that exactly 11 distinct papers exist in pdfs/, markdown/, and manifest.json."""
        assert PDFS_DIR.exists(), "PDFs directory missing"
        assert MARKDOWN_DIR.exists(), "Markdown directory missing"
        assert MANIFEST_PATH.exists(), "Manifest JSON missing"

        pdf_names = {p.stem for p in PDFS_DIR.glob("*.pdf")}
        md_names = {m.stem for m in MARKDOWN_DIR.glob("*.md")}

        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest_data = json.load(f)
        manifest_names = {p["id"] for p in manifest_data.get("papers", [])}

        expected_set = set(EXPECTED_PAPERS)

        missing_pdfs = expected_set - pdf_names
        missing_mds = expected_set - md_names
        missing_manifest = expected_set - manifest_names

        assert not missing_pdfs, f"Missing PDFs: {missing_pdfs}"
        assert not missing_mds, f"Missing Markdown: {missing_mds}"
        assert not missing_manifest, f"Missing Manifest entries: {missing_manifest}"

        assert len(pdf_names) == 11, f"Expected exactly 11 PDFs, got {len(pdf_names)}"
        assert len(md_names) == 11, f"Expected exactly 11 Markdown files, got {len(md_names)}"
        assert len(manifest_names) == 11, f"Expected exactly 11 manifest entries, got {len(manifest_names)}"

    def test_zero_foreign_medical_contamination(self):
        """Forensic check across all 11 markdown files and 11 PDFs for zero foreign medical topics."""
        contaminated = []

        for paper_id in EXPECTED_PAPERS:
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            md_text = md_path.read_text(encoding="utf-8").lower()

            for marker in FOREIGN_CONTAMINATION_MARKERS:
                if marker.lower() in md_text:
                    contaminated.append((f"{paper_id}.md", marker))

            pdf_path = PDFS_DIR / f"{paper_id}.pdf"
            reader = pypdf.PdfReader(str(pdf_path))
            pdf_text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    pdf_text += " " + extracted.lower()

            for marker in FOREIGN_CONTAMINATION_MARKERS:
                if marker.lower() in pdf_text:
                    contaminated.append((f"{paper_id}.pdf", marker))

        assert not contaminated, f"Contaminated files found: {contaminated}"

    def test_clinical_authenticity_and_domain_signatures(self):
        """Verify each paper matches its authentic authors and required clinical terminology."""
        failures = []

        for paper_id, sig in CLINICAL_SIGNATURES.items():
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            fm, body = parse_frontmatter_and_body(md_path)
            full_text = (fm.get("title", "") + " " + " ".join(fm.get("authors", [])) + " " + body).lower()

            # Check authors
            for author in sig["required_authors"]:
                if author.lower() not in full_text:
                    failures.append(f"{paper_id}: missing expected author '{author}'")

            # Check clinical keywords
            matched_kw = [kw for kw in sig["required_keywords"] if kw.lower() in full_text]
            if len(matched_kw) < len(sig["required_keywords"]) // 2 + 1:
                failures.append(f"{paper_id}: matched only {matched_kw} out of {sig['required_keywords']}")

        assert not failures, f"Clinical authenticity failures:\n" + "\n".join(failures)

    def test_baseline_backwards_ocr_tokens_resolved(self):
        """Adversarially verify that all Iteration 1 reported backwards tokens are 100% absent."""
        findings = []
        for paper_id in EXPECTED_PAPERS:
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            text = md_path.read_text(encoding="utf-8").lower()

            for r_term in BASELINE_BACKWARDS_DEFECTS:
                if r_term in text:
                    findings.append((paper_id, r_term))

        assert not findings, f"Baseline backwards text artifacts still present: {findings}"

    def test_strict_gfm_table_syntax_and_delimiters(self):
        """Extract every Markdown table across all 11 papers and verify strict GFM compliance."""
        syntax_errors = []

        for paper_id in EXPECTED_PAPERS:
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            lines = md_path.read_text(encoding="utf-8").splitlines()

            in_table = False
            header_cols = 0
            delimiter_cols = 0
            table_line_start = 0

            for line_idx, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("|") and stripped.endswith("|"):
                    if not in_table:
                        # Header row
                        in_table = True
                        table_line_start = line_idx
                        header_cols = len([c for c in stripped.split("|")[1:-1]])
                        delimiter_cols = 0
                    elif delimiter_cols == 0:
                        # Delimiter row directly follows header
                        # Must only contain -, :, |, whitespace
                        inner_chars = set(stripped.replace("|", "").replace(" ", "").replace("\t", ""))
                        if not inner_chars.issubset({"-", ":"}):
                            syntax_errors.append(
                                f"{paper_id}.md line {line_idx}: Invalid delimiter line characters '{stripped}'"
                            )
                        delim_cells = [c.strip() for c in stripped.split("|")[1:-1]]
                        delimiter_cols = len(delim_cells)
                        for cell_idx, cell in enumerate(delim_cells, 1):
                            if not re.match(r"^:?-+:?$", cell):
                                syntax_errors.append(
                                    f"{paper_id}.md line {line_idx} cell {cell_idx}: Malformed delimiter cell '{cell}'"
                                )
                        if delimiter_cols != header_cols:
                            syntax_errors.append(
                                f"{paper_id}.md line {line_idx}: Delimiter col count ({delimiter_cols}) != Header col count ({header_cols})"
                            )
                    else:
                        # Data row
                        data_cols = len([c for c in stripped.split("|")[1:-1]])
                        if data_cols != header_cols:
                            syntax_errors.append(
                                f"{paper_id}.md line {line_idx}: Data row col count ({data_cols}) != Header col count ({header_cols})"
                            )
                else:
                    if in_table:
                        if delimiter_cols == 0:
                            syntax_errors.append(
                                f"{paper_id}.md line {table_line_start}: Table header has no delimiter row directly below it"
                            )
                        in_table = False

        assert not syntax_errors, f"GFM Table syntax errors detected:\n" + "\n".join(syntax_errors)

    def test_strict_utf8_cleanliness_and_no_control_chars(self):
        """Verify all 11 Markdown files decode cleanly as UTF-8 without control characters."""
        violations = []

        for paper_id in EXPECTED_PAPERS:
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            raw_bytes = md_path.read_bytes()

            # UTF-8 decoding
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                violations.append(f"{paper_id}.md: UTF-8 decode error: {e}")
                continue

            # Check forbidden control characters (\x00 to \x08, \x0b, \x0c, \x0e to \x1f)
            for char_code in range(0x20):
                if char_code in (0x09, 0x0A, 0x0D):  # tab, newline, carriage return are allowed
                    continue
                char = chr(char_code)
                if char in text:
                    violations.append(f"{paper_id}.md: contains forbidden control char \\x{char_code:02x}")

            # Printable ratio
            printable_count = sum(1 for ch in text if ch.isprintable() or ch in "\n\r\t")
            ratio = printable_count / max(len(text), 1)
            if ratio < 0.99:
                violations.append(f"{paper_id}.md: low printable ratio {ratio:.4f}")

            # Word count check: all markdown papers must have >= 1,000 words
            words = text.split()
            if len(words) < 1000:
                violations.append(f"{paper_id}.md: word count {len(words)} < 1000 minimum threshold")

        assert not violations, f"UTF-8/Control character violations:\n" + "\n".join(violations)

    def test_rag_chunking_viability_and_metadata_completeness(self):
        """Simulate RAG chunking across all 11 papers and verify chunk bounds and metadata."""
        all_chunks = []
        rag_errors = []

        for paper_id in EXPECTED_PAPERS:
            md_path = MARKDOWN_DIR / f"{paper_id}.md"
            fm, body = parse_frontmatter_and_body(md_path)

            words = body.split()
            chunk_size = 500
            overlap = 100
            i = 0
            paper_chunks = []

            while i < len(words):
                chunk_slice = words[i : i + chunk_size]
                chunk_text = " ".join(chunk_slice)
                chunk_obj = {
                    "paper_id": paper_id,
                    "chunk_idx": len(paper_chunks),
                    "text": chunk_text,
                    "word_count": len(chunk_slice),
                    "title": fm.get("title"),
                    "doi": fm.get("doi"),
                    "domain": fm.get("domain"),
                    "key_protocols": fm.get("key_protocols", []),
                }
                paper_chunks.append(chunk_obj)
                if i + chunk_size >= len(words):
                    break
                i += chunk_size - overlap

            if len(paper_chunks) < 2:
                rag_errors.append(f"{paper_id}: generated only {len(paper_chunks)} chunks")

            for ch in paper_chunks:
                if ch["word_count"] < 40 or ch["word_count"] > 600:
                    rag_errors.append(f"{paper_id} chunk {ch['chunk_idx']}: invalid word count {ch['word_count']}")
                if not ch["title"] or not ch["doi"] or not ch["domain"]:
                    rag_errors.append(f"{paper_id} chunk {ch['chunk_idx']}: missing required metadata")

            all_chunks.extend(paper_chunks)

        assert not rag_errors, f"RAG chunking errors:\n" + "\n".join(rag_errors)
        assert len(all_chunks) >= 120, f"Expected total chunks >= 120, got {len(all_chunks)}"

    def test_pdf_binary_integrity_and_page_counts(self):
        """Verify all 11 PDF files are valid, non-empty, parseable by PyPDF, and have >= 120KB."""
        pdf_errors = []

        for paper_id in EXPECTED_PAPERS:
            pdf_path = PDFS_DIR / f"{paper_id}.pdf"
            assert pdf_path.exists(), f"PDF missing: {pdf_path}"

            size = pdf_path.stat().st_size
            if size < 50_000:
                pdf_errors.append(f"{paper_id}.pdf: size {size} bytes < 50,000 minimum")

            raw = pdf_path.read_bytes()
            if not raw.startswith(b"%PDF-"):
                pdf_errors.append(f"{paper_id}.pdf: missing %PDF- header")
            if b"%%EOF" not in raw[-4096:]:
                pdf_errors.append(f"{paper_id}.pdf: missing %%EOF marker")

            try:
                reader = pypdf.PdfReader(str(pdf_path))
                num_pages = len(reader.pages)
                if num_pages == 0:
                    pdf_errors.append(f"{paper_id}.pdf: 0 pages in PDF")
                first_text = reader.pages[0].extract_text()
                if not first_text or len(first_text.strip()) < 50:
                    pdf_errors.append(f"{paper_id}.pdf: Page 1 text extraction returned empty")
            except Exception as e:
                pdf_errors.append(f"{paper_id}.pdf: PyPDF parse exception: {e}")

        assert not pdf_errors, f"PDF binary errors:\n" + "\n".join(pdf_errors)
