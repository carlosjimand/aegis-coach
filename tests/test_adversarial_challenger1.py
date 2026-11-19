"""
Aegis Coach — Phase 2 Adversarial Quality & Stress Testing Suite (Challenger 1)
=============================================================================
Author: Challenger 1 (critic, specialist)
Interface Contracts: PROJECT.md lines 1-137, ORIGINAL_REQUEST.md

This test suite executes rigorous empirical stress-testing against Phase 2 deliverables:
1. PDF & Markdown File Integrity & Encoding (Corrupt bytes, UTF-8, Nulls, Form Feeds)
2. Frontmatter YAML Validation & Schema Strictness (PyYAML, types, required keys)
3. Literature Authenticity & Forensic Content Mismatch Detection (Probing for misattributed papers)
4. RAG Embedding Chunking Simulation & Searchability (500-1000 tokens, payload propagation, vocabulary purity)
5. `mvp_next_steps.md` Command & Infrastructure Verification (AST syntax, Docker Compose YAML, Bash integrity, Ports, .env template)
"""

from __future__ import annotations

import ast
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pypdf
import pytest
import yaml

# ==============================================================================
# PATH CONFIGURATION
# ==============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "papers"
PDFS_DIR = DATA_DIR / "pdfs"
MARKDOWN_DIR = DATA_DIR / "markdown"
RAW_MARKDOWN_DIR = DATA_DIR / "raw_markdown"
MANIFEST_PATH = DATA_DIR / "manifest.json"
GUIDE_PATH = PROJECT_ROOT / "mvp_next_steps.md"

REQUIRED_FRONTMATTER_KEYS = {
    "title",
    "authors",
    "year",
    "journal",
    "doi",
    "domain",
    "topics",
    "target_anatomy",
    "key_protocols",
    "evidence_level",
    "ingestion",
}

DOI_REGEX = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Za-z0-9]+$")


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def parse_markdown_with_frontmatter(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """Parse a Markdown file and return its YAML frontmatter dict and raw body."""
    raw_content = file_path.read_text(encoding="utf-8")
    normalized = raw_content.replace("\r\n", "\n")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", normalized, re.DOTALL)
    if not match:
        return {}, normalized
    yaml_text = match.group(1)
    body_text = match.group(2)
    parsed_yaml = yaml.safe_load(yaml_text) or {}
    return parsed_yaml, body_text


def simulate_rag_chunker(
    body: str,
    metadata: Dict[str, Any],
    chunk_word_size: int = 600,
    overlap_words: int = 100,
) -> List[Dict[str, Any]]:
    """Simulate production RAG embedding chunker with metadata propagation."""
    words = body.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i : i + chunk_word_size]
        chunk_text = " ".join(chunk_words)
        chunks.append(
            {
                "chunk_idx": len(chunks),
                "text": chunk_text,
                "word_count": len(chunk_words),
                "metadata": {
                    "title": metadata.get("title"),
                    "authors": metadata.get("authors"),
                    "year": metadata.get("year"),
                    "journal": metadata.get("journal"),
                    "doi": metadata.get("doi"),
                    "domain": metadata.get("domain"),
                    "topics": metadata.get("topics", []),
                    "target_anatomy": metadata.get("target_anatomy", []),
                    "key_protocols": metadata.get("key_protocols", []),
                },
            }
        )
        if i + chunk_word_size >= len(words):
            break
        i += chunk_word_size - overlap_words
    return chunks


# ==============================================================================
# SUITE 1: PDF & MARKDOWN FILE INTEGRITY
# ==============================================================================

class TestSuite1FileIntegrity:
    """Adversarial stress-testing of binary and text file integrity."""

    def test_pdf_binary_integrity_and_magic_bytes(self):
        """Verify that all PDF files have valid PDF magic headers, EOF markers, and non-trivial size."""
        assert PDFS_DIR.exists(), f"PDF directory does not exist at {PDFS_DIR}"
        pdf_files = list(PDFS_DIR.glob("*.pdf"))
        assert len(pdf_files) >= 9, f"Expected at least 9 PDFs, found {len(pdf_files)}"

        for pdf_path in pdf_files:
            raw_bytes = pdf_path.read_bytes()
            assert len(raw_bytes) > 50_000, f"PDF {pdf_path.name} is abnormally small ({len(raw_bytes)} bytes)"
            assert raw_bytes.startswith(b"%PDF-"), f"PDF {pdf_path.name} is missing %PDF- magic header"
            
            # Check EOF marker in the last 2048 bytes
            eof_region = raw_bytes[-2048:]
            assert b"%%EOF" in eof_region, f"PDF {pdf_path.name} missing %%EOF marker (corrupted/truncated download)"

            # Ensure pypdf can parse the document without raising fatal errors
            reader = pypdf.PdfReader(str(pdf_path))
            assert len(reader.pages) > 0, f"PDF {pdf_path.name} contains 0 pages"
            
            # Verify text can be extracted from page 1
            first_page_text = reader.pages[0].extract_text()
            assert first_page_text is not None and len(first_page_text.strip()) > 50, (
                f"PDF {pdf_path.name} page 1 text extraction returned empty or unreadable text"
            )

    def test_markdown_strict_utf8_and_cleanliness(self):
        """Verify that all clean markdown files decode cleanly as UTF-8 without nulls or form-feeds."""
        assert MARKDOWN_DIR.exists(), f"Markdown directory does not exist at {MARKDOWN_DIR}"
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 9, f"Expected at least 9 markdown files, found {len(md_files)}"

        for md_path in md_files:
            raw_bytes = md_path.read_bytes()
            try:
                text = raw_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                pytest.fail(f"File {md_path.name} contains invalid UTF-8 sequences: {e}")

            # Check for corrupt null bytes
            assert "\x00" not in text, f"File {md_path.name} contains forbidden null byte \\x00"

            # Check for unstripped form feed characters
            assert "\x0c" not in text, f"File {md_path.name} contains unstripped form feed \\x0c"

            # Check minimum character count
            assert len(text) > 10_000, f"File {md_path.name} is suspiciously short ({len(text)} chars)"

            # Check that markdown starts with YAML frontmatter delimiter
            assert text.startswith("---"), f"File {md_path.name} does not start with YAML frontmatter '---'"


# ==============================================================================
# SUITE 2: FRONTMATTER YAML VALIDATION & STRICT SCHEMA
# ==============================================================================

class TestSuite2FrontmatterYamlValidation:
    """Strict YAML schema and data-type validation."""

    def test_frontmatter_schema_and_types(self):
        """Validate that all markdown files contain valid YAML frontmatter adhering to PROJECT.md schema."""
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        for md_path in md_files:
            fm, body = parse_markdown_with_frontmatter(md_path)
            assert bool(fm), f"Failed to parse frontmatter in {md_path.name}"

            # Check all required keys exist
            missing_keys = REQUIRED_FRONTMATTER_KEYS - set(fm.keys())
            assert not missing_keys, f"File {md_path.name} missing required frontmatter keys: {missing_keys}"

            # Title
            assert isinstance(fm["title"], str) and len(fm["title"].strip()) > 5, f"Invalid title in {md_path.name}"

            # Authors
            assert isinstance(fm["authors"], list) and len(fm["authors"]) > 0, f"Invalid authors list in {md_path.name}"
            for author in fm["authors"]:
                assert isinstance(author, str) and len(author.strip()) > 2, f"Invalid author entry '{author}' in {md_path.name}"

            # Year
            assert isinstance(fm["year"], int), f"Year in {md_path.name} must be integer, got {type(fm['year'])}"
            assert 1990 <= fm["year"] <= 2026, f"Year {fm['year']} out of plausible range in {md_path.name}"

            # Journal
            assert isinstance(fm["journal"], str) and len(fm["journal"].strip()) > 2, f"Invalid journal in {md_path.name}"

            # DOI
            assert isinstance(fm["doi"], str), f"DOI in {md_path.name} must be string"
            assert DOI_REGEX.match(fm["doi"]), f"DOI '{fm['doi']}' in {md_path.name} does not match standard DOI pattern"

            # Domain
            assert isinstance(fm["domain"], str) and len(fm["domain"].strip()) > 0, f"Invalid domain in {md_path.name}"

            # Topics
            assert isinstance(fm["topics"], list) and len(fm["topics"]) >= 2, f"Topics in {md_path.name} must be list of >= 2 items"
            for t in fm["topics"]:
                assert isinstance(t, str) and len(t) > 0, f"Invalid topic '{t}' in {md_path.name}"

            # Target Anatomy
            assert isinstance(fm["target_anatomy"], list) and len(fm["target_anatomy"]) >= 1, f"Target anatomy in {md_path.name} must be list"

            # Key Protocols
            assert isinstance(fm["key_protocols"], list) and len(fm["key_protocols"]) >= 1, f"Key protocols in {md_path.name} must be list"

            # Evidence Level
            assert isinstance(fm["evidence_level"], str) and len(fm["evidence_level"]) > 0, f"Invalid evidence_level in {md_path.name}"

            # Ingestion sub-dict
            ingestion = fm["ingestion"]
            assert isinstance(ingestion, dict), f"Ingestion metadata in {md_path.name} must be a dict"
            assert "source_file" in ingestion and isinstance(ingestion["source_file"], str)
            assert "engine" in ingestion and isinstance(ingestion["engine"], str)
            assert "cleaned" in ingestion and ingestion["cleaned"] is True


# ==============================================================================
# SUITE 3: FORENSIC LITERATURE AUTHENTICITY & CONTENT INTEGRITY
# ==============================================================================

class TestSuite3LiteratureAuthenticityAndForensicAnomalies:
    """Forensic verification that the actual text corresponds to the claimed scientific paper."""

    def test_forensic_detect_mismatched_medical_papers(self):
        """
        Adversarial forensic check: Detect if any sports medicine paper is contaminated
        with completely unrelated medical domains (pediatric diarrhea, murine bone marrow immunology, Parkinson's dyskinesia).
        """
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        mismatched_papers = []

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            lower_content = content.lower()

            # Check 1: Racecadotril pediatric diarrhea contamination
            if "racecadotril" in lower_content or "acute diarrhoea in children" in lower_content:
                mismatched_papers.append(
                    (
                        md_path.name,
                        "CRITICAL: Contains pediatric diarrhea / Racecadotril systematic review text instead of sports science.",
                    )
                )

            # Check 2: Murine Bone Marrow / RatIgG Immunology contamination
            if "ratigg" in lower_content or "bdbiosciences" in lower_content or "neutrophil granulocytes from murine bone marrow" in lower_content:
                mismatched_papers.append(
                    (
                        md_path.name,
                        "CRITICAL: Contains murine bone marrow immunology / flow cytometry text instead of ultra-trail running fatigue.",
                    )
                )

            # Check 3: Parkinson's Disease / 6-OHDA rat study contamination
            if "6-hydroxydopamine" in lower_content or "parkinson’s rats" in lower_content or "l-dopa-induced dyskinesia" in lower_content:
                mismatched_papers.append(
                    (
                        md_path.name,
                        "CRITICAL: Contains Parkinson's rat model / L-dopa dyskinesia study instead of Achilles tendinopathy rehabilitation.",
                    )
                )

        # In adversarial testing, we explicitly surface any found mismatches
        if mismatched_papers:
            details = "\n".join(f" - {name}: {reason}" for name, reason in mismatched_papers)
            pytest.fail(f"Forensic test detected misattributed/contaminated scientific papers:\n{details}")

    def test_forensic_detect_backwards_text_artifacts(self):
        """
        Detect OCR/PDF conversion artifacts where words are written backwards
        (e.g., 'gniniart' instead of 'training', 'ytisnetni' instead of 'intensity').
        """
        backwards_terms = ["gniniart", "ytisnetni", "emit .tni"]
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        corrupted_files = []

        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8").lower()
            found = [t for t in backwards_terms if t in content]
            if found:
                corrupted_files.append((md_path.name, found))

        if corrupted_files:
            details = "\n".join(f" - {name}: found {terms}" for name, terms in corrupted_files)
            pytest.fail(f"Forensic test detected backwards text artifacts in markdown papers:\n{details}")


# ==============================================================================
# SUITE 4: RAG EMBEDDING CHUNKING SIMULATION & SEARCHABILITY
# ==============================================================================

class TestSuite4RagChunkingSimulationAndSearchability:
    """Stress-test RAG embedding chunking across all papers."""

    def test_rag_chunking_token_quality_and_payload_propagation(self):
        """Verify that RAG chunking produces well-formed chunks with rich payload metadata."""
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        total_chunks = 0

        for md_path in md_files:
            fm, body = parse_markdown_with_frontmatter(md_path)
            chunks = simulate_rag_chunker(body, fm, chunk_word_size=600, overlap_words=100)
            assert len(chunks) >= 3, f"Paper {md_path.name} produced only {len(chunks)} chunks"

            for chunk in chunks:
                total_chunks += 1
                text = chunk["text"]
                metadata = chunk["metadata"]

                # Check word count boundaries
                assert 50 <= chunk["word_count"] <= 800, f"Chunk {chunk['chunk_idx']} in {md_path.name} invalid word count: {chunk['word_count']}"

                # Check character quality: printable ratio >= 98%
                printable_count = sum(1 for ch in text if ch.isprintable() or ch in "\n\t")
                printable_ratio = printable_count / max(len(text), 1)
                assert printable_ratio >= 0.98, f"Chunk {chunk['chunk_idx']} in {md_path.name} low printable ratio: {printable_ratio:.2f}"

                # Check metadata propagation
                assert metadata["title"] == fm["title"]
                assert metadata["doi"] == fm["doi"]
                assert metadata["domain"] == fm["domain"]
                assert isinstance(metadata["topics"], list) and len(metadata["topics"]) > 0

        assert total_chunks >= 100, f"Expected total chunks >= 100 across corpus, got {total_chunks}"

    def test_rag_retrieval_simulation_for_core_clinical_concepts(self):
        """Simulate RAG keyword/semantic retrieval against core sports science protocols."""
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        corpus_chunks = []
        for md_path in md_files:
            fm, body = parse_markdown_with_frontmatter(md_path)
            chunks = simulate_rag_chunker(body, fm, chunk_word_size=500, overlap_words=80)
            corpus_chunks.extend(chunks)

        queries = [
            ("askling", ["extender", "diver", "glider", "hamstring", "l-protocol"]),
            ("polarized", ["80/20", "zone 1", "zone 3", "vo2max", "lactate"]),
            ("tendon", ["continuum", "reactive", "disrepair", "degenerative", "isometric"]),
            ("strength", ["running economy", "1rm", "plyometric", "stiffness"]),
        ]

        for query_tag, keywords in queries:
            matching_chunks = [
                c for c in corpus_chunks
                if any(kw.lower() in c["text"].lower() for kw in keywords)
            ]
            assert len(matching_chunks) > 0, f"Retrieval simulation found 0 chunks matching query domain '{query_tag}'"


# ==============================================================================
# SUITE 5: MVP NEXT STEPS GUIDE COMMAND VERIFICATION
# ==============================================================================

class TestSuite5MvpGuideCommandVerification:
    """Stress-test commands, docker configs, scripts, and security rules in mvp_next_steps.md."""

    def test_guide_presence_and_structure(self):
        """Verify mvp_next_steps.md exists, is non-empty, and covers all required sections."""
        assert GUIDE_PATH.exists(), f"Guide file missing at {GUIDE_PATH}"
        content = GUIDE_PATH.read_text(encoding="utf-8")
        assert len(content) > 30_000, f"Guide file is smaller than expected ({len(content)} chars)"

        # Check required sections
        required_sections = [
            "Section 1: Prerequisites & Architecture Overview",
            "Section 2: Oracle Cloud Infrastructure (OCI) Provisioning",
            "Section 3: Host Setup & Docker Engine V2 Installation",
            "Section 4: Qdrant Vector Database Deployment",
            "Section 5: Dual-Layer Network Security & Firewall Hardening",
            "Section 6: Environment Configuration (`.env`) & 5-Stage Verification Protocol",
        ]
        for section in required_sections:
            assert section in content, f"Guide missing required section: '{section}'"

    def test_guide_python_diagnostic_scripts_syntax(self):
        """Verify that all Python code blocks in mvp_next_steps.md are syntactically valid via ast.parse."""
        content = GUIDE_PATH.read_text(encoding="utf-8")
        code_blocks = re.findall(r"```([a-zA-Z0-9_-]*)\n(.*?)\n```", content, re.DOTALL)
        py_blocks = [block for lang, block in code_blocks if lang.lower() in ["python", "py"]]
        assert len(py_blocks) >= 1, "Expected at least 1 Python code block in guide"

        for idx, py_code in enumerate(py_blocks, 1):
            try:
                tree = ast.parse(py_code)
                assert tree is not None
            except SyntaxError as e:
                pytest.fail(f"Python code block #{idx} in mvp_next_steps.md has syntax error: {e}")

    def test_guide_docker_compose_yaml_syntax_and_security(self):
        """Extract docker-compose block from guide and validate YAML syntax, ports, and volume permissions."""
        content = GUIDE_PATH.read_text(encoding="utf-8")
        # Extract docker-compose yaml inside heredoc
        heredoc_match = re.search(r"cat << 'EOF' > ~/aegis-infra/docker-compose\.yml\n(.*?)\nEOF", content, re.DOTALL)
        assert heredoc_match is not None, "Failed to find docker-compose.yml heredoc block in guide"

        compose_yaml = heredoc_match.group(1)
        try:
            compose_data = yaml.safe_load(compose_yaml)
        except yaml.YAMLError as e:
            pytest.fail(f"Invalid YAML in docker-compose block: {e}")

        assert "services" in compose_data, "docker-compose missing 'services' key"
        assert "qdrant" in compose_data["services"], "docker-compose missing 'qdrant' service"

        qdrant_svc = compose_data["services"]["qdrant"]
        assert "qdrant/qdrant" in qdrant_svc.get("image", ""), "qdrant image missing or incorrect"

        # Check port mappings
        ports = qdrant_svc.get("ports", [])
        assert any("6333:6333" in str(p) for p in ports), "Port 6333 (REST) not mapped in docker-compose"
        assert any("6334:6334" in str(p) for p in ports), "Port 6334 (gRPC) not mapped in docker-compose"

        # Check API key auth env var
        env_vars = qdrant_svc.get("environment", [])
        assert any("QDRANT__SERVICE__API_KEY" in str(env) for env in env_vars), (
            "docker-compose missing QDRANT__SERVICE__API_KEY security enforcement"
        )

    def test_guide_env_template_keys(self):
        """Verify production .env template contains all required API keys and configuration parameters."""
        content = GUIDE_PATH.read_text(encoding="utf-8")
        required_env_vars = [
            "TELEGRAM_BOT_TOKEN",
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "DEEPSEEK_API_KEY",
            "INTERVALS_ICU_API_KEY",
            "INTERVALS_ICU_ATHLETE_ID",
            "SUPABASE_URL",
            "SUPABASE_SERVICE_ROLE_KEY",
            "QDRANT_HOST",
            "QDRANT_GRPC_PORT",
            "QDRANT_API_KEY",
            "QDRANT_COLLECTION_NAME",
        ]

        for var in required_env_vars:
            assert var in content, f".env template in mvp_next_steps.md missing required variable: {var}"
