"""
Aegis Coach — Safety & Clinical Guardrails Module
"""

from poc.safety.rules import (
    CLINICAL_CONTRAINDICATIONS,
    SAFE_ALTERNATIVE_PROTOCOLS,
    evaluate_pain_vas,
    get_contraindications_for_pathology,
    get_safe_alternatives_for_pathology,
    is_movement_contraindicated,
)
from poc.safety.red_flags import RedFlagDetector
from poc.safety.injury_guard import SafetyCheckResult, InjuryGuard

__all__ = [
    "CLINICAL_CONTRAINDICATIONS",
    "SAFE_ALTERNATIVE_PROTOCOLS",
    "evaluate_pain_vas",
    "get_contraindications_for_pathology",
    "get_safe_alternatives_for_pathology",
    "is_movement_contraindicated",
    "RedFlagDetector",
    "SafetyCheckResult",
    "InjuryGuard",
]
