"""
Aegis Coach — Empirical Adversarial Clinical Protocol & RAG Extraction Stress Test Suite
========================================================================================
Author: Challenger 2 (Phase 2 Clinical Integrity & RAG Stress Testing)
Focus:
1. Clinical Integrity & Paper Authenticity Verification
2. Exact Numerical & Procedural Extraction for Key Scientific Protocols:
   - Seiler / Stöggl 80/20 Lactate & Heart Rate Thresholds
   - Askling Hamstring L-Protocol (Extender, Diver, Glider) & H-Test Clearance
   - Silbernagel 0-5/10 Pain-Monitoring Model & Achilles Rehab Progression
   - Gabbett ACWR Mathematical Formula & Danger Zones (>1.5)
   - Millet Ultra-Trail 9-16 Day Biological Recovery Window & Downhill Ban
3. RAG Semantic Chunking, Retrieval & Hallucination Resistance
4. GFM Table Syntax and Text Truncation Analysis
"""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "papers"
MARKDOWN_DIR = DATA_DIR / "markdown"
MANIFEST_PATH = DATA_DIR / "manifest.json"


def extract_frontmatter_and_body(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    normalized = content.replace("\r\n", "\n")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", normalized, re.DOTALL)
    if not match:
        return None, normalized
    yaml_text = match.group(1)
    body_text = match.group(2)
    try:
        data = yaml.safe_load(yaml_text)
        return (data if isinstance(data, dict) else None), body_text
    except Exception:
        return None, body_text


def simulate_rag_chunking(markdown_body: str, metadata: Dict[str, Any], chunk_size: int = 1200, overlap: int = 200) -> List[Dict[str, Any]]:
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
                })
                chunk_index += 1
                overlap_text = current_chunk[-overlap:] if len(current_chunk) > overlap else ""
                current_chunk = f"{overlap_text}\n\n{p}".strip()
            else:
                chunks.append({
                    "chunk_id": f"{metadata.get('id', 'paper')}_chunk_{chunk_index:03d}",
                    "text": p[:chunk_size],
                    "metadata": metadata,
                    "char_count": len(p[:chunk_size]),
                })
                chunk_index += 1
                current_chunk = ""
    if current_chunk:
        chunks.append({
            "chunk_id": f"{metadata.get('id', 'paper')}_chunk_{chunk_index:03d}",
            "text": current_chunk,
            "metadata": metadata,
            "char_count": len(current_chunk),
        })
    return chunks


# ==============================================================================
# 1. PAPER AUTHENTICITY & DOMAIN INTEGRITY
# ==============================================================================

class TestPaperAuthenticityAndIntegrity:
    """Verify that paper markdown bodies match their frontmatter identity and do not contain foreign medical text."""

    def test_probe_auth_01_body_matches_frontmatter_metadata(self):
        """Probe that body text contains the first author and title subject matter."""
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        assert len(md_files) >= 5, "Missing markdown papers."
        
        mismatches = []
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            fm, body = extract_frontmatter_and_body(content)
            assert fm is not None, f"Missing frontmatter in {md_path.name}"
            
            authors = fm.get("authors", [])
            first_author = authors[0] if authors else ""
            surname = first_author.split()[-1] if first_author else ""
            
            # Author check
            author_found = surname.lower() in body.lower() if surname else False
            
            # Key title words in body (excluding common stopwords)
            title = fm.get("title", "")
            title_words = [w.lower() for w in re.findall(r"\b[a-zA-Z]{4,}\b", title) if w.lower() not in {"with", "than", "from", "that", "this", "their", "have", "more", "into", "training"}]
            matched_title_words = [w for w in title_words if w in body.lower()]
            match_ratio = len(matched_title_words) / len(title_words) if title_words else 0
            
            if not author_found or match_ratio < 0.40:
                mismatches.append({
                    "file": md_path.name,
                    "expected_author": surname,
                    "author_found": author_found,
                    "title_match_ratio": round(match_ratio, 2),
                })
        
        if mismatches:
            pytest.fail(f"Paper body authenticity mismatch in {len(mismatches)} papers: {mismatches}")

    def test_probe_auth_02_absence_of_foreign_domain_text(self):
        """Probe for foreign non-sports medical text (pediatric diarrhea, rat dyskinesia, mouse bone marrow)."""
        md_files = list(MARKDOWN_DIR.glob("*.md"))
        foreign_incursions = []
        
        for md_path in md_files:
            content = md_path.read_text(encoding="utf-8")
            _, body = extract_frontmatter_and_body(content)
            
            body_lower = body.lower()
            findings = []
            if "racecadotril" in body_lower or "diarrhoea in children" in body_lower:
                findings.append("Pediatric Diarrhea (Racecadotril / Gordon et al.)")
            if "6-hydroxydopamine" in body_lower or "l-dopa-induced dyskinesia" in body_lower or ("parkinson" in body_lower and "dyskinesia" in body_lower):
                findings.append("Rat Parkinson / Dyskinesia (Song et al.)")
            if "neutrophil granulocytes from murine bone marrow" in body_lower or "immunomagnetic negative enrichment" in body_lower:
                findings.append("Mouse Bone Marrow Immunology (Hasenberg et al.)")
            
            if findings:
                foreign_incursions.append({
                    "file": md_path.name,
                    "foreign_topics": findings
                })
        
        assert not foreign_incursions, f"Found foreign medical content in sports papers: {foreign_incursions}"


# ==============================================================================
# 2. PROTOCOL 1: POLARIZED 80/20 & THRESHOLDS (SEILER, STOGGL, HAUGEN)
# ==============================================================================

class TestProtocol1Polarized8020:
    """Stress test extraction of Seiler/Stöggl polarized 80/20 rules, lactate, and HR thresholds."""

    def test_probe_pol_01_stoggl_numerical_lactate_and_vo2max(self):
        stoggl_file = MARKDOWN_DIR / "stoggl_sperlich_2014_polarized.md"
        assert stoggl_file.exists(), "Stöggl paper missing."
        content = stoggl_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        
        protocols = " ".join(fm.get("key_protocols", []))
        assert "80/20" in protocols or "Zone 1" in protocols
        assert "<2 mmol/L" in protocols or "<2.0" in protocols or "2-4" in protocols
        
        body_lower = body.lower()
        assert "polarized" in body_lower
        assert "vo2" in body_lower or "vo2max" in body_lower or "vo2peak" in body_lower
        assert "11.7%" in body or "11.7" in body or "+11.7" in body
        assert "4mmol" in body_lower or "4 mmol" in body_lower or "lactate" in body_lower

    def test_probe_pol_02_seiler_3zone_model_hr_and_intervals(self):
        seiler_file = MARKDOWN_DIR / "seiler_tonnessen_2009_polarized.md"
        assert seiler_file.exists(), "Seiler paper missing."
        content = seiler_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        
        protocols = " ".join(fm.get("key_protocols", []))
        assert "Zone 1" in protocols and "Zone 2" in protocols and "Zone 3" in protocols
        assert "<80% HRmax" in protocols or "80%" in protocols
        assert "82-88%" in protocols or "88%" in protocols
        assert "4 x 8 min" in protocols or "4x8" in protocols
        assert "HRV" in protocols or "autonomic" in protocols.lower()

        body_lower = body.lower()
        assert "lactate threshold" in body_lower
        assert "80" in body_lower and "20" in body_lower

    def test_probe_pol_03_haugen_volume_and_tapering_benchmarks(self):
        haugen_file = MARKDOWN_DIR / "haugen_2022_polarized.md"
        assert haugen_file.exists(), "Haugen paper missing."
        content = haugen_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        
        protocols = " ".join(fm.get("key_protocols", []))
        assert "130-190 km/week" in protocols or "130-190" in protocols
        assert "160-220 km/week" in protocols or "160-220" in protocols
        assert "40-60%" in protocols or "tapering" in protocols.lower()
        assert "2000-2500m" in protocols or "altitude" in protocols.lower()


# ==============================================================================
# 3. PROTOCOL 2: ASKLING HAMSTRING L-PROTOCOL & H-TEST (ASKLING 2013)
# ==============================================================================

class TestProtocol2AsklingHamstring:
    """Stress test extraction of Askling L-Protocol lengthening exercises, dosages, and H-Test criteria."""

    def test_probe_askling_01_three_exercises_and_dosage(self):
        askling_file = MARKDOWN_DIR / "askling_2013_l_protocol.md"
        assert askling_file.exists(), "Askling 2013 paper missing."
        content = askling_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        
        protocols = " ".join(fm.get("key_protocols", []))
        assert "The Extender" in protocols and "3x12" in protocols
        assert "The Diver" in protocols and "3x6" in protocols
        assert "The Glider" in protocols and "3x4" in protocols

        body_lower = body.lower()
        assert "extender" in body_lower
        assert "diver" in body_lower
        assert "glider" in body_lower

    def test_probe_askling_02_rtp_timeline_and_h_test_clearance(self):
        askling_file = MARKDOWN_DIR / "askling_2013_l_protocol.md"
        content = askling_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        
        protocols = " ".join(fm.get("key_protocols", []))
        assert "28 days" in protocols
        assert "51 days" in protocols
        assert "H-Test" in protocols
        assert ">=95%" in protocols or "95%" in protocols
        assert "0/10 pain" in protocols or "0/10 insecurity" in protocols

        body_lower = body.lower()
        assert "28" in body_lower and "51" in body_lower
        assert "h-test" in body_lower


# ==============================================================================
# 4. PROTOCOL 3: SILBERNAGEL PAIN-MONITORING & TENDON REHAB
# ==============================================================================

class TestProtocol3SilbernagelTendon:
    """Stress test Silbernagel pain-monitoring scale (0-5/10), 24h response rule, and Achilles/patellar rehab."""

    def test_probe_silbernagel_01_pain_scale_and_24h_recovery_in_corpus(self):
        """Probe that Silbernagel pain scale and 24h rule are extractable from tendinopathy papers."""
        tendon_files = [
            MARKDOWN_DIR / "silbernagel_2015_achilles_rehab.md",
            MARKDOWN_DIR / "cook_2016_tendon_continuum.md",
        ]
        found_in_body = False
        for tf in tendon_files:
            if tf.exists():
                content = tf.read_text(encoding="utf-8")
                _, body = extract_frontmatter_and_body(content)
                if "pain-monitoring" in body.lower() or ("0-5" in body and "tendon" in body.lower()):
                    found_in_body = True
        
        if not found_in_body:
            pytest.fail("Silbernagel pain-monitoring model (0-5/10 scale, 24h response) is NOT present in any tendon paper body text!")

    def test_probe_silbernagel_02_4phase_achilles_progression_in_body(self):
        """Probe that the 4-phase Achilles tendinopathy progression is present in silbernagel_2015_achilles_rehab.md body."""
        silb_file = MARKDOWN_DIR / "silbernagel_2015_achilles_rehab.md"
        assert silb_file.exists(), "Silbernagel paper missing."
        content = silb_file.read_text(encoding="utf-8")
        _, body = extract_frontmatter_and_body(content)
        
        body_lower = body.lower()
        has_phases = (
            "phase 1" in body_lower and
            "phase 2" in body_lower and
            "phase 3" in body_lower and
            "phase 4" in body_lower and
            "heel raise" in body_lower
        )
        assert has_phases, "silbernagel_2015_achilles_rehab.md body lacks 4-phase Achilles tendinopathy progression!"


# ==============================================================================
# 5. PROTOCOL 4: GABBETT ACWR FORMULA & DANGER ZONES (>1.5)
# ==============================================================================

class TestProtocol4GabbettACWR:
    """Stress test Gabbett ACWR formula, sweet spot (0.8-1.3), and danger zone (>1.5)."""

    def test_probe_gabbett_01_acwr_formula_and_danger_zone_in_body(self):
        gabbett_file = MARKDOWN_DIR / "gabbett_2016_acwr.md"
        assert gabbett_file.exists(), "Gabbett paper missing."
        content = gabbett_file.read_text(encoding="utf-8")
        _, body = extract_frontmatter_and_body(content)
        
        body_lower = body.lower()
        has_acwr = (
            "acute:chronic" in body_lower or
            "acute to chronic" in body_lower or
            "acute workload" in body_lower or
            "sweet spot" in body_lower or
            "danger zone" in body_lower
        )
        assert has_acwr, "gabbett_2016_acwr.md body lacks ACWR formula, sweet spot, or danger zone!"


# ==============================================================================
# 6. PROTOCOL 5: MILLET ULTRA-TRAIL 9-16 DAY RECOVERY WINDOW
# ==============================================================================

class TestProtocol5MilletUltraTrail:
    """Stress test Millet ultra-trail neuromuscular fatigue (-35% / -39% MVC) and 9-16 day recovery window."""

    def test_probe_millet_01_neuromuscular_fatigue_and_recovery_window_in_body(self):
        millet_file = MARKDOWN_DIR / "millet_2011_ultra_trail_fatigue.md"
        assert millet_file.exists(), "Millet paper missing."
        content = millet_file.read_text(encoding="utf-8")
        _, body = extract_frontmatter_and_body(content)
        
        body_lower = body.lower()
        has_ultra_fatigue = (
            ("ultra-marathon" in body_lower or "ultra-trail" in body_lower or "utmb" in body_lower) and
            ("knee extensor" in body_lower or "plantar flexor" in body_lower or "mvc" in body_lower) and
            ("recovery" in body_lower or "neuromuscular" in body_lower)
        )
        assert has_ultra_fatigue, "millet_2011_ultra_trail_fatigue.md body lacks ultra-trail fatigue and neuromuscular recovery!"


# ==============================================================================
# 7. RAG RETRIEVAL & HALLUCINATION STRESS TESTS
# ==============================================================================

class TestRAGRetrievalAndHallucinationResistance:
    """Simulate RAG chunking and retrieval to test whether queries return valid sports protocols or hallucinated/irrelevant medical texts."""

    def test_probe_rag_01_silbernagel_rag_retrieval(self):
        """Simulate user asking RAG: 'What is the pain monitoring rule for Achilles tendinopathy?'"""
        silb_file = MARKDOWN_DIR / "silbernagel_2015_achilles_rehab.md"
        content = silb_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        chunks = simulate_rag_chunking(body, fm or {})
        
        # Search chunks for pain monitoring in Achilles tendinopathy
        relevant_chunks = [c for c in chunks if "achilles" in c["text"].lower() and ("pain" in c["text"].lower() or "heel raise" in c["text"].lower())]
        assert len(relevant_chunks) > 0, "RAG failed to retrieve any relevant body chunks for Achilles pain monitoring from Silbernagel!"

    def test_probe_rag_02_gabbett_acwr_rag_retrieval(self):
        """Simulate user asking RAG: 'What is the safe ACWR sweet spot and danger zone threshold?'"""
        gabbett_file = MARKDOWN_DIR / "gabbett_2016_acwr.md"
        content = gabbett_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        chunks = simulate_rag_chunking(body, fm or {})
        
        relevant_chunks = [c for c in chunks if "workload" in c["text"].lower() or "sweet spot" in c["text"].lower() or "injury" in c["text"].lower()]
        # Check if chunks contain actual ACWR formula vs pediatric diarrhea
        sports_acwr_chunks = [c for c in relevant_chunks if "diarrhoea" not in c["text"].lower() and "racecadotril" not in c["text"].lower() and "chronic" in c["text"].lower()]
        assert len(sports_acwr_chunks) > 0, "RAG failed to retrieve legitimate ACWR body chunks from Gabbett (retrieved chunks contain pediatric diarrhea)!"

    def test_probe_rag_03_millet_ultratrail_rag_retrieval(self):
        """Simulate user asking RAG: 'How many days of recovery are needed after a 100-mile ultra-trail?'"""
        millet_file = MARKDOWN_DIR / "millet_2011_ultra_trail_fatigue.md"
        content = millet_file.read_text(encoding="utf-8")
        fm, body = extract_frontmatter_and_body(content)
        chunks = simulate_rag_chunking(body, fm or {})
        
        # Exclude chunk 0 which contains the frontmatter title header
        body_chunks = chunks[1:] if len(chunks) > 1 else chunks
        relevant_chunks = [c for c in body_chunks if ("ultra" in c["text"].lower() or "fatigue" in c["text"].lower() or "recovery" in c["text"].lower()) and "neutrophil" not in c["text"].lower()]
        assert len(relevant_chunks) > 0, "RAG failed to retrieve any legitimate ultra-trail body chunks from Millet (retrieved chunks contain mouse immunology)!"
