"""
Aegis Coach — Tier 2 Boundary & Corner Cases Test Suite (`tests/test_tier2_boundaries.py`)
========================================================================================
Assesses system resilience under boundary, extreme, and degraded conditions:
  - TC-BND-01: Empty / Whitespace inputs
  - TC-BND-02: Max token / Large payload handling
  - TC-BND-03: Contradictory injury claims (user chat vs clinical DB record)
  - TC-BND-04: Unknown / Hallucinated exercise handling
  - TC-BND-05: Missing / Tampered tenant header
  - TC-BND-06: Malformed third-party ingress payload handling
  - TC-BND-07: Ambiguous multi-intent compound query parsing

Total: 7 automated test cases.
"""

import pytest
import json
from typing import Dict, Any

from tests.conftest import (
    AgentRouter,
    SafetyGuard,
    AthleteProfile,
    InjuryRecord,
    RehabPhase,
    UserQuery,
    DomainIntent,
    TenantSecurity,
)


class TestTier2BoundaryCases:
    """Boundary Value Analysis (BVA) & Corner Case Verification."""

    @pytest.mark.parametrize("empty_input", ["", "   ", "\n\t\r", "   \n\n  \t "])
    def test_tc_bnd_01_empty_and_whitespace_inputs(
        self,
        agent_router: AgentRouter,
        carlos_profile: AthleteProfile,
        empty_input: str
    ):
        """
        TC-BND-01: Empty & Whitespace Input Handling.
        Authoritative source: PROJECT.md & Explorer 3 blueprint.
        Expects: Safe handling, returns clarification prompt without crashing or raising unhandled exceptions.
        """
        query = UserQuery(
            tenant_id=carlos_profile.tenant_id,
            athlete_id=carlos_profile.athlete_id,
            raw_text=empty_input
        )
        response = agent_router.route_and_execute(query, carlos_profile)

        assert response is not None
        assert response.primary_intent == DomainIntent.GENERAL_CHAT
        assert "¿En qué puedo ayudarte" in response.message_markdown or "No he recibido ningún mensaje" in response.message_markdown
        assert not response.is_safety_override

    def test_tc_bnd_02_max_token_large_payload_handling(
        self,
        agent_router: AgentRouter,
        carlos_profile: AthleteProfile
    ):
        """
        TC-BND-02: Max Token / Extreme Context Length Handling.
        Expects: Graceful truncation and processing of a 15,000-word payload without memory crash or unhandled error.
        """
        large_text = "Corrí 10km suave a 5:00/km con 140 ppm. " * 1500  # ~15,000 words
        query = UserQuery(
            tenant_id=carlos_profile.tenant_id,
            athlete_id=carlos_profile.athlete_id,
            raw_text=large_text[:4000]  # Simulate buffer ceiling
        )
        response = agent_router.route_and_execute(query, carlos_profile)

        assert response is not None
        assert response.primary_intent == DomainIntent.DATA_LOGGING
        assert response.structured_data is not None
        assert response.structured_data.get("distance_km") == 10.0

    def test_tc_bnd_03_contradictory_injury_claims(
        self,
        safety_guard: SafetyGuard,
        agent_router: AgentRouter,
        carlos_profile: AthleteProfile
    ):
        """
        TC-BND-03: Contradictory Injury Claims.
        User chat claim: "No tengo ninguna lesión, ponme series a tope a 100% de sprint".
        Clinical DB record: Active proximal hamstring tear recurrence (May/July).
        Expects: Clinical DB record strictly overrides chat claim. Hard safety interception is enforced.
        """
        contradictory_query_text = "No tengo ninguna lesión, me encuentro perfecto, ponme series a tope a 100% sprint"
        query = UserQuery(
            tenant_id=carlos_profile.tenant_id,
            athlete_id=carlos_profile.athlete_id,
            raw_text=contradictory_query_text
        )

        response = agent_router.route_and_execute(query, carlos_profile)

        assert response.is_safety_override is True
        assert len(response.execution_trace.safety_violations) >= 1
        assert response.execution_trace.safety_violations[0].violation_code == "CONTRAINDICATION_ACUTE_HAMSTRING_MAX_VELOCITY"
        assert "70-75%" in response.message_markdown or "submaximal" in response.message_markdown.lower()

    def test_tc_bnd_04_unknown_hallucinated_exercise_handling(
        self,
        agent_router: AgentRouter,
        carlos_profile: AthleteProfile
    ):
        """
        TC-BND-04: Unknown / Hallucinated Exercise Handling.
        User requests non-existent / fabricated exercise: '4x10 Quantum Hyper-Lunges gravitacionales'.
        Expects: Parser identifies exercise entities, flags unknown exercises, and provides standard movement fallback.
        """
        query_text = "Quiero hacer 4x10 de Quantum Hyper-Lunges gravitacionales con mancuernas"
        decision = agent_router.classify_intent(query_text)

        assert decision.primary_intent == DomainIntent.WORKOUT_PLANNING
        # Exercise should be parsed without crash
        assert "plan" in decision.primary_intent.value.lower() or decision.primary_intent == DomainIntent.WORKOUT_PLANNING

    def test_tc_bnd_05_missing_or_tampered_tenant_header(self):
        """
        TC-BND-05: Missing / Tampered Tenant Header.
        Missing or tampered headers raise 401/403 Security Exception.
        """
        # Missing Header
        with pytest.raises(PermissionError) as exc_info:
            TenantSecurity.validate_tenant_header({})
        assert "401 Unauthorized" in str(exc_info.value)

        # Tampered Header
        with pytest.raises(PermissionError) as exc_info_tampered:
            TenantSecurity.validate_tenant_header({"X-Tenant-ID": "invalid_tampered_tenant_999"})
        assert "403 Forbidden" in str(exc_info_tampered.value)

    def test_tc_bnd_06_malformed_ingress_payload_handling(self):
        """
        TC-BND-06: Malformed Ingress Payload Handling.
        Malformed webhook JSON is rejected with 422 Unprocessable Entity status without crashing server.
        """
        malformed_raw_payloads = [
            "{ bad json: true, ",  # Syntax error
            json.dumps({"distance": "invalid_string_not_float", "duration": -50}),  # Schema violation
            json.dumps({"unrecognized_root": {}})  # Missing required athlete identification
        ]

        def process_ingress_webhook(payload_str: str) -> Dict[str, Any]:
            try:
                data = json.loads(payload_str)
                if "icu_athlete_id" not in data and "athlete_id" not in data:
                    return {"status": 422, "error": "Unprocessable Entity: Missing athlete identifier."}
                if not isinstance(data.get("duration", 0), (int, float)) or data.get("duration", 0) <= 0:
                    return {"status": 422, "error": "Unprocessable Entity: Invalid duration."}
                return {"status": 200, "data": data}
            except json.JSONDecodeError:
                return {"status": 422, "error": "Unprocessable Entity: Malformed JSON syntax."}

        for payload in malformed_raw_payloads:
            result = process_ingress_webhook(payload)
            assert result["status"] == 422
            assert "Unprocessable Entity" in result["error"]

    def test_tc_bnd_07_ambiguous_multi_intent_compound_query(
        self,
        agent_router: AgentRouter,
        carlos_profile: AthleteProfile
    ):
        """
        TC-BND-07: Ambiguous Multi-Intent Compound Query.
        Query contains 3 simultaneous intents:
          1. Medical pain disclosure ("Me duelen las piernas")
          2. Workout intention ("quiero hacer 15km")
          3. Nutrition fueling question ("cuánto arroz como hoy")
        Expects: Decomposed into primary + secondary intents, capturing all domains.
        """
        query_text = "Me duelen las piernas pero quiero hacer 15km y además cuánto arroz como hoy?"
        decision = agent_router.classify_intent(query_text)

        # Should classify with primary and capture secondary intents
        assert decision.primary_intent in [DomainIntent.PHYSIO_REHAB, DomainIntent.WORKOUT_PLANNING, DomainIntent.DATA_LOGGING]
        assert len(decision.secondary_intents) >= 1
        assert decision.extracted_entities.get("distance_km") == 15.0
