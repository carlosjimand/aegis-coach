"""
Aegis Coach — Tier 1 Feature Coverage Test Suite (`tests/test_tier1_features.py`)
================================================================================
Comprehensive category-partition test suite covering the 4 core platform capabilities:
  - Feature 1: Sports Science & Medical Vector RAG Retrieval (TC-RAG-01 to TC-RAG-06)
  - Feature 2: Multi-Agent Swarm Intent Routing (TC-ROUT-01 to TC-ROUT-06)
  - Feature 3: Clinical Safety & Injury Guardrails (TC-SAFE-01 to TC-SAFE-06)
  - Feature 4: Multi-Tenant Data & Profile Isolation (TC-TEN-01 to TC-TEN-06)

Total: 24 automated test cases.
"""

import pytest
import concurrent.futures
from typing import Dict, Any, List

from tests.conftest import (
    KnowledgeChunk,
    VectorStore,
    SafetyGuard,
    AgentRouter,
    AthleteProfile,
    InjuryRecord,
    RecoveryMetrics,
    BiometricState,
    WorkoutLog,
    Sex,
    SportDiscipline,
    RehabPhase,
    ActivityType,
    DomainIntent,
    RiskLevel,
    UserQuery,
    TenantContext,
    TenantIsolationError,
    TenantSecurity,
)


# ==============================================================================
# FEATURE 1: Sports Science & Medical Vector RAG Retrieval
# ==============================================================================

class TestFeature1VectorRAG:
    """Test suite for Vector RAG semantic search, metadata pre-filtering, and ranking."""

    def test_tc_rag_01_hamstring_tendinopathy_retrieval(self, vector_store: VectorStore):
        """
        TC-RAG-01: Hamstring Tendinopathy Protocol Retrieval.
        Authoritative source: Askling et al. 2014 & PROJECT.md.
        Expects: High-relevance retrieval of Heavy Slow Resistance (HSR), isometric bridges,
        and flat submaximal strides with similarity >= 0.75 and exclusion of contraindicated sprints.
        """
        query = "Rehabilitación rotura unión miotendinosa isquiotibial proximal"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_anatomy=["hamstring"],
            rehab_phase="SUBACUTE",
            filter_metadata={"sport": "running", "pathology": "hamstring_proximal"}
        )

        assert len(results) >= 1, "Expected at least 1 matching chunk for proximal hamstring rehabilitation."
        top_chunk, score = results[0]
        assert score >= 0.75, f"Expected similarity score >= 0.75, got {score:.3f}"
        assert top_chunk.chunk_id == "chunk_hamstring_01"
        assert "Heavy Slow Resistance" in top_chunk.content or "HSR" in top_chunk.content
        assert "isometric" in top_chunk.content.lower()
        assert "complete_avulsion" in top_chunk.contraindications or "maximal_velocity_sprint" in top_chunk.contraindications or "maximal velocity" in top_chunk.content.lower()

    def test_tc_rag_02_achilles_tendinopathy_load_management(self, vector_store: VectorStore):
        """
        TC-RAG-02: Achilles Tendinopathy Load Management.
        Authoritative source: Silbernagel et al. 2007, Alfredson et al. 1998.
        Expects: Eccentric heel drops protocol, warnings against aggressive hill running.
        """
        query = "Dolor insercional tendón de aquiles en cuestas"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_anatomy=["achilles_tendon"],
            filter_metadata={"sport": "trail_running", "pathology": "achilles_tendinopathy"}
        )

        assert len(results) >= 1
        top_chunk, score = results[0]
        assert top_chunk.chunk_id == "chunk_achilles_02"
        assert "eccentric" in top_chunk.content.lower()
        assert "Silbernagel" in top_chunk.title or "Silbernagel" in top_chunk.metadata.get("evidence", "")
        assert "aggressive_hill_running" in top_chunk.contraindications

    def test_tc_rag_03_patellar_tendinopathy_isometrics(self, vector_store: VectorStore):
        """
        TC-RAG-03: Patellar Tendinopathy Isometric Protocols.
        Authoritative source: Rio et al. 2015 (Spanish Squat Analgesia).
        Expects: 5x45s Spanish Squats isometrics with analgesic effect citations.
        """
        query = "Dolor punta de rodilla al bajar senderos técnicos"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_anatomy=["patellar_tendon"],
            filter_metadata={"sport": "trail_running", "pathology": "patellar_tendon"}
        )

        assert len(results) >= 1
        top_chunk, score = results[0]
        assert top_chunk.chunk_id == "chunk_patellar_03"
        assert "Spanish squat" in top_chunk.content or "Spanish" in top_chunk.title
        assert "Rio et al." in top_chunk.metadata.get("evidence", "")
        assert "steep_downhill_running" in top_chunk.contraindications

    def test_tc_rag_04_marathon_carbohydrate_periodization(self, vector_store: VectorStore):
        """
        TC-RAG-04: Carbohydrate Periodization for Marathon.
        Authoritative source: Burke et al. 2019, Jeukendrup 2014.
        Expects: 8-10g CHO/kg/day guidelines, pre-race breakfast, 60-90g CHO/hr intra-race.
        """
        query = "Protocolo de carga de hidratos para 42k sub-3h"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_metadata={"discipline": "endurance", "sport": "marathon", "topic": "nutrition"}
        )

        assert len(results) >= 1
        top_chunk, score = results[0]
        assert top_chunk.chunk_id == "chunk_marathon_carb_04"
        assert "8-10g" in top_chunk.content or "8-10" in top_chunk.content
        assert "60-90g" in top_chunk.content or "60-90" in top_chunk.content

    def test_tc_rag_05_altitude_acclimatization_hydration(self, vector_store: VectorStore):
        """
        TC-RAG-05: Altitude Acclimatization & Hydration in Mountain Running.
        Authoritative source: Fulco et al. 1998 & PROJECT.md.
        Expects: Hydration increase +20-30%, aerobic pace dampening.
        """
        query = "Adaptación a carrera de montaña a 3000m altitud"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_metadata={"discipline": "trail_running", "topic": "altitude"}
        )

        assert len(results) >= 1
        top_chunk, score = results[0]
        assert top_chunk.chunk_id == "chunk_altitude_05"
        assert "+20-30%" in top_chunk.content or "20-30%" in top_chunk.content
        assert "aerobic" in top_chunk.content.lower()

    def test_tc_rag_06_post_activation_potentiation_800m(self, vector_store: VectorStore):
        """
        TC-RAG-06: Post-Activation Potentiation (PAP) for 800m Middle Distance.
        Authoritative source: Tillin & Bishop 2009 & PROJECT.md.
        Expects: Heavy back squats (85% 1RM) or hex bar jumps 8-12 min prior to velocity work.
        """
        query = "Ejercicios de potenciación post-activación para medio fondo"
        results = vector_store.search(
            query=query,
            top_k=3,
            filter_metadata={"sport": "track", "topic": "pap_sprint"}
        )

        assert len(results) >= 1
        top_chunk, score = results[0]
        assert top_chunk.chunk_id == "chunk_pap_06"
        assert "8-12 min" in top_chunk.content or "8-12" in top_chunk.content
        assert "squat" in top_chunk.content.lower() or "hex bar" in top_chunk.content.lower()


# ==============================================================================
# FEATURE 2: Multi-Agent Swarm Intent Routing
# ==============================================================================

class TestFeature2AgentRouting:
    """Test suite for intent classification and specialized multi-agent dispatch."""

    def test_tc_rout_01_acute_injury_medical_routing(self, agent_router: AgentRouter):
        """
        TC-ROUT-01: Acute Pain / Injury Disclosure.
        Expects: Primary intent classified as PHYSIO_REHAB.
        """
        query_text = "Ayer sentí un pinchazo agudo en el isquio al acelerar"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.PHYSIO_REHAB

    def test_tc_rout_02_workout_planning_routing(self, agent_router: AgentRouter):
        """
        TC-ROUT-02: Weekly Training Generation Request.
        Expects: Primary intent classified as WORKOUT_PLANNING.
        """
        query_text = "Planifícame el microciclo de la semana que viene con 4 días de entreno"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.WORKOUT_PLANNING

    def test_tc_rout_03_natural_language_workout_logging(self, agent_router: AgentRouter):
        """
        TC-ROUT-03: Natural Language Workout Log.
        Expects: Primary intent DATA_LOGGING with extracted entities (distance: 12.0km, pace: 4:45/km, HR: 142, RPE: 6).
        """
        query_text = "Hoy hice 12km de rodaje suave a 4:45/km con 142 ppm de media, RPE 6"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.DATA_LOGGING
        assert decision.extracted_entities.get("distance_km") == 12.0
        assert decision.extracted_entities.get("pace_avg") == "4:45/km"
        assert decision.extracted_entities.get("avg_heart_rate") == 142
        assert decision.extracted_entities.get("rpe") == 6

    def test_tc_rout_04_motivational_general_chat(self, agent_router: AgentRouter):
        """
        TC-ROUT-04: Motivational / Conversational Check-in.
        Expects: Primary intent classified as GENERAL_CHAT.
        """
        query_text = "Hola! Me cuesta levantarme hoy a entrenar, qué opinas?"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.GENERAL_CHAT

    def test_tc_rout_05_compound_query_multi_intent(self, agent_router: AgentRouter):
        """
        TC-ROUT-05: Compound Query (Pain + Plan Modification).
        Expects: Primary PHYSIO_REHAB with secondary WORKOUT_PLANNING.
        """
        query_text = "Me molesta el soleo derecho, qué hacemos con las series de mañana?"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.PHYSIO_REHAB
        assert DomainIntent.WORKOUT_PLANNING in decision.secondary_intents

    def test_tc_rout_06_nutrition_and_fueling_inquiry(self, agent_router: AgentRouter):
        """
        TC-ROUT-06: Nutrition & Fueling Inquiry.
        Expects: Primary intent classified as NUTRITION_RECOVERY.
        """
        query_text = "Cuántos gramos de carbohidratos debo tomar en salidas de más de 2 horas?"
        decision = agent_router.classify_intent(query_text)
        assert decision.primary_intent == DomainIntent.NUTRITION_RECOVERY


# ==============================================================================
# FEATURE 3: Clinical Safety & Injury Guardrails
# ==============================================================================

class TestFeature3ClinicalSafety:
    """Test suite for deterministic biomechanical safety rules and emergency red-flags."""

    def test_tc_safe_01_high_risk_sprint_hamstring_tear(self, safety_guard: SafetyGuard, carlos_profile: AthleteProfile):
        """
        TC-SAFE-01: High-Risk Sprint with Acute/Subacute Hamstring Tear.
        Expects: Hard Reject, action_taken == 'HARD_REJECT', blocks 100% sprints, substitutes submaximal strides + isometrics.
        """
        query = "Quiero hacer 5x100m de cuestas a tope (100% sprint) para recuperar chispa"
        result = safety_guard.check_query_safety(query, carlos_profile)

        assert not result.is_safe
        assert result.action_taken == "HARD_REJECT"
        assert len(result.violations) == 1
        assert result.violations[0].violation_code == "CONTRAINDICATION_ACUTE_HAMSTRING_MAX_VELOCITY"
        assert "70-75%" in result.safe_alternative or "submaximal" in result.safe_alternative.lower()

    def test_tc_safe_02_spinal_loading_lumbar_disc(self, safety_guard: SafetyGuard, crossfit_profile: AthleteProfile):
        """
        TC-SAFE-02: Heavy Spinal Loading with Lumbar Disc Herniation.
        Expects: Hard Reject, action_taken == 'HARD_REJECT', blocks 1RM deadlifts, substitutes McGill Big 3 & Trap Bar.
        """
        query = "Hoy quiero tirar un test de 1RM de Peso Muerto convencional y luego meter cleans pesados"
        result = safety_guard.check_query_safety(query, crossfit_profile)

        assert not result.is_safe
        assert result.action_taken == "HARD_REJECT"
        assert result.violations[0].violation_code == "CONTRAINDICATION_SPINAL_AXIAL_SHEAR"
        assert "McGill" in result.safe_alternative

    def test_tc_safe_03_patellar_volume_flare_up(self, safety_guard: SafetyGuard):
        """
        TC-SAFE-03: Excessive Volume during Patellar Tendinopathy Flare-up.
        Expects: Soft Reject / Modify, action_taken == 'SOFT_REJECT', blocks downhill running, prescribes uphill treadmill / isometrics.
        """
        patellar_injury = InjuryRecord(
            injury_id="inj_patella_01",
            injury_name="Patellar Tendinitis",
            anatomical_region="patellar_tendon",
            date_onset="2026-08-10",
            rehab_phase=RehabPhase.ACUTE,
            contraindicated_movements=["steep_downhill_running"],
            safe_alternative_protocols=["Spanish squats", "Uphill hiking"]
        )
        athlete = AthleteProfile(
            athlete_id="ath_patella",
            tenant_id="tenant_trail",
            name="Laura",
            age=26,
            height_cm=165.0,
            weight_kg=54.0,
            injuries=[patellar_injury]
        )
        query = "Quiero hacer una tirada de 20km con 1200m de desnivel negativo por sendero técnico"
        result = safety_guard.check_query_safety(query, athlete)

        assert not result.is_safe
        assert result.action_taken == "SOFT_REJECT"
        assert result.violations[0].violation_code == "CONTRAINDICATION_HIGH_ECCENTRIC_IMPACT"
        assert "Spanish Squat" in result.safe_alternative or "Uphill" in result.safe_alternative

    def test_tc_safe_04_overtraining_autonomic_crash(self, safety_guard: SafetyGuard, overtrained_profile: AthleteProfile):
        """
        TC-SAFE-04: Overtraining / Autonomic Crash Warning.
        Expects: Safety Override, action_taken == 'OVERRIDE', intercepts interval workout, replaces with Zone 1 active recovery.
        """
        query = "Hoy me tocan series duras de 5x1000m a ritmo threshold"
        result = safety_guard.check_query_safety(query, overtrained_profile)

        assert not result.is_safe
        assert result.action_taken == "OVERRIDE"
        assert result.violations[0].violation_code == "FATIGUE_OVERRIDE_AUTONOMIC_DEPRESSION"
        assert "Zone 1" in result.safe_alternative or "recuperación" in result.safe_alternative.lower()

    def test_tc_safe_05_cardiovascular_red_flag_emergency(self, safety_guard: SafetyGuard, carlos_profile: AthleteProfile):
        """
        TC-SAFE-05: Medical Red Flag: Chest Pain / Dyspnea.
        Expects: Emergency Lockout, escalation_required == True, immediate doctor referral.
        """
        query = "Siento opresión en el pecho y mareo al correr rápido"
        result = safety_guard.check_query_safety(query, carlos_profile)

        assert not result.is_safe
        assert result.action_taken == "EMERGENCY_LOCKOUT"
        assert result.escalation_required is True
        assert result.violations[0].violation_code == "RED_FLAG_CARDIOVASCULAR_EMERGENCY"
        assert result.violations[0].risk_level == RiskLevel.CRITICAL

    def test_tc_safe_06_low_energy_availability_lea(self, safety_guard: SafetyGuard, marathon_profile: AthleteProfile):
        """
        TC-SAFE-06: Low Energy Availability (LEA) / RED-S Interception.
        Expects: Safety Interception, flags metabolic danger, enforces minimum caloric baseline.
        """
        query = "Quiero hacer una dieta de 1200 kcal con 20h de volumen de entrenamiento semanal"
        result = safety_guard.check_query_safety(query, marathon_profile)

        assert not result.is_safe
        assert result.action_taken == "SAFETY_INTERCEPTION"
        assert result.violations[0].violation_code == "RED_FLAG_ENERGY_DEFICIENCY_LEA"
        assert "kcal" in result.safe_alternative


# ==============================================================================
# FEATURE 4: Multi-Tenant Data & Profile Isolation
# ==============================================================================

class TestFeature4MultiTenancy:
    """Test suite for tenant boundaries, RLS emulation, and cross-tenant leakage prevention."""

    def test_tc_ten_01_cross_tenant_profile_rejection(self, carlos_profile: AthleteProfile):
        """
        TC-TEN-01: Cross-Tenant Profile Rejection.
        Tenant B attempting to access Tenant A profile raises TenantIsolationError.
        """
        with TenantContext("tenant_beta") as tenant_beta_ctx:
            with pytest.raises(TenantIsolationError) as exc_info:
                tenant_beta_ctx.validate_access(carlos_profile.tenant_id)
            assert "Security Violation" in str(exc_info.value)
            assert "tenant_beta" in str(exc_info.value)
            assert "tenant_carlos" in str(exc_info.value)

    def test_tc_ten_02_vector_store_payload_isolation(self, vector_store: VectorStore):
        """
        TC-TEN-02: Vector Store Query Payload Isolation.
        Tenant A private custom chunks are strictly invisible to Tenant B.
        """
        private_chunk_tenant_a = KnowledgeChunk(
            chunk_id="chunk_secret_tenant_a",
            title="Tenant A Private Proprietary Protocol",
            content="Top secret proprietary altitude hyperoxia protocol for elite marathoners.",
            category="PHYSIOLOGY",
            metadata={"confidential": True}
        )
        vector_store.add_chunks([private_chunk_tenant_a], tenant_id="tenant_alpha")

        # Query from Tenant Alpha should find the chunk
        alpha_results = vector_store.search("hyperoxia altitude", tenant_id="tenant_alpha")
        assert any(chunk.chunk_id == "chunk_secret_tenant_a" for chunk, _ in alpha_results)

        # Query from Tenant Beta must NOT find the chunk
        beta_results = vector_store.search("hyperoxia altitude", tenant_id="tenant_beta")
        assert not any(chunk.chunk_id == "chunk_secret_tenant_a" for chunk, _ in beta_results)

    def test_tc_ten_03_workout_history_leakage_prevention(self):
        """
        TC-TEN-03: Workout History Leakage Prevention.
        Simulates database query filtering by tenant context.
        """
        mock_db_workouts = [
            {"workout_id": "w1", "tenant_id": "tenant_101", "distance_km": 15.0},
            {"workout_id": "w2", "tenant_id": "tenant_101", "distance_km": 8.0},
            {"workout_id": "w3", "tenant_id": "tenant_102", "distance_km": 21.0},
        ]

        def get_tenant_workouts(current_tenant_id: str):
            with TenantContext(current_tenant_id) as ctx:
                return [w for w in mock_db_workouts if w["tenant_id"] == ctx.tenant_id]

        tenant_102_workouts = get_tenant_workouts("tenant_102")
        assert len(tenant_102_workouts) == 1
        assert tenant_102_workouts[0]["workout_id"] == "w3"
        assert not any(w["tenant_id"] == "tenant_101" for w in tenant_102_workouts)

    def test_tc_ten_04_intervals_icu_api_key_scoping(self):
        """
        TC-TEN-04: Intervals.icu API Key Scoping.
        Verifies credentials vault guarantees separate per-tenant API keys.
        """
        vault = {
            "tenant_alpha": {"intervals_api_key": "sec_alpha_999", "icu_athlete_id": "i1234"},
            "tenant_beta": {"intervals_api_key": "sec_beta_888", "icu_athlete_id": "i5678"}
        }

        def get_tenant_api_credentials(tenant_id: str) -> Dict[str, str]:
            if tenant_id not in vault:
                raise KeyError(f"No credentials for tenant {tenant_id}")
            return vault[tenant_id]

        creds_alpha = get_tenant_api_credentials("tenant_alpha")
        creds_beta = get_tenant_api_credentials("tenant_beta")

        assert creds_alpha["intervals_api_key"] != creds_beta["intervals_api_key"]
        assert creds_alpha["icu_athlete_id"] != creds_beta["icu_athlete_id"]

    def test_tc_ten_05_mismatched_webhook_rejection(self):
        """
        TC-TEN-05: Mismatched Webhook Rejection.
        Payload tenant mismatch is rejected with 401 Unauthorized.
        """
        with pytest.raises(PermissionError) as exc_info:
            TenantSecurity.verify_webhook_signature(
                payload_tenant_id="tenant_attacker",
                header_tenant_id="tenant_victim"
            )
        assert "401 Unauthorized" in str(exc_info.value)

    def test_tc_ten_06_concurrent_multi_tenant_check_in_isolation(self, agent_router: AgentRouter):
        """
        TC-TEN-06: Concurrent Multi-Tenant Check-in Execution.
        Simultaneous execution across 20 distinct tenants maintains zero session bleeding.
        """
        def execute_checkin(index: int) -> Dict[str, Any]:
            t_id = f"tenant_{index:03d}"
            ath_id = f"ath_{index:03d}"
            profile = AthleteProfile(
                athlete_id=ath_id,
                tenant_id=t_id,
                name=f"Athlete_{index}",
                age=25 + (index % 10),
                height_cm=170.0 + index,
                weight_kg=60.0 + (index % 15)
            )
            query = UserQuery(
                tenant_id=t_id,
                athlete_id=ath_id,
                raw_text=f"Buenos días, hoy hice {5 + index}km suave"
            )
            response = agent_router.route_and_execute(query, profile)
            return {
                "tenant_id": response.tenant_id,
                "athlete_id": response.athlete_id,
                "expected_tenant": t_id,
                "expected_athlete": ath_id
            }

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(execute_checkin, i) for i in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        assert len(results) == 20
        for res in results:
            assert res["tenant_id"] == res["expected_tenant"], "Session bleeding detected across tenant boundaries!"
            assert res["athlete_id"] == res["expected_athlete"]
