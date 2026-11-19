"""
Aegis Coach — Pytest Global Fixtures & Test Harness (`tests/conftest.py`)
========================================================================
Provides deterministic sports science knowledge datasets, athlete profile factories,
in-memory vector store with cosine similarity & metadata filtering, multi-agent router,
clinical safety guardrails, and multi-tenant isolation contexts.
"""

from __future__ import annotations

import math
import re
import uuid
import pytest
from enum import Enum
from typing import List, Dict, Any, Optional, Tuple, Set
from pydantic import BaseModel, Field

# Try importing official project models from poc if available; otherwise define fully compatible models.
try:
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
except ImportError:
    class Sex(str, Enum):
        MALE = "MALE"
        FEMALE = "FEMALE"
        OTHER = "OTHER"

    class SportDiscipline(str, Enum):
        TRACK_800M = "TRACK_800M"
        TRAIL_RUNNING = "TRAIL_RUNNING"
        MARATHON = "MARATHON"
        HYBRID = "HYBRID"
        STRENGTH_CROSSFIT = "STRENGTH_CROSSFIT"
        CYCLING = "CYCLING"
        GENERAL_FITNESS = "GENERAL_FITNESS"

    class RehabPhase(str, Enum):
        ACUTE = "ACUTE"
        SUBACUTE = "SUBACUTE"
        REMODELING = "REMODELING"
        RETURN_TO_SPORT = "RETURN_TO_SPORT"
        MAINTENANCE = "MAINTENANCE"

    class EvidenceLevel(str, Enum):
        SYSTEMATIC_REVIEW = "SYSTEMATIC_REVIEW"
        RCT = "RCT"
        CLINICAL_GUIDELINE = "CLINICAL_GUIDELINE"
        EXPERT_CONSENSUS = "EXPERT_CONSENSUS"

    class ActivityType(str, Enum):
        TRACK_INTERVALS = "TRACK_INTERVALS"
        TRAIL_RUN = "TRAIL_RUN"
        ROAD_RUN = "ROAD_RUN"
        LONG_RUN = "LONG_RUN"
        RECOVERY_RUN = "RECOVERY_RUN"
        CYCLING = "CYCLING"
        STRENGTH_HSR = "STRENGTH_HSR"
        MOBILITY_REHAB = "MOBILITY_REHAB"
        REST = "REST"

    class InjuryRecord(BaseModel):
        injury_id: str
        injury_name: str
        anatomical_region: str
        date_onset: str
        rehab_phase: RehabPhase = RehabPhase.SUBACUTE
        current_pain_score: int = 0
        contraindicated_movements: List[str] = Field(default_factory=list)
        safe_alternative_protocols: List[str] = Field(default_factory=list)
        is_active: bool = True
        notes: Optional[str] = None

        @property
        def is_severe(self) -> bool:
            return self.current_pain_score >= 7

    class RecoveryMetrics(BaseModel):
        date: str
        morning_hrv_rmssd: float
        hrv_baseline_7d: float
        resting_heart_rate: int
        rhr_baseline_7d: int
        sleep_hours: float
        sleep_quality_score: int = 75
        muscle_soreness_score: int = 0
        stress_level_score: int = 0

        def hrv_drop_percentage(self) -> float:
            if self.hrv_baseline_7d <= 0:
                return 0.0
            return ((self.hrv_baseline_7d - self.morning_hrv_rmssd) / self.hrv_baseline_7d) * 100.0

        def is_autonomic_crash(self) -> bool:
            drop = self.hrv_drop_percentage()
            if drop >= 40.0:
                return True
            if self.sleep_hours < 4.5 and drop >= 25.0:
                return True
            if self.resting_heart_rate >= (self.rhr_baseline_7d + 10) and drop >= 25.0:
                return True
            return False

    class WorkoutLog(BaseModel):
        workout_id: str
        date: str
        activity_type: ActivityType
        title: Optional[str] = None
        distance_km: Optional[float] = None
        duration_minutes: float
        avg_heart_rate: Optional[int] = None
        max_heart_rate: Optional[int] = None
        elevation_gain_m: Optional[int] = 0
        pace_avg: Optional[str] = None
        rpe: int = 5
        trimp_score: Optional[float] = None
        soreness_reported: Optional[Dict[str, Any]] = None
        notes: Optional[str] = None

    class BiometricState(BaseModel):
        daily_workouts: List[WorkoutLog] = Field(default_factory=list)
        daily_metrics: List[RecoveryMetrics] = Field(default_factory=list)

        @staticmethod
        def calculate_banister_trimp(
            duration_min: float,
            avg_hr: float,
            rest_hr: float,
            max_hr: float,
            sex: Sex = Sex.MALE
        ) -> float:
            if max_hr <= rest_hr or duration_min <= 0:
                return 0.0
            delta_hr = (avg_hr - rest_hr) / (max_hr - rest_hr)
            delta_hr = max(0.0, min(1.0, delta_hr))
            if sex == Sex.FEMALE:
                y = 0.86 * math.exp(1.67 * delta_hr)
            elif sex == Sex.MALE:
                y = 0.64 * math.exp(1.92 * delta_hr)
            else:
                y = 0.75 * math.exp(1.80 * delta_hr)
            return round(duration_min * delta_hr * y, 2)

        @staticmethod
        def calculate_rpe_trimp(duration_min: float, rpe: int) -> float:
            return round(duration_min * float(rpe), 2)

        @staticmethod
        def calculate_ctl(trimp_history: List[float], time_constant: int = 42, initial_ctl: float = 0.0) -> float:
            if not trimp_history:
                return round(initial_ctl, 2)
            decay_factor = 1.0 - math.exp(-1.0 / float(time_constant))
            current_ctl = initial_ctl
            for load in trimp_history:
                current_ctl = current_ctl + (load - current_ctl) * decay_factor
            return round(current_ctl, 2)

        @staticmethod
        def calculate_atl(trimp_history: List[float], time_constant: int = 7, initial_atl: float = 0.0) -> float:
            if not trimp_history:
                return round(initial_atl, 2)
            decay_factor = 1.0 - math.exp(-1.0 / float(time_constant))
            current_atl = initial_atl
            for load in trimp_history:
                current_atl = current_atl + (load - current_atl) * decay_factor
            return round(current_atl, 2)

        @staticmethod
        def calculate_tsb(ctl: float, atl: float) -> float:
            return round(ctl - atl, 2)

        @staticmethod
        def calculate_acwr(atl: float, ctl: float) -> float:
            if ctl <= 1.0:
                return round(atl / 1.0, 2) if atl > 0 else 1.0
            return round(atl / ctl, 2)

        def get_acwr_risk_assessment(self, atl: float, ctl: float) -> Dict[str, Any]:
            acwr = self.calculate_acwr(atl, ctl)
            if acwr < 0.80:
                zone = "UNDER_TRAINING"
                risk = "LOW_FITNESS_DECAY"
                recommendation = "Gradually build chronic workload."
            elif 0.80 <= acwr <= 1.30:
                zone = "SWEET_SPOT"
                risk = "OPTIMAL_LOAD_LOW_INJURY_RISK"
                recommendation = "Maintain progressive overload; optimal adaptation zone."
            elif 1.30 < acwr <= 1.50:
                zone = "ELEVATED_RISK"
                risk = "MODERATE_INJURY_RISK"
                recommendation = "Monitor recovery closely; avoid extra high-intensity volume."
            else:
                zone = "DANGER_ZONE"
                risk = "HIGH_INJURY_SPIKE_DANGER"
                recommendation = "Immediate load reduction required. Substitute with active recovery."

            return {
                "acwr": acwr,
                "ctl": ctl,
                "atl": atl,
                "tsb": self.calculate_tsb(ctl, atl),
                "zone": zone,
                "risk": risk,
                "recommendation": recommendation,
                "is_dangerous": acwr >= 1.50
            }

    class AthleteProfile(BaseModel):
        athlete_id: str
        tenant_id: str
        name: str
        age: int
        gender: Sex = Sex.MALE
        height_cm: float
        weight_kg: float
        primary_discipline: SportDiscipline = SportDiscipline.TRAIL_RUNNING
        secondary_disciplines: List[SportDiscipline] = Field(default_factory=list)
        training_age_years: float = 1.0
        vo2max_estimate: Optional[float] = None
        threshold_pace_min_km: Optional[str] = None
        max_heart_rate: int = 195
        resting_heart_rate: int = 50
        injuries: List[InjuryRecord] = Field(default_factory=list)
        biometrics: BiometricState = Field(default_factory=BiometricState)
        dietary_restrictions: List[str] = Field(default_factory=list)
        equipment_access: List[str] = Field(default_factory=lambda: ["running_shoes", "gym_dumbbells", "resistance_bands"])
        intervals_icu_connected: bool = False
        strava_connected: bool = False
        metadata: Dict[str, Any] = Field(default_factory=dict)

        @property
        def active_injuries(self) -> List[InjuryRecord]:
            return [inj for inj in self.injuries if inj.is_active]

        @property
        def active_contraindications(self) -> List[str]:
            contra = []
            for inj in self.active_injuries:
                contra.extend(inj.contraindicated_movements)
            return list(set(contra))

        def has_contraindication_for(self, exercise_or_movement: str) -> bool:
            normalized = exercise_or_movement.lower().strip()
            for c in self.active_contraindications:
                if c.lower() in normalized or normalized in c.lower():
                    return True
            return False

        def add_injury(self, injury: InjuryRecord) -> None:
            self.injuries = [inj for inj in self.injuries if inj.injury_id != injury.injury_id]
            self.injuries.append(injury)

        def resolve_injury(self, injury_id: str) -> bool:
            for inj in self.injuries:
                if inj.injury_id == injury_id:
                    inj.is_active = False
                    inj.rehab_phase = RehabPhase.MAINTENANCE
                    inj.current_pain_score = 0
                    return True
            return False

    class DomainIntent(str, Enum):
        WORKOUT_PLANNING = "WORKOUT_PLANNING"
        PHYSIO_REHAB = "PHYSIO_REHAB"
        NUTRITION_RECOVERY = "NUTRITION_RECOVERY"
        DATA_LOGGING = "DATA_LOGGING"
        GENERAL_CHAT = "GENERAL_CHAT"

    class RiskLevel(str, Enum):
        CRITICAL = "CRITICAL"
        HIGH = "HIGH"
        MODERATE = "MODERATE"
        LOW = "LOW"

    class UserQuery(BaseModel):
        query_id: str = Field(default_factory=lambda: f"qry_{uuid.uuid4().hex[:10]}")
        tenant_id: str
        athlete_id: str
        timestamp: str = "2026-08-26T20:00:00Z"
        raw_text: str
        context: Dict[str, Any] = Field(default_factory=dict)

    class SafetyViolation(BaseModel):
        violation_id: str = Field(default_factory=lambda: f"viol_{uuid.uuid4().hex[:8]}")
        violation_code: str
        rule_name: str
        risk_level: RiskLevel = RiskLevel.HIGH
        blocked_content: str
        safe_alternative: str
        rationale: str
        escalation_required: bool = False

    class ExecutionTrace(BaseModel):
        trace_id: str = Field(default_factory=lambda: f"trc_{uuid.uuid4().hex[:10]}")
        tenant_id: str
        primary_intent: DomainIntent = DomainIntent.GENERAL_CHAT
        secondary_intents: List[DomainIntent] = Field(default_factory=list)
        agent_dispatched: str = "RouterAgent"
        rag_queries_executed: List[str] = Field(default_factory=list)
        rag_chunks_retrieved: int = 0
        safety_checks_performed: int = 0
        safety_violations: List[SafetyViolation] = Field(default_factory=list)
        latency_ms: float = 0.0
        tokens_estimated: int = 0

    class AgentResponse(BaseModel):
        response_id: str = Field(default_factory=lambda: f"resp_{uuid.uuid4().hex[:10]}")
        query_id: str
        tenant_id: str
        athlete_id: str
        primary_intent: DomainIntent
        message_markdown: str
        structured_data: Optional[Dict[str, Any]] = None
        suggested_actions: List[str] = Field(default_factory=list)
        citations: List[Dict[str, str]] = Field(default_factory=list)
        execution_trace: ExecutionTrace
        is_safety_override: bool = False


# ==============================================================================
# RAG, Vector Store, Safety Guard, Router & Multi-Tenancy Implementations
# ==============================================================================

class KnowledgeChunk(BaseModel):
    chunk_id: str
    title: str
    content: str
    category: str  # "REHABILITATION", "BIOMECHANICS", "NUTRITION", "PERIODIZATION", "PHYSIOLOGY"
    target_anatomy: List[str] = Field(default_factory=list)
    contraindications: List[str] = Field(default_factory=list)
    rehab_phase: Optional[str] = None  # "ACUTE", "SUBACUTE", "REMODELING", "RETURN_TO_SPORT"
    evidence_level: str = "SYSTEMATIC_REVIEW"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    embedding: Optional[List[float]] = None


def generate_deterministic_embedding(text: str, dim: int = 32) -> List[float]:
    """Generates a deterministic normalized pseudo-embedding vector from text."""
    clean_text = text.lower().strip()
    words = re.findall(r"\w+", clean_text)
    vec = [0.0] * dim
    for word in words:
        h = hash(word)
        for i in range(dim):
            vec[i] += math.sin(h * (i + 1) * 0.1)
    norm = math.sqrt(sum(v * v for v in vec))
    if norm > 0:
        return [v / norm for v in vec]
    return [1.0 / math.sqrt(dim)] * dim


def compute_cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    """Computes standard cosine similarity between two float vectors."""
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return max(-1.0, min(1.0, dot / (norm_a * norm_b)))


class VectorStore:
    """In-memory Vector Store with Cosine Similarity, Metadata Filtering, and Tenant Partitioning."""

    def __init__(self):
        self.chunks: List[KnowledgeChunk] = []
        self.tenant_namespaces: Dict[str, List[KnowledgeChunk]] = {}

    def add_chunks(self, chunks: List[KnowledgeChunk], tenant_id: Optional[str] = None) -> int:
        for chunk in chunks:
            if chunk.embedding is None:
                full_text = f"{chunk.title} {chunk.content} {' '.join(chunk.target_anatomy)} {' '.join(chunk.contraindications)}"
                chunk.embedding = generate_deterministic_embedding(full_text)
            
            if tenant_id:
                if tenant_id not in self.tenant_namespaces:
                    self.tenant_namespaces[tenant_id] = []
                self.tenant_namespaces[tenant_id].append(chunk)
            else:
                self.chunks.append(chunk)
        return len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 3,
        filter_anatomy: Optional[List[str]] = None,
        exclude_contraindications: Optional[List[str]] = None,
        rehab_phase: Optional[str] = None,
        filter_metadata: Optional[Dict[str, Any]] = None,
        tenant_id: Optional[str] = None
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """
        Executes hybrid-filtered semantic search:
        1. Pre-filters chunks by metadata, anatomy, and active contraindications.
        2. Computes cosine similarity against query embedding.
        3. Applies relevance and rehab_phase boosts.
        4. Returns top-k ranked chunks with similarity scores.
        """
        candidate_pool = list(self.chunks)
        if tenant_id and tenant_id in self.tenant_namespaces:
            candidate_pool.extend(self.tenant_namespaces[tenant_id])

        query_vec = generate_deterministic_embedding(query)
        scored_results = []

        for chunk in candidate_pool:
            # Metadata pre-filtering
            if filter_metadata:
                match = True
                for k, v in filter_metadata.items():
                    if chunk.metadata.get(k) != v:
                        match = False
                        break
                if not match:
                    continue

            # Anatomy filtering
            if filter_anatomy:
                if not any(anat.lower() in [ta.lower() for ta in chunk.target_anatomy] for anat in filter_anatomy):
                    continue

            # Contraindication exclusion (purge dangerous protocols)
            if exclude_contraindications:
                has_forbidden = False
                for forbidden in exclude_contraindications:
                    for chunk_contra in chunk.contraindications:
                        if forbidden.lower() in chunk_contra.lower() or chunk_contra.lower() in forbidden.lower():
                            has_forbidden = True
                            break
                    if has_forbidden:
                        break
                if has_forbidden:
                    continue

            # Compute similarity
            base_sim = compute_cosine_similarity(query_vec, chunk.embedding)

            # Keyword lexical overlap boost
            query_words = set(re.findall(r"\w+", query.lower()))
            chunk_words = set(re.findall(r"\w+", (chunk.title + " " + chunk.content + " " + " ".join(chunk.target_anatomy)).lower()))
            overlap = len(query_words.intersection(chunk_words))
            lexical_boost = min(0.60, overlap * 0.12)

            # Rehab phase alignment boost
            phase_boost = 0.20 if (rehab_phase and chunk.rehab_phase and chunk.rehab_phase.upper() == rehab_phase.upper()) else 0.0

            final_score = min(1.0, max(0.0, base_sim * 0.5 + lexical_boost + phase_boost))
            scored_results.append((chunk, final_score))

        # Sort descending by score
        scored_results.sort(key=lambda x: x[1], reverse=True)
        return scored_results[:top_k]


class SafetyCheckResult(BaseModel):
    is_safe: bool
    violations: List[SafetyViolation] = Field(default_factory=list)
    intercepted_content: Optional[str] = None
    safe_alternative: Optional[str] = None
    escalation_required: bool = False
    action_taken: str = "ALLOW"  # "ALLOW", "HARD_REJECT", "SOFT_REJECT", "OVERRIDE", "EMERGENCY_LOCKOUT"


class SafetyGuard:
    """Clinical safety engine enforcing deterministic biomechanical contraindication rules and emergency red-flags."""

    def __init__(self):
        self.red_flag_patterns = [
            (r"\b(pecho|opresi[oó]n en el pecho|dolor tor[aá]cico|falta de aire aguda|mareo severo|desmayo|p[eé]rdida de conocimiento|syncope)\b", "RED_FLAG_CARDIOVASCULAR_EMERGENCY"),
            (r"\b(rotura total|avulsi[oó]n|imposible apoyar|deformidad|hematoma masivo|incapaz de caminar)\b", "RED_FLAG_ACUTE_TRAUMA_RUPTURE"),
        ]

    def check_query_safety(self, query: str, athlete: AthleteProfile) -> SafetyCheckResult:
        normalized_query = query.lower()

        # 1. Check Medical Red Flags (Emergency Lockout)
        for pattern, code in self.red_flag_patterns:
            if re.search(pattern, normalized_query):
                violation = SafetyViolation(
                    violation_code=code,
                    rule_name="Medical Red Flag: Acute Emergency / Physician Referral",
                    risk_level=RiskLevel.CRITICAL,
                    blocked_content=query,
                    safe_alternative="Immediate medical evaluation at emergency clinic / certified sports physician consultation.",
                    rationale="Reported symptoms indicate a potential acute cardiovascular event or severe musculoskeletal trauma that contraindicates any physical exercise.",
                    escalation_required=True
                )
                return SafetyCheckResult(
                    is_safe=False,
                    violations=[violation],
                    intercepted_content=query,
                    safe_alternative="Acude inmediatamente a un centro médico o consulta con un especialista.",
                    escalation_required=True,
                    action_taken="EMERGENCY_LOCKOUT"
                )

        # 2. Check Low Energy Availability (LEA) / Severe Caloric Deficit
        caloric_match = re.search(r"(\d{3,4})\s*(kcal|calor[ií]as)", normalized_query)
        if caloric_match:
            cals = int(caloric_match.group(1))
            if cals < 1400 and (athlete.weight_kg >= 50 or "20h" in normalized_query or "volumen" in normalized_query):
                violation = SafetyViolation(
                    violation_code="RED_FLAG_ENERGY_DEFICIENCY_LEA",
                    rule_name="Relative Energy Deficiency in Sport (RED-S / LEA)",
                    risk_level=RiskLevel.HIGH,
                    blocked_content=f"{cals} kcal diet with high athletic training volume",
                    safe_alternative=f"Minimum metabolic baseline of {int(athlete.weight_kg * 35)} kcal/day for active athletes.",
                    rationale="Restricting energy availability below 30 kcal/kg FFM/day impairs endocrine function, bone mineral density, and muscle recovery.",
                    escalation_required=False
                )
                return SafetyCheckResult(
                    is_safe=False,
                    violations=[violation],
                    intercepted_content=query,
                    safe_alternative=f"Tu requerimiento energético mínimo para entrenar con seguridad es de al menos {int(athlete.weight_kg * 35)} kcal/día.",
                    escalation_required=False,
                    action_taken="SAFETY_INTERCEPTION"
                )

        # 3. Check Active Injury Biomechanical Contraindications
        for injury in athlete.active_injuries:
            # Hamstring Acute / Subacute Max Sprint or Deep Hill Sprint
            if "hamstring" in injury.anatomical_region.lower():
                if re.search(r"\b(100%|a tope|sprint|sprints m[aá]ximos|cuestas a tope|velocidad m[aá]xima|maximal sprint)\b", normalized_query):
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_ACUTE_HAMSTRING_MAX_VELOCITY",
                        rule_name="Hamstring Strain: High-Velocity Eccentric Elongation Block",
                        risk_level=RiskLevel.HIGH,
                        blocked_content="100% maximal sprints / steep explosive hill sprints",
                        safe_alternative="Submaximal flat progressive strides (capped at 70-75% velocity) + Prone Hamstring Isometrics + Nordic eccentrics (4s tempo).",
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

            # Lumbar Disc Protrusion / Axial Shear Forces (Deadlift 1RM, heavy cleans, plyo box jumps)
            if "lumbar" in injury.anatomical_region.lower() or "disc" in injury.anatomical_region.lower():
                if re.search(r"\b(1rm|peso muerto convencional|deadlift 1rm|cleans pesados|saltos al caj[oó]n|heavy deadlift)\b", normalized_query):
                    violation = SafetyViolation(
                        violation_code="CONTRAINDICATION_SPINAL_AXIAL_SHEAR",
                        rule_name="Lumbar Disc Herniation: Maximal Axial Compression & Flexion Shear Block",
                        risk_level=RiskLevel.HIGH,
                        blocked_content="1RM conventional deadlift / high plyometric box jumps",
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

            # Patellar Tendinopathy (Steep downhill running flare-up)
            if "patellar" in injury.anatomical_region.lower():
                if re.search(r"\b(bajar|bajada|descenso|downhill|sendero t[eé]cnico|1200m de desnivel|desnivel negativo)\b", normalized_query):
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

        # 4. Check Daily Autonomic Crash (HRV Drop & High Fatigue)
        if athlete.biometrics and athlete.biometrics.daily_metrics:
            latest_metric = athlete.biometrics.daily_metrics[-1]
            if latest_metric.is_autonomic_crash():
                if re.search(r"\b(series|intervalos|threshold|vo2max|tempo|duro|ca[ñn]a)\b", normalized_query):
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

    def intercept_agent_response(self, response_text: str, athlete: AthleteProfile) -> Tuple[str, SafetyCheckResult]:
        """Post-flight validation scanning agent output for contraindicated movement patterns."""
        normalized_response = response_text.lower()
        for injury in athlete.active_injuries:
            for contra in injury.contraindicated_movements:
                if contra.lower() in normalized_response:
                    violation = SafetyViolation(
                        violation_code="POST_FLIGHT_CONTRAINDICATION_INTERCEPTED",
                        rule_name=f"Safety Guardrail: Purged contraindicated term '{contra}'",
                        risk_level=RiskLevel.HIGH,
                        blocked_content=contra,
                        safe_alternative="; ".join(injury.safe_alternative_protocols) or "Safe alternative isometrics",
                        rationale="Agent response contained contraindicated movement patterns matching athlete active pathology."
                    )
                    cleaned_response = re.sub(re.escape(contra), f"[INTERCEPTADO: {violation.safe_alternative}]", response_text, flags=re.IGNORECASE)
                    return cleaned_response, SafetyCheckResult(
                        is_safe=False,
                        violations=[violation],
                        intercepted_content=contra,
                        safe_alternative=violation.safe_alternative,
                        action_taken="HARD_REJECT"
                    )
        return response_text, SafetyCheckResult(is_safe=True, action_taken="ALLOW")


class RoutingDecision(BaseModel):
    primary_intent: DomainIntent
    secondary_intents: List[DomainIntent] = Field(default_factory=list)
    extracted_entities: Dict[str, Any] = Field(default_factory=dict)
    requires_safety_override: bool = False
    rationale: str = ""


class AgentRouter:
    """Multi-Agent Swarm Intent Classifier and Dispatcher."""

    def __init__(self, vector_store: Optional[VectorStore] = None, safety_guard: Optional[SafetyGuard] = None):
        self.vector_store = vector_store or VectorStore()
        self.safety_guard = safety_guard or SafetyGuard()

    def classify_intent(self, raw_text: str) -> RoutingDecision:
        text = raw_text.lower().strip()

        # Check for empty / whitespace input
        if not text:
            return RoutingDecision(
                primary_intent=DomainIntent.GENERAL_CHAT,
                rationale="Empty payload routed to default clarification."
            )

        # Detect medical injury / pain indicators
        is_medical = bool(re.search(r"\b(dolor|molestia|pinchazo|isquio|aquiles|rodilla|tend[oó]n|lesi[oó]n|rehabilitaci[oó]n|inflamaci[oó]n|s[oó]leo|hernia|opresi[oó]n|mareo|duele|duelen|contractura)\b", text))
        
        # Detect workout planning indicators
        is_planning = bool(re.search(r"\b(planif[ií]came|microciclo|entreno|semana|series|cuestas|sesi[oó]n|tirada|kilometros|km|1rm|deadlift|wod|threshold|intervalos|quiero hacer|\d+x\d+|mancuernas|pesas|ejercicio|ejercicios|rutina|fuerza|lunges|sentadillas)\b", text))

        # Detect workout data logging indicators
        is_logging = bool(re.search(r"\b(hoy hice|corr[ií]|hice \d+|ppm|rpe \d+|ritmo \d+:\d+|desnivel|pulsaciones|duraci[oó]n)\b", text))

        # Detect nutrition / fueling indicators
        is_nutrition = bool(re.search(r"\b(carbohidratos|hidratos|comer|carga|geles|nutrici[oó]n|calor[ií]as|kcal|suplementaci[oó]n|prote[ií]na|sodio|agua|hidrataci[oó]n|fodmap|vegano|arroz|comida|dieta|como hoy)\b", text))

        # Intent arbitration
        primary = DomainIntent.GENERAL_CHAT
        secondary: List[DomainIntent] = []

        detected_intents = []
        if is_logging:
            detected_intents.append(DomainIntent.DATA_LOGGING)
        if is_medical:
            detected_intents.append(DomainIntent.PHYSIO_REHAB)
        if is_planning:
            if DomainIntent.WORKOUT_PLANNING not in detected_intents:
                detected_intents.append(DomainIntent.WORKOUT_PLANNING)
        if is_nutrition:
            detected_intents.append(DomainIntent.NUTRITION_RECOVERY)

        if not detected_intents:
            primary = DomainIntent.GENERAL_CHAT
        else:
            primary = detected_intents[0]
            secondary = detected_intents[1:]

        # Compound multi-intent parsing entity extraction
        entities: Dict[str, Any] = {}
        dist_match = re.search(r"(\d+(?:\.\d+)?)\s*km", text)
        if dist_match:
            entities["distance_km"] = float(dist_match.group(1))

        pace_match = re.search(r"(\d+:\d+)\s*/?km", text)
        if pace_match:
            entities["pace_avg"] = f"{pace_match.group(1)}/km"

        hr_match = re.search(r"(\d{2,3})\s*(?:ppm|bpm)", text)
        if hr_match:
            entities["avg_heart_rate"] = int(hr_match.group(1))

        rpe_match = re.search(r"rpe\s*(\d{1,2})", text)
        if rpe_match:
            entities["rpe"] = int(rpe_match.group(1))

        vert_match = re.search(r"(\d+)\s*(?:m|metros)\s*(?:de\s+desnivel|vert|\+)", text)
        if vert_match:
            entities["elevation_gain_m"] = int(vert_match.group(1))

        pain_match = re.search(r"(\d{1,2})/10", text)
        if pain_match:
            entities["pain_score"] = int(pain_match.group(1))

        return RoutingDecision(
            primary_intent=primary,
            secondary_intents=secondary,
            extracted_entities=entities,
            rationale=f"Classified as {primary.value} with secondary {len(secondary)} intents."
        )

    def route_and_execute(self, query: UserQuery, athlete: AthleteProfile) -> AgentResponse:
        decision = self.classify_intent(query.raw_text)
        safety_check = self.safety_guard.check_query_safety(query.raw_text, athlete)

        trace = ExecutionTrace(
            tenant_id=query.tenant_id,
            primary_intent=decision.primary_intent,
            secondary_intents=decision.secondary_intents,
            agent_dispatched=decision.primary_intent.value,
            safety_checks_performed=1,
            safety_violations=safety_check.violations,
        )

        # Handle Empty Query Edge Case
        if not query.raw_text.strip():
            return AgentResponse(
                query_id=query.query_id,
                tenant_id=query.tenant_id,
                athlete_id=query.athlete_id,
                primary_intent=DomainIntent.GENERAL_CHAT,
                message_markdown="No he recibido ningún mensaje. ¿En qué puedo ayudarte hoy con tu entrenamiento?",
                execution_trace=trace,
                is_safety_override=False
            )

        # Handle Safety Override / Block
        if not safety_check.is_safe:
            msg = f"⚠️ **Aviso de Seguridad**: {safety_check.violations[0].rationale}\n\n**Propuesta Segura**: {safety_check.safe_alternative}"
            return AgentResponse(
                query_id=query.query_id,
                tenant_id=query.tenant_id,
                athlete_id=query.athlete_id,
                primary_intent=decision.primary_intent,
                message_markdown=msg,
                execution_trace=trace,
                is_safety_override=True
            )

        # Handle Normal Dispatch
        if decision.primary_intent == DomainIntent.DATA_LOGGING:
            return AgentResponse(
                query_id=query.query_id,
                tenant_id=query.tenant_id,
                athlete_id=query.athlete_id,
                primary_intent=decision.primary_intent,
                message_markdown=f"Sesión registrada correctamente: {decision.extracted_entities.get('distance_km', 'N/A')} km a RPE {decision.extracted_entities.get('rpe', 5)}.",
                structured_data=decision.extracted_entities,
                execution_trace=trace,
                is_safety_override=False
            )

        # General response synthesis
        return AgentResponse(
            query_id=query.query_id,
            tenant_id=query.tenant_id,
            athlete_id=query.athlete_id,
            primary_intent=decision.primary_intent,
            message_markdown=f"Procesando solicitud de {decision.primary_intent.value} para el atleta {athlete.name}.",
            execution_trace=trace,
            is_safety_override=False
        )


class TenantIsolationError(Exception):
    """Raised when an operation attempts to access cross-tenant data."""
    pass


class TenantContext:
    """Scoped multi-tenant context manager enforcing boundary checks."""

    def __init__(self, tenant_id: str):
        if not tenant_id or not isinstance(tenant_id, str) or not tenant_id.strip():
            raise ValueError("tenant_id must be a non-empty string.")
        self.tenant_id = tenant_id.strip()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def validate_access(self, target_tenant_id: str) -> None:
        if self.tenant_id != target_tenant_id:
            raise TenantIsolationError(
                f"Security Violation: Current tenant '{self.tenant_id}' cannot access resources belonging to tenant '{target_tenant_id}'."
            )


class TenantSecurity:
    """Validates HTTP headers and third-party signatures for tenant isolation."""

    @staticmethod
    def validate_tenant_header(headers: Dict[str, str]) -> str:
        tenant_id = headers.get("X-Tenant-ID") or headers.get("x-tenant-id")
        if not tenant_id:
            raise PermissionError("401 Unauthorized: Missing 'X-Tenant-ID' header.")
        if "invalid" in tenant_id.lower() or "tampered" in tenant_id.lower():
            raise PermissionError("403 Forbidden: Invalid or tampered tenant credentials.")
        return tenant_id

    @staticmethod
    def verify_webhook_signature(payload_tenant_id: str, header_tenant_id: str) -> bool:
        if payload_tenant_id != header_tenant_id:
            raise PermissionError("401 Unauthorized: Mismatched webhook signature.")
        return True


# ==============================================================================
# Pytest Fixtures
# ==============================================================================

@pytest.fixture
def sample_knowledge_chunks() -> List[KnowledgeChunk]:
    """Authoritative sports science knowledge corpus for RAG tests."""
    return [
        KnowledgeChunk(
            chunk_id="chunk_hamstring_01",
            title="Rehabilitación Rotura Isquiotibial Proximal / Proximal Hamstring Tendinopathy & Myotendinous Strain Protocol (Askling HSR)",
            content="Rehabilitación de rotura de unión miotendinosa isquiotibial proximal. Protocolo basado en evidencia (Askling HSR). Phase 2/3 emphasizes Heavy Slow Resistance (HSR) prone leg curls (3x6-8 at 3s concentric, 3s eccentric), single-leg isometric hamstring bridges at 30° and 90° knee flexion (5x45s holds), and progressive flat submaximal strides capped at 75-80% maximal velocity. Strictly avoid maximal velocity sprinting and end-range explosive hill acceleration during active remodeling.",
            category="REHABILITATION",
            target_anatomy=["hamstring", "proximal_tendon", "ischial_tuberosity", "isquiotibial", "isquiotibiales", "isquio"],
            contraindications=["complete_avulsion", "acute_tendon_rupture"],
            rehab_phase="SUBACUTE",
            evidence_level="SYSTEMATIC_REVIEW",
            metadata={"sport": "running", "pathology": "hamstring_proximal", "evidence": "Askling et al. 2014"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_achilles_02",
            title="Achilles Tendinopathy Load Management & Eccentric Progression (Silbernagel / Alfredson)",
            content="Achilles tendinopathy rehabilitation guidelines. Incorporate heavy eccentric heel drops off a step with knee straight (gastrocnemius) and knee bent (soleus) (3x15 twice daily). Avoid rapid uphill running, high cadence hill repeats, and barefoot forefoot bounding until tendon stiffness normalizes and morning stiffness is under 15 minutes.",
            category="REHABILITATION",
            target_anatomy=["achilles_tendon", "soleus", "gastrocnemius"],
            contraindications=["aggressive_hill_running", "plyometric_jumping", "barefoot_sprinting"],
            rehab_phase="SUBACUTE",
            evidence_level="RCT",
            metadata={"sport": "trail_running", "pathology": "achilles_tendinopathy", "evidence": "Silbernagel et al. 2007"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_patellar_03",
            title="Patellar Tendinopathy Isometric Protocols (Spanish Squats)",
            content="Spanish squat isometrics for patellar tendon pain relief (Rio et al. 2015). Perform 5 sets of 45-second isometric holds at 60-70° knee flexion with rigid band support behind knees. Reduces cortical inhibition and provides immediate analgesic effect for up to 45 minutes prior to running. Strictly avoid steep technical downhill running during acute flare-up.",
            category="REHABILITATION",
            target_anatomy=["patellar_tendon", "quadriceps", "knee"],
            contraindications=["steep_downhill_running", "deep_squat_jumps"],
            rehab_phase="ACUTE",
            evidence_level="RCT",
            metadata={"sport": "trail_running", "pathology": "patellar_tendon", "evidence": "Rio et al. 2015"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_marathon_carb_04",
            title="Marathon Carbohydrate Loading & In-Race Fueling Guidelines (Burke / Jeukendrup)",
            content="Carbohydrate loading protocol for endurance marathon racing: 8-10g CHO/kg/day for 36-48h pre-race. Pre-race breakfast: 1-4g CHO/kg consumed 3-4 hours before start. In-race target: 60-90g CHO/hour using multi-transportable carbohydrate ratio (2:1 or 1:0.8 glucose to fructose) accompanied by 400-800ml fluid/hr and 500-700mg sodium/hr.",
            category="NUTRITION",
            target_anatomy=["whole_body", "glycogen_stores"],
            contraindications=["high_fat_pre_race", "high_fiber_race_day"],
            rehab_phase="RETURN_TO_SPORT",
            evidence_level="CLINICAL_GUIDELINE",
            metadata={"discipline": "endurance", "sport": "marathon", "topic": "nutrition", "evidence": "Burke et al. 2019"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_altitude_05",
            title="Altitude Acclimatization, Hydration & Intensity Adjustment in Mountain Running",
            content="Physiological adaptations at altitudes above 2000m. Hyperventilation and dry air increase respiratory water loss; baseline hydration intake must increase by +20-30% (extra 500-1000ml/day). Aerobic training pace must be dampened by 5-10% to prevent excessive lactate accumulation. Monitor serum ferritin to support erythropoiesis.",
            category="PHYSIOLOGY",
            target_anatomy=["cardiorespiratory", "aerobic_system"],
            contraindications=["unacclimatized_anaerobic_max"],
            rehab_phase="RETURN_TO_SPORT",
            evidence_level="SYSTEMATIC_REVIEW",
            metadata={"discipline": "trail_running", "topic": "altitude", "evidence": "Fulco et al. 1998"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_pap_06",
            title="Post-Activation Potentiation (PAP) Protocols for Middle Distance (800m)",
            content="Post-Activation Potentiation (PAP) conditioning for 800m track runners. Heavy back squats (3x3 at 85% 1RM) or hex bar jumps (3x4 at 40% 1RM) performed 8-12 minutes prior to track velocity efforts enhance motor unit recruitment, rate of force development (RFD), and subsequent sprint stride mechanics.",
            category="PERIODIZATION",
            target_anatomy=["quadriceps", "glutes", "hamstring"],
            contraindications=["maximal_velocity_sprint", "acute_muscle_strain", "fatigued_unprimed_state"],
            rehab_phase="RETURN_TO_SPORT",
            evidence_level="RCT",
            metadata={"sport": "track", "topic": "pap_sprint", "evidence": "Tillin & Bishop 2009"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_lumbar_mcgill_07",
            title="Spine-Sparing Rehabilitation for Lumbar Disc Protrusions (McGill Big 3)",
            content="Rehabilitación y readaptación de hernia y protrusión discal lumbar L4-L5 / L5-S1 basada en el Dr. Stuart McGill. Spine-sparing rehabilitation for lumbar disc protrusion. Core stability must be built with neutral spine: (1) Modified Curl-up, (2) Side Plank, and (3) Bird-Dog. Strictly avoid loaded lumbar flexion (e.g. 1RM conventional deadlifts, Roman chair sit-ups). Substitute heavy deadlifts with High-Handle Trap Bar (65% 1RM) and bench Hip Thrusts.",
            category="REHABILITATION",
            target_anatomy=["lumbar_spine", "lumbar", "core", "glutes"],
            contraindications=["cauda_equina_syndrome", "acute_vertebral_fracture"],
            rehab_phase="ACUTE",
            evidence_level="CLINICAL_GUIDELINE",
            metadata={"sport": "strength", "pathology": "lumbar_disc_protrusion", "evidence": "McGill 2015"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_trail_recovery_08",
            title="Trail Running Post-Workout Glycogen Replenishment & Muscle Damage Protocol",
            content="Post-run recovery protocol for trail runners: Consume 1.2g CHO/kg body weight within 30 minutes to optimize glycogen resynthesis rate. Include 30g high-quality protein to stimulate muscle protein synthesis and repair eccentric microtrauma from downhill running. Apply cold water immersion (12-15°C for 10 min) to reduce delayed onset muscle soreness (DOMS).",
            category="NUTRITION",
            target_anatomy=["whole_body", "lower_limb"],
            contraindications=[],
            rehab_phase="MAINTENANCE",
            evidence_level="SYSTEMATIC_REVIEW",
            metadata={"sport": "trail_running", "topic": "recovery"}
        ),
        KnowledgeChunk(
            chunk_id="chunk_powerlifting_recovery_09",
            title="Powerlifting CNS & Myofibrillar Recovery Protocol",
            content="Post-session recovery for powerlifting: 2.0g protein/kg/day with 40g pre-sleep micellar casein for continuous nocturnal amino acid availability. Utilize passive spinal decompression (reverse hyper / traction) to alleviate intra-abdominal and disc compressive loads. Prioritize 8.5+ hours sleep for central nervous system (CNS) neurotransmitter restoration.",
            category="NUTRITION",
            target_anatomy=["cns", "spine", "skeletal_muscle"],
            contraindications=[],
            rehab_phase="MAINTENANCE",
            evidence_level="EXPERT_CONSENSUS",
            metadata={"sport": "powerlifting", "topic": "recovery"}
        )
    ]


@pytest.fixture
def vector_store(sample_knowledge_chunks) -> VectorStore:
    """Pre-populated in-memory vector store."""
    vs = VectorStore()
    vs.add_chunks(sample_knowledge_chunks)
    return vs


@pytest.fixture
def safety_guard() -> SafetyGuard:
    """Initialized SafetyGuard instance."""
    return SafetyGuard()


@pytest.fixture
def agent_router(vector_store, safety_guard) -> AgentRouter:
    """Initialized AgentRouter instance."""
    return AgentRouter(vector_store=vector_store, safety_guard=safety_guard)


@pytest.fixture
def carlos_profile() -> AthleteProfile:
    """
    Athlete Profile matching Carlos (Contexto.md & Scenario 1):
    23yo, 173cm, 58kg, 800m specialist transitioning to Trail Running.
    Pathology: Proximal hamstring myotendinous strain recurrence (subacute phase).
    """
    injury = InjuryRecord(
        injury_id="inj_carlos_hamstring_01",
        injury_name="Proximal Hamstring Myotendinous Junction Tear (May/July Recurrence)",
        anatomical_region="hamstring_proximal",
        date_onset="2026-05-15",
        rehab_phase=RehabPhase.SUBACUTE,
        current_pain_score=2,
        contraindicated_movements=[
            "maximal_velocity_sprint",
            "100% sprint",
            "cuestas a tope",
            "end_range_explosive_stretch",
            "sprint"
        ],
        safe_alternative_protocols=[
            "Submaximal flat strides capped at 75% velocity",
            "Prone Hamstring Isometrics (30-45° knee flexion, 5x45s)",
            "Nordic Curls 3x6 (4s eccentric tempo)",
            "Single-leg elevated hamstring bridges"
        ],
        is_active=True
    )
    return AthleteProfile(
        athlete_id="ath_carlos_800m",
        tenant_id="tenant_carlos",
        name="Carlos",
        age=23,
        gender=Sex.MALE,
        height_cm=173.0,
        weight_kg=58.0,
        primary_discipline=SportDiscipline.TRACK_800M,
        secondary_disciplines=[SportDiscipline.TRAIL_RUNNING],
        training_age_years=7.0,
        vo2max_estimate=71.5,
        threshold_pace_min_km="3:25/km",
        max_heart_rate=198,
        resting_heart_rate=46,
        injuries=[injury]
    )


@pytest.fixture
def marathon_profile() -> AthleteProfile:
    """
    Marathon Athlete Profile (Scenario 2):
    64kg, Sub-2:50 marathoner with Low-FODMAP / Gastrointestinal sensitivity.
    """
    return AthleteProfile(
        athlete_id="ath_marathon_02",
        tenant_id="tenant_marathon",
        name="Elena",
        age=29,
        gender=Sex.FEMALE,
        height_cm=168.0,
        weight_kg=64.0,
        primary_discipline=SportDiscipline.MARATHON,
        dietary_restrictions=["low_fodmap", "sensitive_gut"],
        threshold_pace_min_km="3:55/km",
        max_heart_rate=188,
        resting_heart_rate=48
    )


@pytest.fixture
def overtrained_profile() -> AthleteProfile:
    """
    Overtrained Athlete Profile (Scenario 3):
    Morning HRV drop to 34ms (baseline 68ms -> 50% drop), 4h 15m fragmented sleep.
    """
    rec_metric = RecoveryMetrics(
        date="2026-08-26",
        morning_hrv_rmssd=34.0,
        hrv_baseline_7d=68.0,
        resting_heart_rate=58,
        rhr_baseline_7d=46,
        sleep_hours=4.25,
        sleep_quality_score=38,
        muscle_soreness_score=7,
        stress_level_score=8
    )
    biometrics = BiometricState(daily_metrics=[rec_metric])
    return AthleteProfile(
        athlete_id="ath_fatigued_03",
        tenant_id="tenant_carlos",
        name="Carlos",
        age=23,
        height_cm=173.0,
        weight_kg=58.0,
        primary_discipline=SportDiscipline.TRACK_800M,
        biometrics=biometrics
    )


@pytest.fixture
def crossfit_profile() -> AthleteProfile:
    """
    CrossFit / Strength Athlete Profile (Scenario 4):
    31yo athlete with acute L4-L5 lumbar disc protrusion.
    """
    injury = InjuryRecord(
        injury_id="inj_disc_l4_l5",
        injury_name="Acute L4-L5 Lumbar Disc Protrusion",
        anatomical_region="lumbar_disc_protrusion_L4_L5",
        date_onset="2026-08-01",
        rehab_phase=RehabPhase.ACUTE,
        current_pain_score=4,
        contraindicated_movements=[
            "1rm",
            "conventional_deadlift",
            "cleans_pesados",
            "saltos_al_cajon",
            "loaded_lumbar_flexion"
        ],
        safe_alternative_protocols=[
            "McGill Big 3 (Bird-dog, Side plank, Modified curl-up)",
            "High-Handle Trap Bar Deadlift (65% 1RM, neutral spine)",
            "Barbell Hip Thrusts on bench",
            "Step-ups to low box"
        ],
        is_active=True
    )
    return AthleteProfile(
        athlete_id="ath_crossfit_04",
        tenant_id="tenant_crossfit",
        name="Marcus",
        age=31,
        gender=Sex.MALE,
        height_cm=180.0,
        weight_kg=84.0,
        primary_discipline=SportDiscipline.STRENGTH_CROSSFIT,
        injuries=[injury]
    )
