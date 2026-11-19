#!/usr/bin/env python3
"""
Independent Victory Auditor Forensic Probe for Aegis Coach Phase 2.
Performs exhaustive checks on:
1. PDF Integrity (magic bytes, size, page count, authentic text extraction)
2. Raw Markdown & Clean Markdown files (null bytes, binary corruption, minimum length, frontmatter schema)
3. Manifest.json schema and reference consistency
4. mvp_next_steps.md syntax and section requirements
5. Test assertion authenticity in tests/ directory
"""

import os
import sys
import json
import re
import yaml
from pathlib import Path
import pypdf

PROJECT_ROOT = Path("c:/Users/carlo/OneDrive/Documentos/Proyectos/aegis-coach")
DATA_DIR = PROJECT_ROOT / "data" / "papers"
PDFS_DIR = DATA_DIR / "pdfs"
RAW_MD_DIR = DATA_DIR / "raw_markdown"
CLEAN_MD_DIR = DATA_DIR / "markdown"
MANIFEST_PATH = DATA_DIR / "manifest.json"
GUIDE_PATH = PROJECT_ROOT / "mvp_next_steps.md"
TESTS_DIR = PROJECT_ROOT / "tests"

def check_pdfs():
    print("=== [1/5] PDF FORENSIC AUDIT ===")
    assert PDFS_DIR.exists(), f"PDF dir missing: {PDFS_DIR}"
    pdf_files = list(PDFS_DIR.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files.")
    assert len(pdf_files) >= 5, f"Expected at least 5 PDFs, found {len(pdf_files)}"

    for pdf_path in sorted(pdf_files):
        size = pdf_path.stat().st_size
        with open(pdf_path, "rb") as f:
            header = f.read(10)
        assert header.startswith(b"%PDF"), f"{pdf_path.name} does not have %PDF header!"
        assert size > 10000, f"{pdf_path.name} is suspiciously small: {size} bytes"

        # Check pypdf parsing
        reader = pypdf.PdfReader(str(pdf_path))
        num_pages = len(reader.pages)
        assert num_pages > 0, f"{pdf_path.name} has 0 pages!"
        text_sample = ""
        for p in reader.pages[:3]:
            text_sample += p.extract_text() or ""
        assert len(text_sample.strip()) > 50, f"{pdf_path.name} yielded negligible text ({len(text_sample)} chars)"
        print(f"  [OK] {pdf_path.name}: {size:,} bytes, {num_pages} pages, text_sample={len(text_sample)} chars")

def check_markdown_files():
    print("\n=== [2/5] MARKDOWN QUALITY & INTEGRITY AUDIT ===")
    raw_files = list(RAW_MD_DIR.glob("*.raw.md"))
    clean_files = list(CLEAN_MD_DIR.glob("*.md"))
    print(f"Found {len(raw_files)} raw MD files and {len(clean_files)} clean MD files.")
    assert len(raw_files) >= 5, "Fewer than 5 raw markdown files"
    assert len(clean_files) >= 5, "Fewer than 5 clean markdown files"
    assert len(raw_files) == len(clean_files), "Mismatch between raw and clean markdown count"

    for clean_md in sorted(clean_files):
        content = clean_md.read_text(encoding="utf-8")
        assert "\x00" not in content, f"NULL byte detected in {clean_md.name}!"
        assert "\x0c" not in content, f"Form feed \\x0c detected in {clean_md.name}!"
        assert len(content.strip()) > 1000, f"{clean_md.name} text too short ({len(content)} chars)"

        # Check frontmatter
        assert content.startswith("---"), f"{clean_md.name} does not start with YAML frontmatter!"
        parts = content.split("---", 2)
        assert len(parts) >= 3, f"{clean_md.name} malformed frontmatter delimiters"
        frontmatter_str = parts[1]
        fm = yaml.safe_load(frontmatter_str)
        assert isinstance(fm, dict), f"{clean_md.name} frontmatter is not a dict"
        required_keys = ["title", "authors", "year", "domain", "key_protocols"]
        for k in required_keys:
            assert k in fm, f"Missing key '{k}' in {clean_md.name} frontmatter"
        assert len(fm["key_protocols"]) > 0, f"Empty key_protocols in {clean_md.name}"

        # Check body text length
        body = parts[2].strip()
        assert len(body) > 500, f"{clean_md.name} has insufficient body text"
        print(f"  [OK] {clean_md.name}: {len(content):,} chars, YAML title: '{fm['title'][:40]}...', protocols: {len(fm['key_protocols'])}")

def check_manifest():
    print("\n=== [3/5] MANIFEST SCHEMA AUDIT ===")
    assert MANIFEST_PATH.exists(), "manifest.json missing"
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest.get("version") == "1.0.0", f"Unexpected version {manifest.get('version')}"
    papers = manifest.get("papers", [])
    assert len(papers) >= 5, f"Manifest lists only {len(papers)} papers"
    for p in papers:
        for pkey in ["id", "pdf_path", "raw_md_path", "clean_md_path", "title", "authors", "year", "key_protocols"]:
            assert pkey in p, f"Paper entry {p.get('id')} missing key {pkey}"
        # verify referenced paths exist
        assert (PROJECT_ROOT / p["pdf_path"]).exists(), f"Manifest pdf_path does not exist: {p['pdf_path']}"
        assert (PROJECT_ROOT / p["raw_md_path"]).exists(), f"Manifest raw_md_path does not exist: {p['raw_md_path']}"
        assert (PROJECT_ROOT / p["clean_md_path"]).exists(), f"Manifest clean_md_path does not exist: {p['clean_md_path']}"
    print(f"  [OK] manifest.json contains {len(papers)} valid registered papers with all files present.")

def check_user_guide():
    print("\n=== [4/5] MVP USER ACTION GUIDE AUDIT (mvp_next_steps.md) ===")
    assert GUIDE_PATH.exists(), "mvp_next_steps.md missing at root"
    content = GUIDE_PATH.read_text(encoding="utf-8")
    assert len(content) > 5000, f"mvp_next_steps.md is too short: {len(content)} chars"
    
    # Check essential topics requested in R3
    required_topics = [
        ("Oracle Cloud", "Oracle Cloud Always Free Tier"),
        ("VM.Standard.A1.Flex", "Ampere A1 Flex Shape"),
        ("ARM64", "ARM64 architecture"),
        ("docker-compose", "Docker Compose specification"),
        ("qdrant", "Qdrant Vector Database"),
        ("6333", "REST Port 6333"),
        ("6334", "gRPC Port 6334"),
        ("QDRANT__SERVICE__API_KEY", "API key auth config"),
        ("ufw", "Host UFW firewall"),
        ("Ingress", "OCI Ingress security rules"),
        (".env", "Environment template"),
        ("curl", "Health check curl diagnostics")
    ]
    for pattern, name in required_topics:
        assert re.search(pattern, content, re.IGNORECASE), f"Topic missing in mvp_next_steps.md: {name} (pattern: {pattern})"
        print(f"  [OK] Found topic: {name}")

def check_test_suite_authenticity():
    print("\n=== [5/5] TEST SUITE ASSERTION FORENSICS ===")
    test_files = list(TESTS_DIR.glob("test_*.py"))
    assert len(test_files) >= 5, f"Expected test files, found {len(test_files)}"
    
    total_asserts = 0
    total_test_functions = 0
    suspicious_patterns = 0

    for tf in test_files:
        code = tf.read_text(encoding="utf-8")
        test_funcs = re.findall(r"def\s+(test_\w+)\s*\(", code)
        asserts = re.findall(r"\bassert\b", code)
        
        # Check for facade assertions like `assert True` or `assert 1 == 1`
        trivial_asserts = re.findall(r"assert\s+(True|1\s*==\s*1|True\s*is\s*True)\b", code)
        
        total_asserts += len(asserts)
        total_test_functions += len(test_funcs)
        suspicious_patterns += len(trivial_asserts)

        print(f"  [OK] {tf.name}: {len(test_funcs)} tests, {len(asserts)} assertions, {len(trivial_asserts)} trivial asserts")

    assert suspicious_patterns == 0, f"Found {suspicious_patterns} trivial assertions!"
    assert total_asserts > 100, f"Total assertions {total_asserts} is suspiciously low for comprehensive suite"
    print(f"\nAudit complete: {total_test_functions} test functions, {total_asserts} genuine assertions across {len(test_files)} test modules.")

if __name__ == "__main__":
    try:
        check_pdfs()
        check_markdown_files()
        check_manifest()
        check_user_guide()
        check_test_suite_authenticity()
        print("\n>>> ALL FORENSIC INTEGRITY CHECKS PASSED WITH ZERO VIOLATIONS <<<")
    except Exception as e:
        print(f"\n>>> FORENSIC AUDIT FAILED: {e} <<<")
        sys.exit(1)
