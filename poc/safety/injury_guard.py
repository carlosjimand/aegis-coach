"""
Aegis Coach — Biomechanical Injury Guard & Safety Interceptor
=============================================================
Provides deterministic pre-flight query validation and post-flight agent response interception
to prevent prescription of contraindicated exercises, detect overtraining crashes, and enforce clinical safety.
"""

from __future__ import annotations

import re
from typing import List, Tuple, Optional, Dict, Any
from pydantic import BaseModel, Field

from poc.models.athlete import AthleteProfile, RehabPhase
from poc.models.conversation import SafetyViolation, RiskLevel
from poc.safety.rules import (
    CLINICAL_CONTRAINDICATIONS,
    SAFE_ALTERNATIVE_PROTOCOLS,
    evaluate_pain_vas,
    get_contraindications_for_pathology,
    get_safe_alternatives_for_pathology
)
from poc.safety.red_flags import RedFlagDetector


class SafetyCheckResult(BaseModel):
    """Result of a safety evaluation containing diagnostic details and safe alternative recommendations."""

    is_safe: bool = Field(default=True, description="Whether the request/response passed all safety checks.")
    violations: List[SafetyViolation] = Field(
        default_factory=list,
        description="List of specific safety rule violations detected."
    )
    intercepted_content: Optional[str] = Field(
        default=None,
        description="The specific phrase, exercise, or query that triggered interception."
    )
    safe_alternative: Optional[str] = Field(
        default=None,
        description="Evidence-based replacement exercise or protocol."
    )
    escalation_required: bool = Field(
        default=False,
        description="True if an acute medical red flag requires certified physician referral."
    )
    action_taken: str = Field(
        default="ALLOW",
        description="Action applied: 'ALLOW', 'HARD_REJECT', 'SOFT_REJECT', 'OVERRIDE', 'EMERGENCY_LOCKOUT', 'SAFETY_INTERCEPTION'."
    )


class InjuryGuard:
    """
    Deterministic clinical safety guardrail engine.
    Ensures zero contraindicated exercises reach injured athletes and halts training under extreme fatigue or trauma.
    """

    def __init__(self):
        self.red_flag_detector = RedFlagDetector()

    def check_query_safety(self, query: str, athlete: AthleteProfile) -> SafetyCheckResult:
        """
        Performs pre-flight safety analysis on incoming user query against athlete's clinical and physiological profile.
        """
        normalized_query = query.lower().strip()

        # ----------------------------------------------------------------------
        # 1. Medical Red Flags Check (Emergency Lockout)
        # ----------------------------------------------------------------------
        red_flag_violation = self.red_flag_detector.detect_red_flags(query, athlete)
        if red_flag_violation:
            notice = self.red_flag_detector.format_medical_referral_notice(red_flag_violation)
            return SafetyCheckResult(
                is_safe=False,
                violations=[red_flag_violation],
                intercepted_content=red_flag_violation.blocked_content,
                safe_alternative=notice,
                escalation_required=True,
                action_taken="EMERGENCY_LOCKOUT"
            )

        # ----------------------------------------------------------------------
        # 2. Severe Caloric Restriction / Relative Energy Deficiency in Sport (RED-S)
        # ----------------------------------------------------------------------
        caloric_match = re.search(r"\b(\d{3,4})\s*(kcal|calor[ií]as|calorias)\b", normalized_query)
        if caloric_match:
            cals = int(caloric_match.group(1))
            if cals < 1400 and (athlete.weight_kg >= 48 or "20h" in normalized_query or "volumen" in normalized_query or "entreno" in normalized_query):
                safe_cal_target = int(max(1800, athlete.weight_kg * 35))
                violation = SafetyViolation(
                    violation_code="RED_FLAG_ENERGY_DEFICIENCY_LEA",
                    rule_name="Relative Energy Deficiency in Sport (RED-S / Low Energy Availability)",
                    risk_level=RiskLevel.HIGH,
                    blocked_content=f"{cals} kcal/day diet plan under high training volume",
                    safe_alternative=f"Minimum metabolic baseline of {safe_cal_target} kcal/day for active endurance athletes.",
                    rationale="Restricting energy availability below 30 kcal/kg FFM/day impairs endocrine function, bone mineral density, and muscle recovery.",
                    escalation_required=False
                )
                return SafetyCheckResult(
                    is_safe=False,
                    violations=[violation],
                    intercepted_content=query,
                    safe_alternative=f"Tu requerimiento energético mínimo para entrenar con seguridad es de al menos {safe_cal_target} kcal/día.",
                    escalation_required=False,
                    action_taken="SAFETY_INTERCEPTION"
                )

        # ----------------------------------------------------------------------
        # 3. Active Injury Biomechanical Contraindications Check
        # ----------------------------------------------------------------------
        for injury in athlete.active_injuries:
            region = injury.anatomical_region.lower()
            injury_name = injury.injury_name.lower()

            # --- A. Hamstring Pathology (Strain / Proximal Tendinopathy) ---
            if "hamstring" in region or "isquio" in region or "hamstring" in injury_name:
                if re.search(
                    r"\b(100%|a tope|sprint|sprints|sprints m[aá]ximos|cuestas a tope|velocidad m[aá]xima|maximal sprint|salidas de tacos|all-out sprint|hill sprints)\b",
                    normalized_query
                ):
                    alternatives = SAFE_ALTERNATIVE_PROTOCOLS.get("hamstring_proximal", [])
                    alt_text = " + ".join(alternatives[:3]) if alternatives else "Askling L-Protocol + Prone Hamstring Isometrics"
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_ACUTE_HAMSTRING_MAX_VELOCITY",
                        rule_name="Hamstring Strain: High-Velocity Eccentric Elongation Block",
                        risk_level=RiskLevel.HIGH,
                        blocked_content="100% maximal sprints / steep explosive hill sprints",
                        safe_alternative="Submaximal flat progressive strides (capped at 70-75% velocity) + Prone Hamstring Isometrics (30-45° flexion, 5x45s) + Nordic eccentrics (4s tempo).",
                        rationale="Maximal velocity sprinting and steep incline acceleration produce extreme peak eccentric stretch loads at the proximal myotendinous junction, the primary mechanism of recurrence.",
                        escalation_required=False
                    )
                    return SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content="100% sprints / cuestas a tope",
                        safe_alternative="70-75% submaximal flat strides + Nordic curls 3x6 + Hamstring bridges.",
                        escalation_required=False,
                        action_taken="HARD_REJECT"
                    )

            # --- B. Lumbar Spine / Disc Pathology (Herniation / Protrusion) ---
            if "lumbar" in region or "disc" in region or "spine" in region or "columna" in region:
                if re.search(
                    r"\b(1rm|peso muerto convencional|deadlift 1rm|cleans pesados|saltos al caj[oó]n|heavy deadlift|loaded lumbar flexion|sit-ups en banco romano)\b",
                    normalized_query
                ):
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_SPINAL_AXIAL_SHEAR",
                        rule_name="Lumbar Disc Herniation: Maximal Axial Compression & Flexion Shear Block",
                        risk_level=RiskLevel.HIGH,
                        blocked_content="1RM conventional deadlift / high plyometric box jumps / loaded lumbar flexion",
                        safe_alternative="Dr. Stuart McGill Big 3 (Bird-dog, Side plank, Modified curl-up) + High-Handle Trap Bar submaximal (65% 1RM) + Barbell Hip Thrusts.",
                        rationale="Maximal conventional deadlifts under lumbar flexion create intradiscal pressures exceeding 1500N and intense anterior shear forces, directly threatening nerve root impingement or re-herniation.",
                        escalation_required=False
                    )
                    return SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content="1RM conventional deadlift / plyo jumps",
                        safe_alternative="McGill Big 3 + High-Handle Trap Bar Submaximal (65% 1RM, 4x6) + Hip Thrusts.",
                        escalation_required=False,
                        action_taken="HARD_REJECT"
                    )

            # --- C. Patellar Tendon Pathology (Tendinopathy / Jumper's Knee) ---
            if "patellar" in region or "rodilla" in region or "patellar" in injury_name:
                if re.search(
                    r"\b(bajar|bajada|descenso|downhill|sendero t[eé]cnico|1200m de desnivel|desnivel negativo|bajadas agresivas|deep squat jumps)\b",
                    normalized_query
                ):
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_HIGH_ECCENTRIC_IMPACT",
                        rule_name="Patellar Tendinopathy: High Patellofemoral Impact & Shear Dampening",
                        risk_level=RiskLevel.MODERATE,
                        blocked_content="Steep technical downhill running with high vertical drop",
                        safe_alternative="Uphill treadmill hiking (8-12% incline) / low-impact stationary cycling + Spanish Squats isometrics (5x45s).",
                        rationale="Downhill running amplifies peak patellar tendon eccentric braking forces by over 400%, exacerbating collagen disarray during active tendinitis.",
                        escalation_required=False
                    )
                    return SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content="Steep downhill trail run",
                        safe_alternative="Uphill treadmill hiking / low-impact cycling + Spanish Squat isometrics 5x45s.",
                        escalation_required=False,
                        action_taken="SOFT_REJECT"
                    )

            # --- D. Achilles Tendon Pathology (Tendinopathy) ---
            if "achilles" in region or "aquiles" in region or "achilles" in injury_name:
                if re.search(
                    r"\b(cuestas empinadas|cuestas a tope|hill repeats|barefoot|descalzo|saltos pliom[eé]tricos|maximal hops)\b",
                    normalized_query
                ):
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_ACHILLES_PEAK_STRAIN",
                        rule_name="Achilles Tendinopathy: High Cadence Hill & Plyometric Loading Block",
                        risk_level=RiskLevel.HIGH,
                        blocked_content="Aggressive hill repeats / barefoot bounding",
                        safe_alternative="Alfredson eccentric heel drops (3x15 straight & bent knee) + flat aerobic strides with cadence >= 175 spm.",
                        rationale="Steep uphill propulsion places maximal tensile stretch loads (>8x bodyweight) on the Achilles tendon insertion.",
                        escalation_required=False
                    )
                    return SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content="Aggressive hill repeats / barefoot bounding",
                        safe_alternative="Alfredson Eccentric Heel Drops (3x15 straight & bent knee) + Flat running.",
                        escalation_required=False,
                        action_taken="HARD_REJECT"
                    )

        # ----------------------------------------------------------------------
        # 4. Daily Autonomic Crash & Overtraining Fatigue Check
        # ----------------------------------------------------------------------
        if athlete.biometrics and athlete.biometrics.daily_metrics:
            latest_metric = athlete.biometrics.daily_metrics[-1]
            if latest_metric.is_autonomic_crash():
                if re.search(r"\b(series|intervalos|threshold|vo2max|tempo|duro|ca[ñn]a|hard session|tirada larga|wod)\b", normalized_query):
                    violation = SafetyViolation(
                        violation_code="FATIGUE_OVERRIDE_AUTONOMIC_DEPRESSION",
                        rule_name="Autonomic Crash: High-Intensity Interval Override",
                        risk_level=RiskLevel.MODERATE,
                        blocked_content="High intensity VO2max / threshold intervals during autonomic exhaustion",
                        safe_alternative="40-minute Zone 1 active recovery bike ride (HR < 120 bpm) + 15 min mobility & diaphragmatic breathing.",
                        rationale="Severe parasympathetic withdrawal (>40% HRV drop) coupled with sleep deficit drastically reduces tissue repair capacity and elevates acute injury risk by >300%.",
                        escalation_required=False
                    )
                    return SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content="Threshold/VO2max interval session",
                        safe_alternative="40 min Zone 1 active recovery + mobility.",
                        escalation_required=False,
                        action_taken="OVERRIDE"
                    )

        return SafetyCheckResult(is_safe=True, action_taken="ALLOW")

    def intercept_agent_response(
        self,
        response_text: str,
        athlete: AthleteProfile
    ) -> Tuple[str, SafetyCheckResult]:
        """
        Post-flight validation: scans agent-generated output for contraindicated terms and phrases.
        Replaces contraindicated terms with safe alternative tokens and returns sanitized text.
        """
        normalized_response = response_text.lower()
        cleaned_text = response_text
        violations: List[SafetyViolation] = []

        for injury in athlete.active_injuries:
            contra_set = set(injury.contraindicated_movements)
            for c in get_contraindications_for_pathology(injury.anatomical_region):
                contra_set.add(c)

            # Sort descending by length so longer phrases match first
            sorted_contras = sorted(list(contra_set), key=len, reverse=True)
            for contra in sorted_contras:
                if not contra.strip():
                    continue

                contra_variants = {contra, contra.replace("_", " "), contra.replace(" ", "_")}
                for cv in contra_variants:
                    if cv.lower() in normalized_response:
                        alt = "; ".join(injury.safe_alternative_protocols) if injury.safe_alternative_protocols else "Safe alternative isometrics"
                        violation = SafetyViolation(
                            violation_code="POST_FLIGHT_CONTRAINDICATION_INTERCEPTED",
                            rule_name=f"Safety Guardrail: Purged contraindicated term '{cv}'",
                            risk_level=RiskLevel.HIGH,
                            blocked_content=cv,
                            safe_alternative=alt,
                            rationale=f"Agent response contained contraindicated movement pattern '{cv}' matching athlete active pathology ({injury.injury_name})."
                        )
                        violations.append(violation)
                        cleaned_text = re.sub(
                            re.escape(cv),
                            f"[INTERCEPTADO: {violation.safe_alternative}]",
                            cleaned_text,
                            flags=re.IGNORECASE
                        )
                        normalized_response = cleaned_text.lower()

        if violations:
            return cleaned_text, SafetyCheckResult(
                is_safe=False,
                violations=violations,
                intercepted_content=violations[0].blocked_content,
                safe_alternative=violations[0].safe_alternative,
                action_taken="HARD_REJECT"
            )

        return response_text, SafetyCheckResult(is_safe=True, action_taken="ALLOW")
