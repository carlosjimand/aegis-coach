import json
import re
import yaml
from pathlib import Path

project_root = Path(".").resolve()
data_dir = project_root / "data" / "papers"
md_dir = data_dir / "markdown"
pdf_dir = data_dir / "pdfs"
manifest_path = data_dir / "manifest.json"

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

print(f"Total papers in manifest: {manifest.get('total_papers')}")
print(f"Domains summary: {json.dumps(manifest.get('domains'), indent=2)}")

forbidden_patterns = [
    (r"\bracecadotril\b", "Pediatric Diarrhea / Racecadotril"),
    (r"\bdiarrhoea\s+in\s+children\b", "Pediatric Diarrhea"),
    (r"\b6-hydroxydopamine\b", "Rat Parkinson's / 6-OHDA"),
    (r"\bl-dopa-induced\s+dyskinesia\b", "Rat Parkinson's / Dyskinesia"),
    (r"\bmurine\s+bone\s+marrow\b", "Mouse Immunology"),
    (r"\bratingg\b", "Mouse Immunology"),
    (r"\bflow\s+cytometry\s+analysis\b", "Flow Cytometry"),
]

backwards_patterns = [
    r"\bgniniart\b", r"\bytisnetni\b", r"\bemit \.tni\b", r"\bdeunitnoc\b",
    r"\beulav-p\b", r"\bdnuorgkcab\b", r"\becnatsiser\b", r"\bcirtemoylp\b",
    r"\blavretni\b", r"\bnoitnevretni\b", r"\bselbairav\b", r"\bgninnur\b",
    r"\bhtgnerts\b", r"\btnirps\b", r"\bemulov\b", r"\bdeziralop\b",
]

clinical_verification = {
    "stoggl_sperlich_2014_polarized": [
        (r"polarized", "Polarized concept"),
        (r"threshold|hiit|high intensity", "Comparison groups"),
        (r"vo2|vo\s*2|oxygen uptake|peak velocity", "Performance variables"),
    ],
    "seiler_tonnessen_2009_polarized": [
        (r"zone 1|zone 2|zone 3|<2(\.0)?\s*m[Mm]|<2 mmol", "3-zone model"),
        (r"80/20|80%|80\s*%", "80/20 distribution"),
        (r"4\s*x\s*8|4x8|interval", "4x8 interval dosing"),
        (r"autonomic|hrv|recovery", "Autonomic/HRV recovery"),
    ],
    "haugen_2022_polarized": [
        (r"distance runners|world-class|elite", "Subject cohort"),
        (r"volume|km/week|km|mile", "Volume metrics"),
        (r"taper|exponential", "Tapering protocol"),
        (r"altitude", "Altitude training"),
    ],
    "askling_2013_l_protocol": [
        (r"extender", "The Extender exercise"),
        (r"diver", "The Diver exercise"),
        (r"glider", "The Glider exercise"),
        (r"28\s*days|28(\.1)?\s*days", "28 days RTP"),
        (r"h-test|straight-leg", "Askling H-Test"),
    ],
    "askling_2014_l_protocol_acute": [
        (r"extender", "The Extender exercise"),
        (r"diver", "The Diver exercise"),
        (r"glider", "The Glider exercise"),
        (r"49\s*days|49(\.0)?\s*days", "49 days RTP"),
        (r"biceps femoris|semimembranosus|sprint|stretch", "Differentiation of injury types"),
    ],
    "silbernagel_2007_pain_monitoring": [
        (r"pain-monitoring|pain monitoring", "Pain monitoring model"),
        (r"vas|0-10|5", "VAS scale up to 5"),
        (r"24|morning stiffness|next morning", "24h recovery / morning stiffness"),
        (r"achilles tendinopathy", "Condition"),
    ],
    "silbernagel_2015_achilles_rehab": [
        (r"phase 1|phase 2|phase 3|phase 4", "4-phase rehab"),
        (r"heavy slow resistance|hsr|isometric", "Loading types"),
        (r"plyometric|energy storage|stretch-shortening", "Energy storage / plyometrics"),
        (r"return to sport|clearance", "Sport clearance"),
    ],
    "cook_2016_tendon_continuum": [
        (r"continuum", "Tendon continuum"),
        (r"reactive|disrepair|degenerative", "3 continuum stages"),
        (r"isometric|heavy slow resistance|hsr", "Stage-matched loading"),
    ],
    "gabbett_2016_acwr": [
        (r"acute:chronic|acute chronic|acwr|acute workload", "ACWR concept"),
        (r"0\.8|1\.3|1\.5|danger zone|sweet spot", "ACWR risk zones"),
        (r"injury", "Injury prevention paradox"),
    ],
    "millet_2011_ultra_trail_fatigue": [
        (r"ultra|trail|utmb|mountain", "Ultra-trail context"),
        (r"neuromuscular|mvc|central|peripheral", "Fatigue mechanics"),
        (r"recovery|9.*16|days", "Recovery duration"),
    ],
    "blagrove_2018_strength_runners": [
        (r"strength training|resistance training|plyometric", "Strength interventions"),
        (r"running economy|re", "Running economy improvement"),
        (r"80%|1rm|8\s*weeks|2-3\s*times", "Dosage & protocols"),
    ],
}

print("\n" + "=" * 100)
print(f"{'Paper ID':<35} | {'Words':<6} | {'Forbidden':<10} | {'Backwards':<10} | {'Clinical':<10} | {'Status'}")
print("-" * 100)

all_ok = True

for p in manifest.get("papers", []):
    pid = p["id"]
    md_file = md_dir / f"{pid}.md"
    pdf_file = pdf_dir / f"{pid}.pdf"
    
    if not md_file.exists():
        print(f"{pid:<35} | MISSING MD FILE")
        all_ok = False
        continue
    
    if not pdf_file.exists():
        print(f"{pid:<35} | MISSING PDF FILE")
        all_ok = False
        continue
        
    content = md_file.read_text(encoding="utf-8")
    words = len(content.split())
    
    # Check forbidden
    found_forbidden = []
    for pat, label in forbidden_patterns:
        if re.search(pat, content, re.IGNORECASE):
            found_forbidden.append(label)
            
    # Check backwards
    found_backwards = []
    for pat in backwards_patterns:
        if re.search(pat, content, re.IGNORECASE):
            found_backwards.append(pat)
            
    # Check clinical
    clinical_checks = clinical_verification.get(pid, [])
    missing_clinical = []
    for pat, label in clinical_checks:
        if not re.search(pat, content, re.IGNORECASE):
            missing_clinical.append(label)
            
    forb_status = "CLEAN" if not found_forbidden else f"ERR: {','.join(found_forbidden)}"
    back_status = "CLEAN" if not found_backwards else f"ERR: {len(found_backwards)}"
    clin_status = "OK" if not missing_clinical else f"MISSING: {','.join(missing_clinical)}"
    
    status = "PASS" if (not found_forbidden and not found_backwards and not missing_clinical and words >= 1000) else "FAIL"
    if status == "FAIL":
        all_ok = False
        
    print(f"{pid:<35} | {words:<6} | {forb_status:<10} | {back_status:<10} | {clin_status:<10} | {status}")

print("=" * 100)
print(f"Overall Corpus Clinical & Integrity Status: {'PASS' if all_ok else 'FAIL'}")
