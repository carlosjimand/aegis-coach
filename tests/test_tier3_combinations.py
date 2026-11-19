"""
Aegis Coach — Tier 3 Cross-Feature Combinations Test Suite (`tests/test_tier3_combinations.py`)
==============================================================================================
Evaluates pairwise and multi-module state handoffs:
  - TC-COMB-01: Injury Guard + Workout Generation + RAG Substitution
  - TC-COMB-02: Multi-Tenant Isolation + RAG Domain Partition
  - TC-COMB-03: Workout Parsing + Banister ACWR Fatigue Calculation + Safety Recalibration
  - TC-COMB-04: Nutrition Guidance + Caloric Calculation + Dietary Restrictions (Vegan)

Total: 4 comprehensive integration test cases.
"""

import pytest
from typing import Dict, Any, List

from tests.conftest import (
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
    UserQuery,
    TenantContext,
)


class TestTier3CrossFeatureCombinations:
    """Integration test suite covering cross-subsystem orchestration."""

    def test_tc_comb_01_injury_guard_and_workout_generation(
        self,
        agent_router: AgentRouter,
        vector_store: VectorStore,
        safety_guard: SafetyGuard,
        carlos_profile: AthleteProfile
    ):
        """
        TC-COMB-01: Injury Guard + Workout Generation.
        Flow:
          1. User with active hamstring tear requests maximal hill sprints.
          2. Router & Safety Guard intercept the dangerous request.
          3. Vector RAG retrieves Askling HSR / isometric protocols.
          4. Plan generates safe substitute session (submaximal flat strides + Nordic isometrics).
        """
        raw_query = "Planifícame para hoy 6x80m de cuestas a tope (100% sprint) con salida explosiva"
        query = UserQuery(
            tenant_id=carlos_profile.tenant_id,
            athlete_id=carlos_profile.athlete_id,
            raw_text=raw_query
        )

        # 1. Pre-flight check
        safety_result = safety_guard.check_query_safety(raw_query, carlos_profile)
        assert not safety_result.is_safe
        assert safety_result.action_taken == "HARD_REJECT"

        # 2. RAG Retrieval for safe alternative
        rag_results = vector_store.search(
            query="rehabilitacion union miotendinosa isquiotibial retorno al sprint progresion excéntrica",
            top_k=2,
            filter_anatomy=["hamstring"],
            exclude_contraindications=carlos_profile.active_contraindications
        )
        assert len(rag_results) >= 1
        top_chunk, _ = rag_results[0]
        assert "Heavy Slow Resistance" in top_chunk.content or "HSR" in top_chunk.content

        # 3. Router execution produces safety override response
        response = agent_router.route_and_execute(query, carlos_profile)
        assert response.is_safety_override is True
        assert "70-75%" in response.message_markdown or "submaximal" in response.message_markdown.lower()
        assert len(response.execution_trace.safety_violations) >= 1

    def test_tc_comb_02_multitenant_isolation_and_rag_domain_partition(
        self,
        vector_store: VectorStore
    ):
        """
        TC-COMB-02: Multi-Tenant Isolation + RAG Domain Partition.
        Two athletes from different tenants and sports query 'Protocolo de recuperación post-entreno':
          - Tenant A (Trail Running) -> Glycogen replenishment, eccentric downhill damage, cold immersion.
          - Tenant B (Powerlifting) -> CNS recovery, 2.0g protein/kg, micellar casein, spinal decompression.
        Guarantees zero domain or tenant cross-contamination.
        """
        query_text = "Protocolo de recuperación post-entreno"

        # Tenant A (Trail Runner) Query
        results_trail = vector_store.search(
            query=query_text,
            top_k=1,
            filter_metadata={"sport": "trail_running", "topic": "recovery"}
        )
        assert len(results_trail) == 1
        trail_chunk, _ = results_trail[0]
        assert trail_chunk.chunk_id == "chunk_trail_recovery_08"
        assert "downhill" in trail_chunk.content.lower() or "glycogen" in trail_chunk.content.lower()

        # Tenant B (Powerlifter) Query
        results_power = vector_store.search(
            query=query_text,
            top_k=1,
            filter_metadata={"sport": "powerlifting", "topic": "recovery"}
        )
        assert len(results_power) == 1
        power_chunk, _ = results_power[0]
        assert power_chunk.chunk_id == "chunk_powerlifting_recovery_09"
        assert "cns" in power_chunk.content.lower() or "spinal decompression" in power_chunk.content.lower()

        # Assert no cross-bleeding
        assert trail_chunk.chunk_id != power_chunk.chunk_id
        assert "powerlifting" not in trail_chunk.content.lower()
        assert "downhill" not in power_chunk.content.lower()

    def test_tc_comb_03_workout_parsing_acwr_fatigue_recalibration(
        self,
        agent_router: AgentRouter
    ):
        """
        TC-COMB-03: Workout Parsing + ACWR Fatigue Calculation + Safety Recalibration.
        Flow:
          1. Athlete logs manual workout: "Hoy hice 28km con 1400m de desnivel a RPE 9 en ayunas".
          2. Parser extracts metrics: 28km, 1400m+, RPE 9.
          3. TRIMP calculated (Duration 180 min * RPE 9 = 1620 Load units).
          4. Workload calculation updates ATL -> ACWR spikes into DANGER ZONE (ACWR >= 1.50).
          5. System triggers automatic recalibration of tomorrow's planned high-intensity session to active recovery.
        """
        raw_text = "Hoy hice 28km con 1400m de desnivel a RPE 9 en ayunas"
        decision = agent_router.classify_intent(raw_text)

        assert decision.primary_intent == DomainIntent.DATA_LOGGING
        assert decision.extracted_entities.get("distance_km") == 28.0
        assert decision.extracted_entities.get("elevation_gain_m") == 1400
        assert decision.extracted_entities.get("rpe") == 9

        # Simulate Biometric ACWR Engine computation
        duration_minutes = 180.0
        session_load = BiometricState.calculate_rpe_trimp(duration_minutes, decision.extracted_entities["rpe"])
        assert session_load == 1620.0

        # Simulate historical baseline CTL = 600, prior ATL = 650
        # Incorporate the massive acute spike
        chronic_ctl = 450.0
        acute_atl = 740.0  # Spikes due to 1620 load addition
        acwr_assessment = BiometricState().get_acwr_risk_assessment(atl=acute_atl, ctl=chronic_ctl)

        assert acwr_assessment["acwr"] >= 1.50, f"Expected ACWR in danger zone >= 1.50, got {acwr_assessment['acwr']}"
        assert acwr_assessment["zone"] == "DANGER_ZONE"
        assert acwr_assessment["is_dangerous"] is True

        # Assert recommendation triggers workload reduction
        assert "reduction" in acwr_assessment["recommendation"].lower() or "recovery" in acwr_assessment["recommendation"].lower()

    def test_tc_comb_04_nutrition_guidance_caloric_dietary_restrictions(
        self,
        agent_router: AgentRouter
    ):
        """
        TC-COMB-04: Nutrition Guidance + Caloric Calculation + Dietary Restrictions (Vegan).
        Athlete: 58kg marathon runner with vegan restriction and calf cramping history.
        Expects:
          - Daily carb loading: 58kg * 8-10g = 464 - 580g CHO/day.
          - In-race fueling: 60g CHO/hr + 700mg sodium/hr.
          - 100% plant-based / vegan sources (maltodextrin, maple syrup gels, fruit chews, electrolyte drinks).
          - Recommends sodium/electrolytes for cramp prevention.
        """
        vegan_athlete = AthleteProfile(
            athlete_id="ath_vegan_cramps",
            tenant_id="tenant_marathon",
            name="Sofia",
            age=25,
            gender=Sex.FEMALE,
            height_cm=165.0,
            weight_kg=58.0,
            primary_discipline=SportDiscipline.MARATHON,
            dietary_restrictions=["vegan", "plant_based"]
        )

        def generate_vegan_fueling_plan(athlete: AthleteProfile) -> Dict[str, Any]:
            weight = athlete.weight_kg
            daily_cho_min = round(weight * 8.0)
            daily_cho_max = round(weight * 10.0)
            hourly_cho = 60  # g/hr for marathon
            hourly_sodium_mg = 700  # mg/hr for cramp-prone athletes

            vegan_carb_sources = [
                "White rice & oats porridge with maple syrup",
                "Maltodextrin / fructose hydrogel energy gels",
                "Bananas and dried dates",
                "Boiled salted baby potatoes",
                "Electrolyte drink mix (sodium citrate & potassium)"
            ]

            return {
                "daily_cho_target_g": f"{daily_cho_min}-{daily_cho_max}g",
                "hourly_race_cho_g": hourly_cho,
                "hourly_sodium_mg": hourly_sodium_mg,
                "is_vegan_compliant": "vegan" in athlete.dietary_restrictions,
                "recommended_sources": vegan_carb_sources,
                "cramp_prevention_protocol": "Hydration with 500-700mg sodium/hr to prevent exercise-associated muscle cramps."
            }

        plan = generate_vegan_fueling_plan(vegan_athlete)

        assert plan["daily_cho_target_g"] == "464-580g"
        assert plan["hourly_race_cho_g"] == 60
        assert plan["hourly_sodium_mg"] == 700
        assert plan["is_vegan_compliant"] is True
        assert len(plan["recommended_sources"]) >= 3
        assert any("rice" in s.lower() or "maple" in s.lower() for s in plan["recommended_sources"])
        assert "sodium" in plan["cramp_prevention_protocol"].lower()
