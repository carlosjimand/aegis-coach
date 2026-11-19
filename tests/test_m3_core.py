"""
Unit & Integration Tests for Milestone M3
=========================================
Tests:
- Configuration (poc.config)
- Athlete Data Models & Banister Physiology Calculations (poc.models.athlete)
- Conversation Models & Trace Telemetry (poc.models.conversation)
- Clinical Sports Science Datasets (poc.data)
- Deterministic & Live Embedding Adapters (poc.rag.embeddings)
- Vector Store Ingestion & Metadata Filtering (poc.rag.vector_store)
- Hybrid Retriever & Clinical Citation Formatter (poc.rag.retriever)
- Multi-Tenant Context & Isolation Security (poc.tenancy)
"""

import json
import pytest
from pathlib import Path

from poc.config import get_config, reset_config, AegisConfig
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
from poc.rag.embeddings import (
    DeterministicEmbeddingAdapter,
    OpenAIEmbeddingAdapter,
    get_embedding_adapter,
)
from poc.rag.vector_store import (
    KnowledgeChunk,
    VectorStore,
)
from poc.rag.retriever import (
    HybridRetriever,
)
from poc.tenancy.context import (
    TenantContext,
    TenantIsolationError,
    TenantSecurityError,
    get_current_tenant,
    set_current_tenant,
    clear_current_tenant,
)
from poc.tenancy.security import (
    TenantSecurityManager,
)


class TestM3Config:
    def test_default_config(self):
        cfg = get_config()
        assert cfg.mock_mode is True
        assert cfg.embedding_dim == 128
        assert cfg.medical_knowledge_path.exists()
        assert cfg.sample_workouts_path.exists()
        assert cfg.user_profiles_path.exists()

    def test_reset_config(self):
        custom = AegisConfig(embedding_dim=256, mock_mode=True)
        reset_config(custom)
        assert get_config().embedding_dim == 256
        reset_config()  # Reset back to default


class TestM3DataModels:
    def test_injury_record_properties(self):
        inj = InjuryRecord(
            injury_id="inj_test_01",
            injury_name="Hamstring Strain",
            anatomical_region="hamstring_proximal",
            date_onset="2026-05-18",
            rehab_phase=RehabPhase.SUBACUTE,
            current_pain_score=2,
            contraindicated_movements=["maximal_sprints", "hill_sprints"],
            safe_alternative_protocols=["isometric_prone_knee_flexion_30deg"]
        )
        assert inj.is_active is True
        assert inj.is_severe is False

        severe_inj = InjuryRecord(
            injury_id="inj_test_02",
            injury_name="Acute Hamstring Tear",
            anatomical_region="hamstring_proximal",
            date_onset="2026-08-20",
            rehab_phase=RehabPhase.ACUTE,
            current_pain_score=8,
            contraindicated_movements=["all_running"]
        )
        assert severe_inj.is_severe is True

    def test_recovery_metrics_autonomic_crash(self):
        normal = RecoveryMetrics(
            date="2026-08-26",
            morning_hrv_rmssd=68.0,
            hrv_baseline_7d=70.0,
            resting_heart_rate=45,
            rhr_baseline_7d=44,
            sleep_hours=8.0
        )
        assert normal.is_autonomic_crash() is False
        assert normal.hrv_drop_percentage() < 5.0

        crash = RecoveryMetrics(
            date="2026-08-26",
            morning_hrv_rmssd=34.0,
            hrv_baseline_7d=68.0,
            resting_heart_rate=58,
            rhr_baseline_7d=46,
            sleep_hours=4.25
        )
        assert crash.is_autonomic_crash() is True
        assert crash.hrv_drop_percentage() == 50.0

    def test_banister_trimp_calculation(self):
        bio = BiometricState()
        # Test male calculation
        male_trimp = bio.calculate_banister_trimp(
            duration_min=60.0,
            avg_hr=160.0,
            rest_hr=45.0,
            max_hr=200.0,
            sex=Sex.MALE
        )
        # Test female calculation
        female_trimp = bio.calculate_banister_trimp(
            duration_min=60.0,
            avg_hr=160.0,
            rest_hr=45.0,
            max_hr=200.0,
            sex=Sex.FEMALE
        )
        assert male_trimp > 0.0
        assert female_trimp > 0.0
        assert male_trimp != female_trimp

        # Test boundary cases (zero duration, negative reserve)
        assert bio.calculate_banister_trimp(0, 160, 45, 200) == 0.0
        assert bio.calculate_banister_trimp(60, 40, 50, 200) == 0.0

    def test_ctl_atl_tsb_acwr_calculations(self):
        bio = BiometricState()
        workout_loads = [40.0, 50.0, 60.0, 70.0, 80.0, 100.0, 140.0]

        ctl = bio.calculate_ctl(workout_loads)
        atl = bio.calculate_atl(workout_loads)
        tsb = bio.calculate_tsb(ctl, atl)
        acwr = bio.calculate_acwr(atl, ctl)

        assert ctl > 0
        assert atl > ctl  # Recent heavy loads increase acute load faster than chronic
        assert tsb == round(ctl - atl, 2)
        assert acwr == round(atl / ctl, 2)

        risk = bio.get_acwr_risk_assessment(atl=140.0, ctl=80.0)
        assert risk["acwr"] == 1.75
        assert risk["zone"] == "DANGER_ZONE"
        assert risk["is_dangerous"] is True

    def test_athlete_profile_contraindication_matching(self):
        athlete = AthleteProfile(
            athlete_id="ath_test_01",
            tenant_id="tenant_test",
            name="Test Athlete",
            age=24,
            height_cm=175.0,
            weight_kg=60.0,
            primary_discipline=SportDiscipline.TRACK_800M,
            max_heart_rate=200,
            resting_heart_rate=45,
            injuries=[
                InjuryRecord(
                    injury_id="inj_01",
                    injury_name="Hamstring Strain",
                    anatomical_region="hamstring_proximal",
                    date_onset="2026-05-01",
                    rehab_phase=RehabPhase.SUBACUTE,
                    current_pain_score=2,
                    contraindicated_movements=["maximal_sprint", "hill_sprint_100pct"]
                )
            ]
        )
        assert len(athlete.active_contraindications) == 2
        assert athlete.has_contraindication_for("maximal_sprint") is True
        assert athlete.has_contraindication_for("hill_sprint_100pct") is True
        assert athlete.has_contraindication_for("easy_jogging") is False

        # Resolve injury
        assert athlete.resolve_injury("inj_01") is True
        assert len(athlete.active_contraindications) == 0


class TestM3DataFiles:
    def test_medical_knowledge_json(self):
        cfg = get_config()
        with open(cfg.medical_knowledge_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert isinstance(data, list)
        assert len(data) >= 7

        required_keys = {"chunk_id", "title", "content", "category", "target_anatomy", "contraindications", "evidence_level", "citations"}
        for item in data:
            assert required_keys.issubset(item.keys()), f"Missing keys in {item.get('chunk_id')}"

        # Verify key sports science topics are covered
        titles = [item["title"].lower() for item in data]
        contents = [item["content"].lower() for item in data]
        all_text = " ".join(titles + contents)

        assert "askling" in all_text or "hamstring" in all_text
        assert "alfredson" in all_text or "achilles" in all_text
        assert "spanish squat" in all_text or "patellar" in all_text
        assert "mcgill" in all_text or "lumbar" in all_text
        assert "carbohydrate" in all_text or "fodmap" in all_text
        assert "altitude" in all_text or "hypoxia" in all_text
        assert "pap" in all_text or "potentiation" in all_text

    def test_user_profiles_json(self):
        cfg = get_config()
        with open(cfg.user_profiles_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) >= 5
        profiles = [AthleteProfile(**item) for item in data]
        carlos = next(p for p in profiles if p.athlete_id == "ath_carlos_001")
        assert carlos.tenant_id == "tenant_carlos_800m"
        assert len(carlos.injuries) >= 1

    def test_sample_workouts_json(self):
        cfg = get_config()
        with open(cfg.sample_workouts_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert len(data) >= 5
        for w in data:
            assert "workout_id" in w
            assert "activity_type" in w
            assert "duration_minutes" in w


class TestM3RAG:
    def test_deterministic_embedding_adapter(self):
        adapter = DeterministicEmbeddingAdapter(dimension=128)

        v1 = adapter.embed_text("Rehabilitación unión miotendinosa isquiotibial Askling HSR")
        v2 = adapter.embed_text("Proximal hamstring strain recovery protocol")
        v3 = adapter.embed_text("Protocolo de carga de hidratos maratón low fodmap")

        assert len(v1) == 128
        assert len(v2) == 128
        assert len(v3) == 128

        # L2 norm must be approximately 1.0
        import numpy as np
        assert abs(np.linalg.norm(v1) - 1.0) < 1e-4

        sim_hamstrings = VectorStore.compute_cosine_similarity(np.array(v1), np.array(v2))
        sim_unrelated = VectorStore.compute_cosine_similarity(np.array(v1), np.array(v3))

        assert sim_hamstrings > sim_unrelated
        assert sim_hamstrings > 0.40

    def test_vector_store_ingestion_and_search(self):
        vs = VectorStore()
        count = vs.ingest_default_knowledge()
        assert count >= 7

        # Search without filter
        results = vs.search(query="Isquiotibial Askling ejercicios", top_k=3)
        assert len(results) > 0
        assert "hamstring" in results[0][0].target_anatomy or "hamstring_proximal" in results[0][0].target_anatomy

    def test_vector_store_metadata_filtering(self):
        vs = VectorStore()
        vs.ingest_default_knowledge()

        # Anatomical filter
        res_patellar = vs.search(
            query="Dolor de rodilla al bajar",
            filter_anatomy=["patellar_tendon"],
            top_k=2
        )
        assert len(res_patellar) > 0
        for chunk, score in res_patellar:
            assert "patellar_tendon" in chunk.target_anatomy

        # Contraindication purge
        res_filtered = vs.search(
            query="Rehabilitación isquiotibial",
            exclude_contraindications=["acute_hamstring_tear", "maximal_sprint"],
            top_k=5
        )
        for chunk, score in res_filtered:
            for contra in chunk.contraindications:
                assert contra != "maximal_sprint"

    def test_hybrid_retriever_and_citations(self):
        hr = HybridRetriever()
        results = hr.retrieve(
            query="Protocolo Stuart McGill para hernia discal lumbar y peso muerto",
            top_k=2
        )
        assert len(results) > 0
        chunk, score = results[0]
        assert "lumbar" in chunk.chunk_id or "lumbar_spine" in chunk.target_anatomy

        formatted = hr.format_clinical_context(results)
        assert "Sports Science & Clinical Evidence Context" in formatted
        assert "McGill" in formatted or "Adams" in formatted


class TestM3Tenancy:
    def test_tenant_context_scoping(self):
        clear_current_tenant()
        assert get_current_tenant() is None

        with TenantContext("tenant_carlos_800m"):
            assert get_current_tenant() == "tenant_carlos_800m"

            # Nested context
            with TenantContext("tenant_elena_marathon"):
                assert get_current_tenant() == "tenant_elena_marathon"

            # Restored outer
            assert get_current_tenant() == "tenant_carlos_800m"

        assert get_current_tenant() is None

    def test_tenant_security_manager_tokens(self):
        sec = TenantSecurityManager()
        token = sec.generate_tenant_token("tenant_carlos_800m")
        assert isinstance(token, str)

        verified = sec.verify_tenant_token(token)
        assert verified == "tenant_carlos_800m"

        # Tampered token
        tampered = token[:-4] + "abcd"
        with pytest.raises(TenantSecurityError):
            sec.verify_tenant_token(tampered)

    def test_tenant_isolation_assertions(self):
        sec = TenantSecurityManager()

        with TenantContext("tenant_carlos_800m"):
            # Access own resource
            sec.assert_tenant_access("tenant_carlos_800m")

            # Cross-tenant access must raise TenantIsolationError
            with pytest.raises(TenantIsolationError):
                sec.assert_tenant_access("tenant_elena_marathon")

    def test_vector_store_tenant_isolation(self):
        vs = VectorStore()
        vs.clear()

        # Global chunk
        vs.add_chunk(KnowledgeChunk(
            chunk_id="global_chunk_01",
            title="Global Sports Nutrition",
            content="General hydration guidelines",
            tenant_id=None
        ))

        # Tenant A chunk
        vs.add_chunk(KnowledgeChunk(
            chunk_id="tenant_a_private_01",
            title="Carlos Private Hamstring Protocol",
            content="Custom clinic notes from Dr. Martinez",
            tenant_id="tenant_carlos_800m"
        ))

        # Tenant B chunk
        vs.add_chunk(KnowledgeChunk(
            chunk_id="tenant_b_private_01",
            title="Elena Private Marathon Plan",
            content="Custom pacing notes for Valencia Marathon",
            tenant_id="tenant_elena_marathon"
        ))

        # Query as Tenant A -> Should see global + Tenant A, NOT Tenant B
        res_a = vs.search(query="notes", tenant_id="tenant_carlos_800m", top_k=5)
        cids_a = [c.chunk_id for c, _ in res_a]
        assert "global_chunk_01" in cids_a
        assert "tenant_a_private_01" in cids_a
        assert "tenant_b_private_01" not in cids_a

        # Query as Tenant B -> Should see global + Tenant B, NOT Tenant A
        res_b = vs.search(query="notes", tenant_id="tenant_elena_marathon", top_k=5)
        cids_b = [c.chunk_id for c, _ in res_b]
        assert "global_chunk_01" in cids_b
        assert "tenant_b_private_01" in cids_b
        assert "tenant_a_private_01" not in cids_b
