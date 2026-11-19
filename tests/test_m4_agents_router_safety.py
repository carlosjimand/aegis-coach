"""
Aegis Coach — Milestone M4 Unit & Integration Test Suite (`tests/test_m4_agents_router_safety.py`)
===================================================================================================
Direct unit and integration tests for:
  - Clinical rules, pain VAS policy & safe alternative mapping (`poc.safety.rules`)
  - Red-flag detector (`poc.safety.red_flags`)
  - Injury guard pre-flight & post-flight interception (`poc.safety.injury_guard`)
  - Domain micro-agents (Medical, Planner, Nutrition, DataEntry, General) (`poc.agents.*`)
  - Multi-agent swarm intent router (`poc.router.agent_router`)
  - CLI runner switches (`poc.run_poc`)
"""

import pytest
import json
from pathlib import Path

from poc.config import get_config
from poc.models.athlete import (
    AthleteProfile,
    InjuryRecord,
    RecoveryMetrics,
    BiometricState,
    Sex,
    SportDiscipline,
    RehabPhase,
    ActivityType
)
from poc.models.conversation import UserQuery, DomainIntent, RiskLevel, AgentResponse
from poc.safety.rules import (
    CLINICAL_CONTRAINDICATIONS,
    SAFE_ALTERNATIVE_PROTOCOLS,
    evaluate_pain_vas,
    get_contraindications_for_pathology,
    get_safe_alternatives_for_pathology,
    is_movement_contraindicated
)
from poc.safety.red_flags import RedFlagDetector
from poc.safety.injury_guard import InjuryGuard, SafetyCheckResult
from poc.agents.medical_agent import MedicalAgent
from poc.agents.planner_agent import PlannerAgent
from poc.agents.nutrition_agent import NutritionAgent
from poc.agents.data_entry_agent import DataEntryAgent
from poc.agents.general_agent import GeneralAgent
from poc.router.agent_router import AgentRouter, RoutingDecision
from poc.rag.vector_store import VectorStore
from poc.rag.retriever import HybridRetriever


# ==============================================================================
# Fixtures
# ==============================================================================

@pytest.fixture
def populated_vector_store() -> VectorStore:
    vs = VectorStore()
    vs.ingest_default_knowledge()
    return vs


@pytest.fixture
def hybrid_retriever(populated_vector_store: VectorStore) -> HybridRetriever:
    return HybridRetriever(vector_store=populated_vector_store)


@pytest.fixture
def injury_guard() -> InjuryGuard:
    return InjuryGuard()


@pytest.fixture
def full_agent_router(populated_vector_store: VectorStore, injury_guard: InjuryGuard) -> AgentRouter:
    return AgentRouter(vector_store=populated_vector_store, safety_guard=injury_guard)


@pytest.fixture
def test_carlos_profile() -> AthleteProfile:
    injury = InjuryRecord(
        injury_id="inj_carlos_01",
        injury_name="Proximal Hamstring Strain",
        anatomical_region="hamstring_proximal",
        date_onset="2026-05-18",
        rehab_phase=RehabPhase.SUBACUTE,
        current_pain_score=2,
        contraindicated_movements=["maximal_sprint", "cuestas_a_tope", "100% sprint"],
        safe_alternative_protocols=["Askling L-Protocol", "Prone Hamstring Isometrics 5x45s"]
    )
    return AthleteProfile(
        athlete_id="ath_carlos_01",
        tenant_id="tenant_carlos_800m",
        name="Carlos",
        age=23,
        height_cm=173.0,
        weight_kg=58.0,
        primary_discipline=SportDiscipline.TRACK_800M,
        injuries=[injury]
    )


@pytest.fixture
def test_marathon_profile() -> AthleteProfile:
    return AthleteProfile(
        athlete_id="ath_elena_01",
        tenant_id="tenant_elena_marathon",
        name="Elena",
        age=28,
        gender=Sex.FEMALE,
        height_cm=168.0,
        weight_kg=54.0,
        primary_discipline=SportDiscipline.MARATHON,
        dietary_restrictions=["low_fodmap", "sensitive_gut"]
    )


# ==============================================================================
# 1. Tests for Clinical Safety Rules & Pain VAS Policy
# ==============================================================================

class TestClinicalSafetyRules:
    def test_evaluate_pain_vas_thresholds(self):
        # VAS 0: Asymptomatic
        r0 = evaluate_pain_vas(0)
        assert r0["category"] == "ASYMPTOMATIC"
        assert r0["is_acceptable"] is True
        assert r0["escalation_required"] is False

        # VAS 1-3: Safe adaptation zone
        r2 = evaluate_pain_vas(2)
        assert r2["category"] == "SAFE_ADAPTATION_ZONE"
        assert r2["is_acceptable"] is True
        assert r2["requires_load_reduction"] is False
        assert r2["escalation_required"] is False

        # VAS 4-6: Load reduction zone
        r5 = evaluate_pain_vas(5)
        assert r5["category"] == "ELEVATED_PAIN_LOAD_REDUCTION"
        assert r5["is_acceptable"] is False
        assert r5["requires_load_reduction"] is True
        assert r5["escalation_required"] is False

        # VAS 7-10: Red flag zone
        r8 = evaluate_pain_vas(8)
        assert r8["category"] == "ACUTE_CLINICAL_RED_FLAG"
        assert r8["is_acceptable"] is False
        assert r8["escalation_required"] is True

    def test_contraindication_and_alternative_lookups(self):
        contras = get_contraindications_for_pathology("hamstring_proximal")
        assert len(contras) > 0
        assert any("sprint" in c for c in contras)

        alts = get_safe_alternatives_for_pathology("hamstring_proximal")
        assert len(alts) > 0
        assert any("Askling" in a for a in alts)

        assert is_movement_contraindicated("100% sprint en cuesta", "hamstring_proximal") is True
        assert is_movement_contraindicated("trote suave regenerativo", "hamstring_proximal") is False


# ==============================================================================
# 2. Tests for RedFlagDetector
# ==============================================================================

class TestRedFlagDetector:
    def test_detect_cardiovascular_emergency(self, test_carlos_profile):
        detector = RedFlagDetector()
        viol = detector.detect_red_flags("Tengo una fuerte opresión en el pecho y me falta el aire", test_carlos_profile)
        assert viol is not None
        assert viol.violation_code == "RED_FLAG_CARDIOVASCULAR_EMERGENCY"
        assert viol.risk_level == RiskLevel.CRITICAL
        assert viol.escalation_required is True

    def test_detect_acute_trauma(self, test_carlos_profile):
        detector = RedFlagDetector()
        viol = detector.detect_red_flags("Sonó un chasquido fuerte en el isquio y es imposible apoyar el pie", test_carlos_profile)
        assert viol is not None
        assert viol.violation_code == "RED_FLAG_ACUTE_TRAUMA_RUPTURE"
        assert viol.escalation_required is True

    def test_detect_severe_pain_score(self, test_carlos_profile):
        detector = RedFlagDetector()
        viol = detector.detect_red_flags("Tengo dolor insoportable de 9/10 en el tendón", test_carlos_profile)
        assert viol is not None
        assert viol.violation_code == "RED_FLAG_SEVERE_PAIN_VAS_CRITICAL"
        assert viol.escalation_required is True


# ==============================================================================
# 3. Tests for InjuryGuard (Pre-flight & Post-flight)
# ==============================================================================

class TestInjuryGuard:
    def test_pre_flight_sprint_interception(self, injury_guard, test_carlos_profile):
        res = injury_guard.check_query_safety("Quiero hacer series de sprints máximos al 100%", test_carlos_profile)
        assert res.is_safe is False
        assert res.action_taken == "HARD_REJECT"
        assert len(res.violations) == 1
        assert "70-75%" in res.safe_alternative

    def test_pre_flight_safe_query_pass(self, injury_guard, test_carlos_profile):
        res = injury_guard.check_query_safety("Hoy quiero hacer un trote continuo suave en llano Z1", test_carlos_profile)
        assert res.is_safe is True
        assert res.action_taken == "ALLOW"

    def test_post_flight_response_interception(self, injury_guard, test_carlos_profile):
        dirty_response = "Para mejorar tu velocidad, haz 5 series de 100% sprint en pista."
        cleaned, res = injury_guard.intercept_agent_response(dirty_response, test_carlos_profile)
        assert res.is_safe is False
        assert "[INTERCEPTADO:" in cleaned
        assert "100% sprint" not in cleaned


# ==============================================================================
# 4. Tests for Specialized Domain Agents
# ==============================================================================

class TestDomainAgents:
    def test_medical_agent_retrieval_and_citations(self, hybrid_retriever, test_carlos_profile):
        agent = MedicalAgent(retriever=hybrid_retriever)
        query = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text="¿Cómo debo rehabilitar mi rotura miotendinosa de isquiotibial proximal?"
        )
        response = agent.process(query, test_carlos_profile)
        assert response.primary_intent == DomainIntent.PHYSIO_REHAB
        assert len(response.citations) >= 1
        assert "Askling" in response.message_markdown or "HSR" in response.message_markdown
        assert response.execution_trace.rag_chunks_retrieved >= 1

    def test_planner_agent_periodized_workout(self, test_carlos_profile):
        agent = PlannerAgent()
        query = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text="Planifícame el entrenamiento de hoy para preparar el 800m"
        )
        response = agent.process(query, test_carlos_profile)
        assert response.primary_intent == DomainIntent.WORKOUT_PLANNING
        assert "Calentamiento" in response.message_markdown
        assert "Bloque Principal" in response.message_markdown
        assert response.structured_data is not None
        assert "target_duration_minutes" in response.structured_data

    def test_nutrition_agent_burke_loading(self, test_marathon_profile):
        agent = NutritionAgent()
        query = UserQuery(
            tenant_id=test_marathon_profile.tenant_id,
            athlete_id=test_marathon_profile.athlete_id,
            raw_text="¿Cómo debo hacer la carga de carbohidratos para el maratón sin tener gases?"
        )
        response = agent.process(query, test_marathon_profile)
        assert response.primary_intent == DomainIntent.NUTRITION_RECOVERY
        assert "Low-FODMAP" in response.message_markdown
        assert response.structured_data["protocol"] == "BURKE_CARBOHYDRATE_LOADING"
        # 54kg * 8-10g = 432-540g
        assert response.structured_data["daily_carbs_target_g"][0] == 432

    def test_data_entry_agent_parser(self, test_carlos_profile):
        agent = DataEntryAgent()
        query = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text="Hoy corrí 12.5km en 55 minutos con 240m de desnivel positivo a 160 ppm y RPE 7"
        )
        response = agent.process(query, test_carlos_profile)
        assert response.primary_intent == DomainIntent.DATA_LOGGING
        sd = response.structured_data
        assert sd["distance_km"] == 12.5
        assert sd["duration_minutes"] == 55.0
        assert sd["elevation_gain_m"] == 240
        assert sd["avg_heart_rate"] == 160
        assert sd["rpe"] == 7
        assert sd["trimp_score"] > 0

    def test_general_agent_empty_and_greeting(self, test_carlos_profile):
        agent = GeneralAgent()
        # Empty query
        q_empty = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text=""
        )
        resp_empty = agent.process(q_empty, test_carlos_profile)
        assert "¿En qué puedo ayudarte" in resp_empty.message_markdown

        # Greeting
        q_greet = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text="Buenos días, ¿qué tal?"
        )
        resp_greet = agent.process(q_greet, test_carlos_profile)
        assert "Buenos días" in resp_greet.message_markdown


# ==============================================================================
# 5. Tests for AgentRouter & Swarm Orchestration
# ==============================================================================

class TestAgentRouter:
    def test_router_end_to_end_safe_dispatch(self, full_agent_router, test_marathon_profile):
        query = UserQuery(
            tenant_id=test_marathon_profile.tenant_id,
            athlete_id=test_marathon_profile.athlete_id,
            raw_text="¿Cuántos carbohidratos debo consumir antes del maratón?"
        )
        response = full_agent_router.route_and_execute(query, test_marathon_profile)
        assert response.primary_intent == DomainIntent.NUTRITION_RECOVERY
        assert response.is_safety_override is False
        assert response.execution_trace.agent_dispatched == "NutritionRecoverySpecialist"

    def test_router_end_to_end_unsafe_intercept(self, full_agent_router, test_carlos_profile):
        query = UserQuery(
            tenant_id=test_carlos_profile.tenant_id,
            athlete_id=test_carlos_profile.athlete_id,
            raw_text="Planifícame 10 series de sprints a tope de 100m en cuesta"
        )
        response = full_agent_router.route_and_execute(query, test_carlos_profile)
        assert response.is_safety_override is True
        assert response.execution_trace.agent_dispatched == "SafetyGuardrailInterceptor"
        assert len(response.execution_trace.safety_violations) >= 1
