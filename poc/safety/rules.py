"""
Aegis Coach — Clinical Safety Rules & Biomechanical Contraindications
======================================================================
Defines clinical lookup matrices, movement contraindication tables,
pain threshold policies (Visual Analog Scale), and evidence-based safe alternative protocols.
"""

from __future__ import annotations

from typing import Dict, List, Any, Optional
from poc.models.athlete import RehabPhase


# ==============================================================================
# Clinical Pathology Contraindication Lookup Matrix
# ==============================================================================

# Mapping from canonical anatomical pathology to contraindicated movement patterns
CLINICAL_CONTRAINDICATIONS: Dict[str, List[str]] = {
    "hamstring_proximal": [
        "maximal_velocity_sprint",
        "100% sprint",
        "sprint_max_velocity",
        "cuestas a tope",
        "hill_sprints_100%",
        "nordic_curl_unassisted",
        "straight_leg_deadlift_end_range",
        "ballistic_kicking",
        "end_range_explosive_stretch",
        "sprint",
        "sprints",
        "series de velocidad maxima",
        "salidas de tacos"
    ],
    "hamstring_strain": [
        "maximal_velocity_sprint",
        "100% sprint",
        "sprint_max_velocity",
        "cuestas a tope",
        "hill_sprints_100%",
        "nordic_curl_unassisted",
        "straight_leg_deadlift_end_range",
        "ballistic_kicking",
        "end_range_explosive_stretch",
        "sprint",
        "sprints"
    ],
    "achilles_tendon": [
        "aggressive_hill_running",
        "plyometric_jumping",
        "barefoot_sprinting",
        "maximal_hop_tests",
        "cuestas empinadas",
        "series en cuesta ascendente",
        "saltos pliometricos reactivos",
        "salto a la comba rapido"
    ],
    "achilles_tendinopathy": [
        "aggressive_hill_running",
        "plyometric_jumping",
        "barefoot_sprinting",
        "maximal_hop_tests",
        "cuestas empinadas",
        "series en cuesta ascendente"
    ],
    "patellar_tendon": [
        "steep_downhill_running",
        "bajadas tecnicas pronunciadas",
        "desnivel negativo agresivo",
        "deep_squat_jumps",
        "plyometric_bounding",
        "saltos con flexion profunda de rodilla",
        "descensos rapidos"
    ],
    "patellar_tendinopathy": [
        "steep_downhill_running",
        "bajadas tecnicas pronunciadas",
        "deep_squat_jumps",
        "plyometric_bounding"
    ],
    "lumbar_spine": [
        "1rm_conventional_deadlift",
        "1rm",
        "conventional_deadlift",
        "loaded_lumbar_flexion",
        "plyometric_box_jumps",
        "heavy_good_mornings",
        "heavy_cleans",
        "cleans_pesados",
        "saltos_al_cajon",
        "peso muerto convencional 1rm",
        "sit-ups en banco romano"
    ],
    "lumbar_disc_protrusion": [
        "1rm_conventional_deadlift",
        "1rm",
        "conventional_deadlift",
        "loaded_lumbar_flexion",
        "plyometric_box_jumps",
        "heavy_good_mornings",
        "heavy_cleans",
        "cleans_pesados",
        "saltos_al_cajon"
    ],
    "lumbar_herniation": [
        "1rm_conventional_deadlift",
        "1rm",
        "conventional_deadlift",
        "loaded_lumbar_flexion",
        "plyometric_box_jumps",
        "heavy_good_mornings",
        "heavy_cleans"
    ],
    "plantar_fascia": [
        "barefoot_intervals",
        "steep_hill_bounds",
        "unsupported_plyometrics",
        "series descalzo",
        "saltos reactivos continuos"
    ],
    "plantar_fasciitis": [
        "barefoot_intervals",
        "steep_hill_bounds",
        "unsupported_plyometrics"
    ]
}


# ==============================================================================
# Evidence-Based Safe Alternative Protocols
# ==============================================================================

SAFE_ALTERNATIVE_PROTOCOLS: Dict[str, List[str]] = {
    "hamstring_proximal": [
        "Askling L-Protocol (The Extender, The Diver, The Glider)",
        "Heavy Slow Resistance (HSR) prone leg curls (3x6-8 at 3s concentric / 3s eccentric)",
        "Prone Hamstring Isometrics (30-45° knee flexion, 5x45s holds, RPE 5-6)",
        "Bilateral and Single-leg elevated glute bridges",
        "Nordic Hamstring Curls (assisted, 3x6 with 4s slow eccentric tempo)",
        "Flat submaximal progressive strides capped at 70-75% maximal velocity"
    ],
    "hamstring_strain": [
        "Askling L-Protocol (The Extender, The Diver, The Glider)",
        "Prone Hamstring Isometrics (30-45° knee flexion, 5x45s holds)",
        "Single-leg elevated glute bridges",
        "Flat submaximal progressive strides (capped at 70-75% max velocity)",
        "Nordic Curls assisted (3x6 with 4s eccentric tempo)"
    ],
    "achilles_tendon": [
        "Silbernagel Combined Loading Protocol (pain-monitored)",
        "Alfredson Eccentric Heel Drops: 3x15 straight-knee (gastrocnemius) + 3x15 bent-knee (soleus) twice daily",
        "Heavy Slow Resistance (HSR) seated and standing calf raises (3x6-8, 3s/3s tempo)",
        "Isometric bilateral flat calf raises (5x45s hold at mid-range)",
        "Flat surface endurance runs with strict cadence >= 175 spm to reduce peak Achilles strain"
    ],
    "achilles_tendinopathy": [
        "Alfredson Eccentric Heel Drops: 3x15 straight-knee + 3x15 bent-knee twice daily",
        "Isometric flat calf raises (5x45s holds)",
        "Flat endurance runs with midfoot landing and high cadence (>=175 spm)"
    ],
    "patellar_tendon": [
        "Rio et al. 2015 Spanish Squats Isometrics (5x45s at 60-70° knee flexion with rigid band support)",
        "Isometric single-leg leg press holds at 60° knee flexion (5x45s at 70% MVC)",
        "Heavy Slow Resistance (HSR) leg press & box squats (3x6-8, 3s concentric / 3s eccentric)",
        "Low-impact stationary cycling / uphill treadmill hiking (8-12% incline, 0% downhill shock)"
    ],
    "patellar_tendinopathy": [
        "Spanish Squats Isometrics (5x45s at 60-70° knee flexion)",
        "Isometric leg press holds at 60° knee flexion (5x45s)",
        "Uphill treadmill hiking (8-12% incline) / low-impact cycling"
    ],
    "lumbar_spine": [
        "Dr. Stuart McGill Big 3 Core Stability (Modified Curl-Up, Side Plank, Bird-Dog)",
        "High-Handle Trap Bar Deadlift (Submaximal 65% 1RM, neutral spine, 4x6)",
        "Barbell Hip Thrusts on padded bench (glute isolation without lumbar shear)",
        "Chest-supported dumbbell rows and neutral-spine split squats",
        "Walking and passive decompression"
    ],
    "lumbar_disc_protrusion": [
        "Dr. Stuart McGill Big 3 (Modified Curl-Up, Side Plank, Bird-Dog)",
        "High-Handle Trap Bar Deadlift (Submaximal 65% 1RM, neutral spine, 4x6)",
        "Barbell Hip Thrusts on padded bench",
        "Split squats with dumbbells at sides"
    ],
    "lumbar_herniation": [
        "Dr. Stuart McGill Big 3 (Modified Curl-Up, Side Plank, Bird-Dog)",
        "High-Handle Trap Bar Deadlift (Submaximal 65% 1RM, neutral spine)",
        "Barbell Hip Thrusts on bench"
    ],
    "plantar_fascia": [
        "High-load strength training (Rathleff protocol): Heel raises with towel under toes (3x8-12, 3s/3s)",
        "Plantar fascia specific stretching against wall / manual big toe dorsiflexion",
        "Cushioned neutral road shoes (avoiding barefoot surfaces)",
        "Low-impact cross-training (swimming, cycling, rowing)"
    ],
    "plantar_fasciitis": [
        "Rathleff Protocol: Heel raises with rolled towel under toes (3x8-12)",
        "Manual plantar fascia and calf stretching",
        "Cushioned footwear and low-impact cross-training"
    ],
    "autonomic_crash": [
        "40-minute Zone 1 active recovery stationary bike ride (HR < 120 bpm, low resistance)",
        "15-minute parasympathetic mobility & diaphragmatic box breathing (4s in, 4s hold, 4s out, 4s hold)",
        "Targeted 8.5+ hours sleep and hydration with 500mg electrolyte salts",
        "Postpone high-intensity intervals / threshold sessions until HRV recovers within 15% of 7-day baseline"
    ]
}


# ==============================================================================
# Clinical Pain Threshold Policy (Visual Analog Scale / VAS 0-10)
# ==============================================================================

def evaluate_pain_vas(pain_score: int) -> Dict[str, Any]:
    """
    Evaluates reported pain level on the Visual Analog Scale (VAS 0-10)
    according to sports medicine clinical loading frameworks (Silbernagel et al., Askling et al.).

    - VAS 0-3: Acceptable "Safe Adaptation Zone" provided symptoms settle within 24 hours.
    - VAS 4-6: "Warning / Load Reduction Zone" — requires immediate intensity downgrade to isometrics/HSR.
    - VAS 7-10: "Clinical Red Flag Zone" — hard emergency lockout and certified physician referral.
    """
    if pain_score <= 0:
        return {
            "vas_score": pain_score,
            "category": "ASYMPTOMATIC",
            "is_acceptable": True,
            "requires_load_reduction": False,
            "escalation_required": False,
            "guideline": "No active pain. Full periodized training permitted within progressive overload."
        }
    elif 1 <= pain_score <= 3:
        return {
            "vas_score": pain_score,
            "category": "SAFE_ADAPTATION_ZONE",
            "is_acceptable": True,
            "requires_load_reduction": False,
            "escalation_required": False,
            "guideline": (
                "Mild discomfort (VAS <= 3/10) is clinically acceptable during tendon/muscle rehabilitation, "
                "provided pain does not worsen during the session and fully resolves to baseline within 24 hours."
            )
        }
    elif 4 <= pain_score <= 6:
        return {
            "vas_score": pain_score,
            "category": "ELEVATED_PAIN_LOAD_REDUCTION",
            "is_acceptable": False,
            "requires_load_reduction": True,
            "escalation_required": False,
            "guideline": (
                "Moderate pain (VAS 4-6/10) indicates mechanical overload or tissue irritation. "
                "Immediate intensity downgrade required: cease high-velocity, ballistic, or deep end-range loading. "
                "Substitute with heavy isometrics, low-impact cross-training, and pain-free range of motion."
            )
        }
    else:  # pain_score >= 7
        return {
            "vas_score": pain_score,
            "category": "ACUTE_CLINICAL_RED_FLAG",
            "is_acceptable": False,
            "requires_load_reduction": True,
            "escalation_required": True,
            "guideline": (
                "Severe pain (VAS >= 7/10) indicates potential acute tissue rupture, structural damage, or severe inflammation. "
                "Immediate cessation of all training. Mandatory consultation with a sports medicine physician or orthopedic specialist."
            )
        }


# ==============================================================================
# Helper Functions
# ==============================================================================

def get_contraindications_for_pathology(pathology: str) -> List[str]:
    """Retrieves list of contraindicated movement keywords for a given pathology name or anatomical region."""
    norm = pathology.lower().strip().replace("-", "_").replace(" ", "_")
    for key, contra_list in CLINICAL_CONTRAINDICATIONS.items():
        if key in norm or norm in key:
            return contra_list
    return []


def get_safe_alternatives_for_pathology(pathology: str) -> List[str]:
    """Retrieves evidence-based safe alternative protocols for a given pathology."""
    norm = pathology.lower().strip().replace("-", "_").replace(" ", "_")
    for key, alt_list in SAFE_ALTERNATIVE_PROTOCOLS.items():
        if key in norm or norm in key:
            return alt_list
    return [
        "Controlled low-impact active recovery",
        "Isometric holds in pain-free range (5x45s)",
        "Zone 1 stationary cycling / mobility work"
    ]


def is_movement_contraindicated(movement_text: str, pathology: str) -> bool:
    """Checks if a specific movement text violates contraindications for a pathology."""
    contra_list = get_contraindications_for_pathology(pathology)
    norm_text = movement_text.lower()
    for contra in contra_list:
        if contra.lower() in norm_text:
            return True
    return False
