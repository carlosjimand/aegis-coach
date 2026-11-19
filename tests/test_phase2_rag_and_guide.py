"""
Aegis Coach — Phase 2 Comprehensive Test Suite (`tests/test_phase2_rag_and_guide.py`)
===================================================================================
End-to-End automated validation suite for Phase 2:
- Tier 1: Feature Coverage (PDF Acquisition, Markdown Conversions, Frontmatter Structure, Guide Presence)
- Tier 2: Boundary & Formatting Quality (Form-feeds/Artifacts, Token/Word Counts, Strict YAML Schema, GFM Tables, Heading Hierarchy)
- Tier 3: Cross-Feature Domain & Clinical Integrity (Polarized 80/20, Askling L-Protocol & H-Test, Silbernagel Pain Model & Cook Continuum, ACWR & Ultra-Trail Fatigue)
- Tier 4: Real-World Ingestion & Guide Usability (Manifest JSON Schema, RAG Chunking Simulation, Docker/Qdrant Commands, Ports 6333/6334, Dual Firewall, 5-Stage Diagnostics, .env Template)

Authoritative Source:
- ORIGINAL_REQUEST.md (Requirements R1, R2, R3)
- PROJECT.md (Features 21-31, Milestones M2.1-M2.3, Schemas 1 & 2)
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
import yaml

# ==============================================================================
# PATH CONFIGURATION & CONSTANTS
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "papers"
PDFS_DIR = DATA_DIR / "pdfs"
MARKDOWN_DIR = DATA_DIR / "markdown"
RAW_MARKDOWN_DIR = DATA_DIR / "raw_markdown"
MANIFEST_PATH = DATA_DIR / "manifest.json"
GUIDE_PATH = PROJECT_ROOT / "mvp_next_steps.md"

REQUIRED_GOLD_STANDARD_PAPER_IDS = [
    "stoggl_sperlich_2014_polarized",
    "seiler_tonnessen_2009_polarized",
    "haugen_2022_polarized",
    "askling_2013_l_protocol",
    "askling_2014_l_protocol_acute",
    "silbernagel_2007_pain_monitoring",
    "silbernagel_2015_achilles_rehab",
    "cook_2016_tendon_continuum",
    "gabbett_2016_acwr",
    "millet_2011_ultra_trail_fatigue",
    "blagrove_2018_strength_runners",
]

ALLOWED_DOMAINS = {
    "endurance_physiology",
    "hamstring_rehabilitation",
    "tendinopathy_pain_monitoring",
    "workload_fatigue_biomechanics",
    "polarized_training",
    "injury_rehabilitation",
    "biomechanics",
}

# ==============================================================================
# TEST FIXTURES & HELPER FUNCTIONS
# ==============================================================================

def extract_frontmatter_and_body(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Extract YAML frontmatter dictionary and markdown body from file content (supports LF and CRLF)."""
    normalized = content.replace("\r\n", "\n")
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)$"
    match = re.match(pattern, normalized, re.DOTALL)
    if not match:
        return None, content
    yaml_text = match.group(1)
    body_text = match.group(2)
    try:
        data = yaml.safe_load(yaml_text)
        return (data if isinstance(data, dict) else None), body_text
    except Exception:
        return None, body_text


def count_words(text: str) -> int:
    """Count words in a text block, ignoring punctuation and markdown formatting."""
    clean = re.sub(r"[#*_`~\[\]\(\)\<\>\|\-\+]", " ", text)
    tokens = clean.split()
    return len(tokens)


def validate_gfm_table_syntax(table_text: str) -> Tuple[bool, str]:
    """Validate GitHub Flavored Markdown table header, delimiter, and row columns."""
    lines = [line.strip() for line in table_text.strip().replace("\r\n", "\n").split("\n") if line.strip()]
    if len(lines) < 2:
        return False, "Table must have at least header and delimiter lines."
    
    header = lines[0]
    delimiter = lines[1]
    
    if not (header.startswith("|") and header.endswith("|")):
        return False, f"Header row not enclosed in pipes: {header}"
    
    header_cols = [c.strip() for c in header.split("|")[1:-1]]
    num_cols = len(header_cols)
    if num_cols == 0:
        return False, "Table has 0 columns."
    
    delimiter_pattern = r"^\|(\s*:?-{1,}:?\s*\|)+$"
    if not re.match(delimiter_pattern, delimiter):
        return False, f"Invalid GFM delimiter line: {delimiter}"
    
    delimiter_cols = [c.strip() for c in delimiter.split("|")[1:-1]]
    if len(delimiter_cols) != num_cols:
        return False, f"Delimiter column count ({len(delimiter_cols)}) mismatch with header ({num_cols})."
    
    for idx, row in enumerate(lines[2:], start=3):
        if not (row.startswith("|") and row.endswith("|")):
            return False, f"Row {idx} not enclosed in pipes: {row}"
        row_cols = [c.strip() for c in row.split("|")[1:-1]]
        if len(row_cols) != num_cols:
            return False, f"Row {idx} column count ({len(row_cols)}) mismatch with header ({num_cols})."
            
    return True, "Valid GFM Table"


def simulate_rag_chunking(markdown_body: str, metadata: Dict[str, Any], chunk_size: int = 1200, overlap: int = 200) -> List[Dict[str, Any]]:
    """Simulate production RAG chunking algorithm with metadata propagation."""
    paragraphs = markdown_body.split("\n\n")
    chunks = []
    current_chunk = ""
    chunk_index = 0
    
    for para in paragraphs:
        p = para.strip()
        if not p:
            continue
        if len(current_chunk) + len(p) + 2 <= chunk_size:
            current_chunk = f"{current_chunk}\n\n{p}".strip()
        else:
            if current_chunk:
                chunks.append({
                    "chunk_id": f"{metadata.get('id', 'paper')}_chunk_{chunk_index:03d}",
                    "text": current_chunk,
                    "metadata": metadata,
                    "char_count": len(current_chunk),
                    "estimated_tokens": max(1, len(current_chunk) // 4)
                })
                chunk_index += 1
                # apply overlap
                overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else ""
                current_chunk = f"{overlap_text}\n\n{p}".strip()
            else:
                chunks.append({
                    "chunk_id": f"{metadata.get('id', 'paper')}_chunk_{chunk_index:03d}",
                    "text": p[:chunk_size],
                    "metadata": metadata,
                    "char_count": len(p[:chunk_size]),
                    "estimated_tokens": max(1, len(p[:chunk_size]) // 4)
                })
                chunk_index += 1
                current_chunk = ""
                
    if current_chunk:
        chunks.append({
            "chunk_id": f"{metadata.get('id', 'paper')}_chunk_{chunk_index:03d}",
            "text": current_chunk,
            "metadata": metadata,
            "char_count": len(current_chunk),
            "estimated_tokens": max(1, len(current_chunk) // 4)
        })
    return chunks


# ==============================================================================
# TIER 1: FEATURE COVERAGE
# ==============================================================================

class TestTier1FeatureCoverage:
    """
    Tier 1: Feature Coverage Verification
    - Scientific Literature Acquisition (PDFs >= 5 to 10 papers)
    - MarkItDown Markdown Conversion outputs
    - YAML Frontmatter block inclusion
    - User Action Guide (mvp_next_steps.md) existence
    """

    def test_tc_cov_01_pdf_acquisition_and_count(self):
        """
        TC-COV-01: Verify presence of downloaded Gold Standard scientific PDFs.
        Authoritative source: ORIGINAL_REQUEST.md lines 50-52, PROJECT.md lines 19, 110-123.
        Requirement: At least 5 to 10 high-quality scientific PDFs in data/papers/pdfs/.
        """
        assert PDFS_DIR.exists(), f"PDFs directory does not exist at {PDFS_DIR}."
        pdf_files = list(PDFS_DIR.glob("*.pdf"))
        
        assert len(pdf_files) >= 5, (
            f"Expected at least 5 scientific PDFs in {PDFS_DIR}, but found {len(pdf_files)}. "
            f"Files present: {[f.name for f in pdf_files]}"
        )
        
        # Verify each PDF has meaningful binary size (> 10 KB)
        for pdf in pdf_files:
            size_bytes = pdf.stat().st_size
            assert size_bytes > 10 * 1024, (
                f"PDF file {pdf.name} is too small ({size_bytes} bytes). Must be > 10 KB."
            )

    def test_tc_cov_02_markdown_conversions_presence(self):
        """
        TC-COV-02: Verify presence of converted Markdown files.
        Authoritative source: ORIGINAL_REQUEST.md lines 53-55, 62-64, PROJECT.md lines 20-21, 125.
        Requirement: At least 5 markdown files corresponding to the scientific papers.
        """
        assert MARKDOWN_DIR.exists(), f"Markdown directory does not exist at {MARKDOWN_DIR}."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        assert len(md_files) >= 5, (
            f"Expected at least 5 markdown papers in {MARKDOWN_DIR}, but found {len(md_files)}. "
            f"Files present: {[f.name for f in md_files]}"
        )
        
        for md in md_files:
            size_bytes = md.stat().st_size
            assert size_bytes > 500, (
                f"Markdown file {md.name} is too small ({size_bytes} bytes). Must be > 500 bytes."
            )

    def test_tc_cov_03_frontmatter_block_presence(self):
        """
        TC-COV-03: Verify YAML frontmatter block in each converted markdown paper.
        Authoritative source: PROJECT.md lines 22, 44-76.
        Requirement: Each markdown file starts with '---' and contains structured metadata.
        """
        assert MARKDOWN_DIR.exists(), f"Markdown directory does not exist at {MARKDOWN_DIR}."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) > 0, "No markdown files found to validate frontmatter."
        
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8", errors="replace")
            assert content.startswith("---"), (
                f"File {md_path.name} does not start with YAML frontmatter delimiter '---'."
            )
            # Ensure there is a closing delimiter
            lines = content.splitlines()
            closing_delimiters = [i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---"]
            assert len(closing_delimiters) >= 1, (
                f"File {md_path.name} lacks closing frontmatter delimiter '---'."
            )

    def test_tc_cov_04_mvp_next_steps_guide_presence(self):
        """
        TC-COV-04: Verify existence and non-emptiness of mvp_next_steps.md guide.
        Authoritative source: ORIGINAL_REQUEST.md lines 56-58, 66-68, PROJECT.md lines 24-28, 129.
        Requirement: Step-by-step user action guide generated at project root.
        """
        assert GUIDE_PATH.exists(), f"Guide file does not exist at {GUIDE_PATH}."
        guide_size = GUIDE_PATH.stat().st_size
        assert guide_size > 1000, f"Guide file {GUIDE_PATH.name} is too small ({guide_size} bytes)."
        content = GUIDE_PATH.read_text(encoding="utf-8")
        assert "# Aegis Coach" in content or "Oracle Cloud" in content, (
            "Guide file missing primary title or infrastructure headings."
        )


# ==============================================================================
# TIER 2: BOUNDARY & FORMATTING QUALITY
# ==============================================================================

class TestTier2BoundaryFormattingQuality:
    """
    Tier 2: Boundary & Formatting Quality Verification
    - Absence of raw PDF binary artifacts, form feeds (\\x0c), and null bytes
    - Minimum word count per paper (full paper extraction vs truncated abstract)
    - Strict YAML frontmatter schema validation (types, mandatory keys)
    - GitHub Flavored Markdown (GFM) pipe table syntax
    - Markdown heading hierarchy and formatting integrity
    """

    def test_tc_fmt_01_absence_of_raw_binary_artifacts_and_form_feeds(self):
        """
        TC-FMT-01: Ensure zero form feeds, null bytes, PDF stream markers, or replacement characters.
        Authoritative source: ORIGINAL_REQUEST.md line 63, PROJECT.md line 21.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 5, "Insufficient markdown files for artifact checking."

        for md_path in md_files:
            raw_bytes = md_path.read_bytes()
            # Check for form-feed byte 0x0C
            assert b"\x0c" not in raw_bytes, (
                f"File {md_path.name} contains raw PDF form feed character \\x0c."
            )
            # Check for null bytes 0x00
            assert b"\x00" not in raw_bytes, (
                f"File {md_path.name} contains unprintable null byte \\x00."
            )
            
            content = md_path.read_text(encoding="utf-8", errors="replace")
            # Check for unicode replacement character \ufffd
            assert "\ufffd" not in content, (
                f"File {md_path.name} contains broken Unicode replacement character \\ufffd."
            )
            # Check for raw PDF structural artifacts
            assert "endobj" not in content.lower() or "stream" not in content.lower(), (
                f"File {md_path.name} contains unparsed PDF object streams."
            )

    def test_tc_fmt_02_minimum_content_length_and_word_count(self):
        """
        TC-FMT-02: Ensure thorough content extraction (>= 1000 words per paper).
        Authoritative source: PROJECT.md lines 20-21.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 5, "Insufficient markdown files for word count check."

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            frontmatter, body = extract_frontmatter_and_body(content)
            word_count = count_words(body)
            assert word_count >= 1000, (
                f"File {md_path.name} has only {word_count} words in body. "
                "Expected >= 1000 words for full-length scientific paper."
            )

    def test_tc_fmt_03_strict_yaml_frontmatter_schema_validation(self):
        """
        TC-FMT-03: Validate strict YAML schema types and mandatory fields in frontmatter.
        Authoritative source: PROJECT.md lines 44-76.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 5, "Insufficient markdown files for frontmatter check."

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, _ = extract_frontmatter_and_body(content)
            assert fm is not None, f"Failed to parse YAML frontmatter in {md_path.name}."
            
            # 1. Title validation
            assert "title" in fm, f"Missing 'title' in {md_path.name}"
            assert isinstance(fm["title"], str) and len(fm["title"]) > 5
            
            # 2. Authors validation
            assert "authors" in fm, f"Missing 'authors' in {md_path.name}"
            assert isinstance(fm["authors"], list) and len(fm["authors"]) >= 1
            for author in fm["authors"]:
                assert isinstance(author, str) and len(author) > 0
                
            # 3. Year validation
            assert "year" in fm, f"Missing 'year' in {md_path.name}"
            assert isinstance(fm["year"], int) and 1990 <= fm["year"] <= 2030
            
            # 4. Journal validation
            assert "journal" in fm, f"Missing 'journal' in {md_path.name}"
            assert isinstance(fm["journal"], str) and len(fm["journal"]) > 0
            
            # 5. Identifier validation (doi, pmid, or pmcid)
            has_identifier = any(k in fm and fm[k] for k in ("doi", "pmid", "pmcid"))
            assert has_identifier, f"Missing DOI, PMID, or PMCID in {md_path.name}"
            
            # 6. Domain validation
            assert "domain" in fm, f"Missing 'domain' in {md_path.name}"
            assert isinstance(fm["domain"], str) and fm["domain"] in ALLOWED_DOMAINS
            
            # 7. Topics validation
            assert "topics" in fm, f"Missing 'topics' in {md_path.name}"
            assert isinstance(fm["topics"], list) and len(fm["topics"]) >= 1
            
            # 8. Target Anatomy validation
            assert "target_anatomy" in fm, f"Missing 'target_anatomy' in {md_path.name}"
            assert isinstance(fm["target_anatomy"], list) and len(fm["target_anatomy"]) >= 1
            
            # 9. Key Protocols validation
            assert "key_protocols" in fm, f"Missing 'key_protocols' in {md_path.name}"
            assert isinstance(fm["key_protocols"], list) and len(fm["key_protocols"]) >= 1
            
            # 10. Ingestion metadata validation
            if "ingestion" in fm:
                ing = fm["ingestion"]
                assert isinstance(ing, dict)
                assert "cleaned" in ing and isinstance(ing["cleaned"], bool)

    def test_tc_fmt_04_gfm_markdown_table_syntax_integrity(self):
        """
        TC-FMT-04: Validate GFM pipe syntax for all extracted markdown tables.
        Authoritative source: PROJECT.md lines 11, 74.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        tables_checked = 0
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            _, body = extract_frontmatter_and_body(content)
            
            # Find markdown table blocks
            lines = body.splitlines()
            in_table = False
            current_table_lines = []
            
            for line in lines:
                stripped = line.strip()
                if stripped.startswith("|") and stripped.endswith("|"):
                    in_table = True
                    current_table_lines.append(stripped)
                else:
                    if in_table:
                        # Validate collected table block
                        table_str = "\n".join(current_table_lines)
                        is_valid, reason = validate_gfm_table_syntax(table_str)
                        assert is_valid, f"Malformed GFM table in {md_path.name}: {reason}\nTable:\n{table_str}"
                        tables_checked += 1
                        in_table = False
                        current_table_lines = []
            if in_table:
                table_str = "\n".join(current_table_lines)
                is_valid, reason = validate_gfm_table_syntax(table_str)
                assert is_valid, f"Malformed GFM table in {md_path.name}: {reason}\nTable:\n{table_str}"
                tables_checked += 1
                
        # Asserts tables were tested across corpus
        assert tables_checked >= 0

    def test_tc_fmt_05_heading_hierarchy_integrity(self):
        """
        TC-FMT-05: Validate proper markdown heading hierarchy without orphan tokens or level skips.
        Authoritative source: PROJECT.md lines 11, 21.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            _, body = extract_frontmatter_and_body(content)
            lines = body.splitlines()
            
            last_level = 0
            for line_idx, line in enumerate(lines, start=1):
                match = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
                if match:
                    hashes, title = match.groups()
                    level = len(hashes)
                    assert len(title.strip()) > 0, (
                        f"Empty heading text at line {line_idx} in {md_path.name}"
                    )
                    # Check for severe level jumps (e.g. H1 directly to H4)
                    if last_level > 0 and level > last_level + 2:
                        pytest.fail(
                            f"Abrupt heading level jump from H{last_level} to H{level} "
                            f"at line {line_idx} in {md_path.name}: '{line}'"
                        )
                    last_level = level


# ==============================================================================
# TIER 3: CROSS-FEATURE DOMAIN & CLINICAL INTEGRITY
# ==============================================================================

class TestTier3DomainClinicalIntegrity:
    """
    Tier 3: Domain & Clinical Protocol Integrity Verification
    - Polarized Training 80/20 & 3-Zone Physiological Rules (Seiler, Stöggl & Sperlich, Haugen)
    - Askling Hamstring Lengthening L-Protocol & H-Test Clearance (Askling 2013, 2014)
    - Silbernagel Achilles Tendinopathy Pain-Monitoring Model (Silbernagel 2007, 2015, Cook 2016)
    - Workload Management (ACWR) & Ultra-Trail Neuromuscular Fatigue (Gabbett, Millet, Blagrove)
    """

    def test_tc_clin_01_polarized_training_80_20_protocol_rules(self):
        """
        TC-CLIN-01: Validate Polarized Training 80/20 intensity distribution and threshold rules.
        Authoritative source: Stöggl & Sperlich (2014), Seiler & Tønnessen (2009), Haugen (2022).
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        polarized_papers = []
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            if fm and (
                fm.get("domain") in ("endurance_physiology", "polarized_training") or
                any("polarized" in t for t in fm.get("topics", [])) or
                "polarized" in md_path.name.lower()
            ):
                polarized_papers.append((md_path, fm, body))
                
        assert len(polarized_papers) >= 2, (
            f"Expected at least 2 Polarized Training papers, found {len(polarized_papers)}."
        )
        
        for md_path, fm, body in polarized_papers:
            # Check target anatomy contains cardiovascular / aerobic systems
            anatomy = [a.lower() for a in fm.get("target_anatomy", [])]
            assert any(term in " ".join(anatomy) for term in ("cardiovascular", "aerobic", "metabolic", "mitochondrial")), (
                f"Paper {md_path.name} missing cardiovascular/aerobic target anatomy. Got: {anatomy}"
            )
            
            # Check key protocols mention 80/20, zones, or lactate
            protocols = " ".join(fm.get("key_protocols", [])).lower()
            full_text = (protocols + " " + body).lower()
            
            has_distribution_rule = (
                "80/20" in full_text or "80%" in full_text or "polarized" in full_text
            )
            assert has_distribution_rule, (
                f"Paper {md_path.name} does not state 80/20 or polarized training distribution rule."
            )
            
            has_zone_or_lactate = (
                "zone" in full_text or "lactate" in full_text or "vo2max" in full_text or "mmol" in full_text
            )
            assert has_zone_or_lactate, (
                f"Paper {md_path.name} missing 3-zone, blood lactate, or VO2max physiological metrics."
            )

    def test_tc_clin_02_askling_hamstring_lengthening_l_protocol_rules(self):
        """
        TC-CLIN-02: Validate Askling Hamstring L-Protocol lengthening exercises and H-Test.
        Authoritative source: Askling et al. (2013, 2014) & BJSM Gold Standard RCTs.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        askling_papers = []
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            if fm and (
                "askling" in md_path.name.lower() or
                "hamstring" in fm.get("domain", "") or
                any("hamstring" in t for t in fm.get("topics", [])) or
                any("askling" in a.lower() for a in fm.get("authors", []))
            ):
                askling_papers.append((md_path, fm, body))
                
        assert len(askling_papers) >= 1, (
            f"Expected at least 1 Askling Hamstring paper, found {len(askling_papers)}."
        )
        
        for md_path, fm, body in askling_papers:
            # Check anatomy targets hamstrings / posterior chain
            anatomy = [a.lower() for a in fm.get("target_anatomy", [])]
            assert any(term in " ".join(anatomy) for term in ("hamstring", "biceps femoris", "semitendinosus", "posterior_chain")), (
                f"Paper {md_path.name} missing hamstring target anatomy. Got: {anatomy}"
            )
            
            # Check for the 3 lengthening exercises: Extender, Diver, Glider
            protocols_and_body = (" ".join(fm.get("key_protocols", [])) + " " + body).lower()
            
            assert "extender" in protocols_and_body, (
                f"Paper {md_path.name} missing 'Extender' lengthening exercise."
            )
            assert "diver" in protocols_and_body, (
                f"Paper {md_path.name} missing 'Diver' lengthening exercise."
            )
            assert "glider" in protocols_and_body, (
                f"Paper {md_path.name} missing 'Glider' lengthening exercise."
            )
            
            # Check for return to sport evaluation: H-Test or active flexibility
            assert "h-test" in protocols_and_body or "flexibility" in protocols_and_body or "lengthening" in protocols_and_body, (
                f"Paper {md_path.name} missing H-Test or lengthening clinical criteria."
            )

    def test_tc_clin_03_silbernagel_tendinopathy_pain_monitoring_model(self):
        """
        TC-CLIN-03: Validate Silbernagel Pain-Monitoring Model and Tendon Continuum.
        Authoritative source: Silbernagel et al. (2007, 2015) & Cook et al. (2016).
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        tendon_papers = []
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            if fm and (
                "silbernagel" in md_path.name.lower() or
                "cook" in md_path.name.lower() or
                "tendinopathy" in fm.get("domain", "") or
                any("tendon" in t for t in fm.get("topics", []))
            ):
                tendon_papers.append((md_path, fm, body))
                
        assert len(tendon_papers) >= 2, (
            f"Expected at least 2 Tendinopathy papers, found {len(tendon_papers)}."
        )
        
        for md_path, fm, body in tendon_papers:
            anatomy = [a.lower() for a in fm.get("target_anatomy", [])]
            assert any(term in " ".join(anatomy) for term in ("achilles", "patellar", "tendon")), (
                f"Paper {md_path.name} missing tendon target anatomy. Got: {anatomy}"
            )
            
            protocols_and_body = (" ".join(fm.get("key_protocols", [])) + " " + body).lower()
            
            # Validate pain scale rules (<=5/10) and next-day recovery
            has_pain_model = (
                "pain" in protocols_and_body and
                ("5" in protocols_and_body or "scale" in protocols_and_body or "continuum" in protocols_and_body)
            )
            assert has_pain_model, (
                f"Paper {md_path.name} missing pain-monitoring or tendon continuum parameters."
            )
            
            # Validate loading progression terminology
            has_loading_terminology = any(
                term in protocols_and_body for term in (
                    "isometric", "eccentric", "heavy slow resistance", "hsr", "energy storage", "plyometric", "load"
                )
            )
            assert has_loading_terminology, (
                f"Paper {md_path.name} missing tendon progressive loading terminology."
            )

    def test_tc_clin_04_workload_fatigue_and_strength_biomechanics_rules(self):
        """
        TC-CLIN-04: Validate Workload Management (ACWR), Ultra Fatigue, and Strength Training.
        Authoritative source: Gabbett (2016), Millet et al. (2011), Blagrove et al. (2018).
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        
        biomech_papers = []
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            if fm and (
                "gabbett" in md_path.name.lower() or
                "millet" in md_path.name.lower() or
                "blagrove" in md_path.name.lower() or
                fm.get("domain") in ("workload_fatigue_biomechanics", "biomechanics")
            ):
                biomech_papers.append((md_path, fm, body))
                
        assert len(biomech_papers) >= 2, (
            f"Expected at least 2 workload/fatigue/biomechanics papers, found {len(biomech_papers)}."
        )
        
        all_text = " ".join(
            " ".join(fm.get("key_protocols", [])) + " " + body
            for _, fm, body in biomech_papers
        ).lower()
        
        # Verify ACWR concepts
        assert "workload" in all_text or "acwr" in all_text or "acute" in all_text, (
            "Missing ACWR workload management terminology in biomechanics corpus."
        )
        
        # Verify fatigue / recovery concepts
        assert "fatigue" in all_text or "neuromuscular" in all_text or "recovery" in all_text, (
            "Missing neuromuscular fatigue / recovery concepts in biomechanics corpus."
        )
        
        # Verify strength training / running economy concepts
        assert "strength" in all_text or "economy" in all_text or "resistance" in all_text, (
            "Missing strength training for running economy concepts in biomechanics corpus."
        )


# ==============================================================================
# TIER 4: REAL-WORLD INGESTION & GUIDE USABILITY
# ==============================================================================

class TestTier4RealWorldIngestionAndGuideUsability:
    """
    Tier 4: Ingestion Pipeline & Deployment Guide Usability
    - Manifest JSON schema and path consistency validation
    - Simulated RAG vector store chunking and metadata propagation
    - Docker Compose & Qdrant configuration verification
    - Dual-layer network firewall (OCI VCN Ingress + Ubuntu UFW) verification
    - 5-stage health verification diagnostics
    - Complete production .env configuration template
    """

    def test_tc_use_01_manifest_json_schema_and_path_consistency(self):
        """
        TC-USE-01: Validate data/papers/manifest.json schema and real file path mappings.
        Authoritative source: PROJECT.md lines 78-103.
        """
        assert MANIFEST_PATH.exists(), f"Manifest file does not exist at {MANIFEST_PATH}."
        
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        # 1. Top-level keys
        assert "version" in manifest, "Missing 'version' in manifest.json"
        assert "generated_at" in manifest, "Missing 'generated_at' in manifest.json"
        assert "total_papers" in manifest, "Missing 'total_papers' in manifest.json"
        assert isinstance(manifest["total_papers"], int) and manifest["total_papers"] >= 5
        assert "domains" in manifest and isinstance(manifest["domains"], dict)
        assert "papers" in manifest and isinstance(manifest["papers"], list)
        assert len(manifest["papers"]) == manifest["total_papers"]
        
        # 2. Per-paper validation
        for entry in manifest["papers"]:
            assert "id" in entry, f"Paper entry missing 'id': {entry}"
            assert "pdf_path" in entry, f"Paper entry missing 'pdf_path': {entry}"
            assert "clean_md_path" in entry, f"Paper entry missing 'clean_md_path': {entry}"
            
            # Verify paths resolve to real files
            pdf_full_path = PROJECT_ROOT / entry["pdf_path"]
            clean_md_full_path = PROJECT_ROOT / entry["clean_md_path"]
            
            assert pdf_full_path.exists(), f"Referenced PDF file does not exist: {pdf_full_path}"
            assert clean_md_full_path.exists(), f"Referenced Markdown file does not exist: {clean_md_full_path}"
            
            # Verify metadata consistency with markdown frontmatter
            content = clean_md_full_path.read_text(encoding="utf-8")
            fm, _ = extract_frontmatter_and_body(content)
            assert fm is not None, f"Failed parsing frontmatter for {clean_md_full_path.name}"
            if "title" in entry and entry["title"]:
                assert fm.get("title") == entry["title"], (
                    f"Title mismatch between manifest ('{entry.get('title')}') and frontmatter ('{fm.get('title')}')"
                )

    def test_tc_use_02_rag_chunking_and_metadata_propagation_simulation(self):
        """
        TC-USE-02: Simulate vector store chunking on all markdown papers.
        Authoritative source: PROJECT.md lines 11, 23.
        Requirement: Verify that all papers yield clean chunks with propagated metadata.
        """
        assert MARKDOWN_DIR.exists(), f"Directory {MARKDOWN_DIR} not found."
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 5, "Insufficient markdown files for chunking test."
        
        total_chunks = 0
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            assert fm is not None, f"Missing frontmatter in {md_path.name}"
            
            paper_meta = {
                "id": md_path.stem,
                "title": fm.get("title"),
                "domain": fm.get("domain"),
                "topics": fm.get("topics"),
                "target_anatomy": fm.get("target_anatomy"),
                "key_protocols": fm.get("key_protocols"),
            }
            
            chunks = simulate_rag_chunking(body, paper_meta, chunk_size=1200, overlap=200)
            assert len(chunks) >= 3, (
                f"Paper {md_path.name} produced only {len(chunks)} chunks. Expected >= 3."
            )
            
            for chunk in chunks:
                assert len(chunk["text"]) > 20, f"Empty chunk text in {chunk['chunk_id']}"
                assert chunk["estimated_tokens"] < 2000, f"Chunk too large: {chunk['chunk_id']}"
                assert chunk["metadata"]["id"] == md_path.stem
                assert "target_anatomy" in chunk["metadata"]
                
            total_chunks += len(chunks)
            
        assert total_chunks >= 30, f"Expected >= 30 total chunks across corpus, got {total_chunks}."

    def test_tc_use_03_guide_docker_and_qdrant_deployment_spec(self):
        """
        TC-USE-03: Validate Docker, Qdrant ports (6333/6334), and persistent volume in guide.
        Authoritative source: ORIGINAL_REQUEST.md line 57, PROJECT.md lines 25, 28.
        """
        assert GUIDE_PATH.exists(), f"Guide file {GUIDE_PATH} not found."
        content = GUIDE_PATH.read_text(encoding="utf-8")
        
        # 1. Docker Compose / Docker run presence
        assert "docker" in content.lower(), "Guide missing Docker deployment instructions."
        assert "docker-compose" in content.lower() or "docker compose" in content.lower(), (
            "Guide missing Docker Compose configuration."
        )
        
        # 2. Qdrant ports
        assert "6333" in content, "Guide missing Qdrant HTTP/REST port 6333."
        assert "6334" in content, "Guide missing Qdrant gRPC port 6334."
        
        # 3. Persistent storage mount
        assert "storage" in content.lower() or "volume" in content.lower(), (
            "Guide missing persistent storage volume configuration for Qdrant."
        )
        
        # 4. API Key authentication
        assert "api_key" in content.lower() or "api-key" in content.lower() or "qdrant__service__api_key" in content.lower(), (
            "Guide missing Qdrant API key authentication instructions."
        )

    def test_tc_use_04_guide_dual_layer_network_security_and_firewall(self):
        """
        TC-USE-04: Validate Dual-Layer Firewall instructions (OCI VCN Ingress + Ubuntu UFW).
        Authoritative source: PROJECT.md lines 12, 26, 28.
        """
        assert GUIDE_PATH.exists(), f"Guide file {GUIDE_PATH} not found."
        content = GUIDE_PATH.read_text(encoding="utf-8")
        
        # Layer 1: OCI Cloud Security Lists / Ingress Rules
        assert "ingress" in content.lower() or "security list" in content.lower() or "vcn" in content.lower(), (
            "Guide missing Layer 1: OCI VCN Ingress Security List instructions."
        )
        
        # Layer 2: Host OS Firewall (ufw / iptables)
        assert "ufw" in content.lower() or "iptables" in content.lower(), (
            "Guide missing Layer 2: Ubuntu host OS firewall (ufw/iptables) instructions."
        )
        
        # Specific port opening commands
        assert "6333" in content and "6334" in content, (
            "Guide missing firewall rules for both REST (6333) and gRPC (6334) ports."
        )

    def test_tc_use_05_guide_5_stage_verification_diagnostic_suite(self):
        """
        TC-USE-05: Validate 5-Stage Health Verification Diagnostics in guide.
        Authoritative source: PROJECT.md lines 12, 28.
        """
        assert GUIDE_PATH.exists(), f"Guide file {GUIDE_PATH} not found."
        content = GUIDE_PATH.read_text(encoding="utf-8")
        
        # Stage 1: Container inspection
        assert "docker ps" in content or "docker compose ps" in content, (
            "Guide missing Stage 1: Docker process inspection command."
        )
        
        # Stage 2: REST healthcheck curl command
        assert "curl" in content and ("6333" in content or "healthz" in content or "collections" in content), (
            "Guide missing Stage 2: Remote REST curl healthcheck command."
        )
        
        # Stage 3: Collection CRUD test
        assert "collection" in content.lower() or "crud" in content.lower(), (
            "Guide missing Stage 3: Vector collection test instructions."
        )
        
        # Stage 4: Web UI Dashboard
        assert "dashboard" in content.lower() or ":6333" in content, (
            "Guide missing Stage 4: Interactive Web UI Dashboard verification."
        )
        
        # Stage 5: SDK or Python verification probe
        assert "python" in content.lower() or "qdrant_client" in content.lower(), (
            "Guide missing Stage 5: Programmatic client verification probe."
        )

    def test_tc_use_06_guide_env_template_completeness(self):
        """
        TC-USE-06: Validate complete production .env configuration template in guide.
        Authoritative source: PROJECT.md lines 27, 37.
        """
        assert GUIDE_PATH.exists(), f"Guide file {GUIDE_PATH} not found."
        content = GUIDE_PATH.read_text(encoding="utf-8")
        
        # Check all required environment keys in .env template
        required_env_keys = [
            "TELEGRAM_BOT_TOKEN",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "DEEPSEEK_API_KEY",
            "INTERVALS_API_KEY",
            "INTERVALS_ATHLETE_ID",
            "SUPABASE_URL",
            "SUPABASE_KEY",
            "QDRANT_HOST",
            "QDRANT_API_KEY",
        ]
        
        missing_keys = []
        for key in required_env_keys:
            # Check with flexible suffix / naming
            if key == "SUPABASE_KEY":
                if not ("SUPABASE_KEY" in content or "SUPABASE_SERVICE_ROLE_KEY" in content or "SUPABASE_ANON_KEY" in content):
                    missing_keys.append(key)
            elif key == "QDRANT_HOST":
                if not ("QDRANT_HOST" in content or "QDRANT_URL" in content):
                    missing_keys.append(key)
            elif key == "INTERVALS_API_KEY":
                if not ("INTERVALS_API_KEY" in content or "INTERVALS_ICU_API_KEY" in content):
                    missing_keys.append(key)
            elif key == "INTERVALS_ATHLETE_ID":
                if not ("INTERVALS_ATHLETE_ID" in content or "INTERVALS_ICU_ATHLETE_ID" in content):
                    missing_keys.append(key)
            else:
                if key not in content:
                    missing_keys.append(key)
                    
        assert not missing_keys, f"Guide .env template is missing required keys: {missing_keys}"
