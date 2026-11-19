"""
Aegis Coach — Models Package
=============================
Exposes core domain models for athlete state, injuries, biometrics, conversations,
and execution traces.
"""

from poc.models.athlete import (
    Sex,
    SportDiscipline,
    RehabPhase,
    EvidenceLevel,
    ActivityType,
    InjuryRecord,
    RecoveryMetrics,
    WorkoutLog,
    BiometricState,
    AthleteProfile,
)
from poc.models.conversation import (
    DomainIntent,
    RiskLevel,
    UserQuery,
    SafetyViolation,
    ExecutionTrace,
    AgentResponse,
)

__all__ = [
    "Sex",
    "SportDiscipline",
    "RehabPhase",
    "EvidenceLevel",
    "ActivityType",
    "InjuryRecord",
    "RecoveryMetrics",
    "WorkoutLog",
    "BiometricState",
    "AthleteProfile",
    "DomainIntent",
    "RiskLevel",
    "UserQuery",
    "SafetyViolation",
    "ExecutionTrace",
    "AgentResponse",
]
