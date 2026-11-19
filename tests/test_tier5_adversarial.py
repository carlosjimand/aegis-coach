"""
Aegis Coach — Tier 5 Adversarial & Security Boundary Stress Test Suite
=======================================================================
Empirical challenger probe suite testing:
1. Adversarial Vector RAG & Semantic Precision:
   - Extreme, pathological, fuzz, and foreign-script queries.
   - Conflicting, non-existent, and contradictory anatomical metadata filters.
   - Semantic negation and contraindication bypass attempts.
   - Mathematical edge cases: zero vectors, boundary alphas, high top_k, empty store.
2. Multi-Tenant Security & Isolation Boundaries:
   - Cross-tenant data leakage probes across vector stores, contexts, and profiles.
   - HMAC token tampering, spoofing, bit-flipping, expired tokens, and malformed structures.
   - Missing, unscoped, and nested tenant execution contexts.
   - High-concurrency async and multithreaded multi-tenant stress testing.
"""

import time
import base64
import json
import hmac
import hashlib
import asyncio
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import pytest
from typing import List, Dict, Any

from poc.config import get_config
from poc.rag.embeddings import DeterministicEmbeddingAdapter, get_embedding_adapter
from poc.rag.vector_store import VectorStore, KnowledgeChunk
from poc.rag.retriever import HybridRetriever
from poc.tenancy.context import (
    TenantContext,
    TenantIsolationError,
    TenantSecurityError,
    get_current_tenant,
    set_current_tenant,
    clear_current_tenant,
)
from poc.tenancy.security import TenantSecurityManager
from poc.models.athlete import AthleteProfile, InjuryRecord, RehabPhase, Sex, SportDiscipline


# ============================================================================
# Category 1: Adversarial Vector RAG, Semantic Precision & Metadata Filtering
# ============================================================================

class TestAdversarialVectorRAG:
    """Stress-testing Vector Store, Embedding Engine, and Hybrid Retriever."""

    @pytest.fixture(autouse=True)
    def setup_rag(self):
        self.store = VectorStore()
        self.store.ingest_default_knowledge()
        self.retriever = HybridRetriever(vector_store=self.store)

    # 1.1 Extreme & Pathological Queries
    @pytest.mark.parametrize("extreme_query, desc", [
        ("", "Empty string"),
        ("   \t\n\r  ", "Whitespace only"),
        ("!@#$%^&*()_+-=[]{}|;:',.<>?/`~", "Pure special characters"),
        ("a" * 10000, "10k repeated single character"),
        ("SELECT * FROM chunks WHERE 1=1; DROP TABLE users; --", "SQL injection payload"),
        ("(?=.*[a-z])(?=.*[A-Z])(?=.*\\d).*", "Regex pattern bomb"),
        ("🏃‍♂️🏋️‍♀️🚴‍♂️🔥💥🩺⚡", "Pure emoji string"),
        ("Протокол реабилитации подколенного сухожилия", "Russian Cyrillic sports medicine query"),
        ("بروتوكول إعادة تأهيل وتر العرقوب", "Arabic sports medicine query"),
        ("腘绳肌肌腱病康复方案与离心力量训练", "Chinese sports medicine query"),
    ])
    def test_adv_rag_01_extreme_and_pathological_queries(self, extreme_query: str, desc: str):
        """Vector RAG must handle extreme and pathological input strings without crashing or producing NaN."""
        results = self.store.search(extreme_query, top_k=3)
        assert isinstance(results, list), f"Expected list for {desc}, got {type(results)}"

        # Verify no NaN or Inf in scores
        for chunk, score in results:
            assert not np.isnan(score), f"Score is NaN for query '{desc}'"
            assert not np.isinf(score), f"Score is Infinite for query '{desc}'"
            assert isinstance(chunk.title, str)

        # Test hybrid retriever with same extreme query
        hybrid_res = self.retriever.retrieve(extreme_query, top_k=3)
        assert isinstance(hybrid_res, list)
        formatted = self.retriever.format_clinical_context(hybrid_res)
        assert isinstance(formatted, str)

    # 1.2 Conflicting & Non-Existent Anatomical Filters
    def test_adv_rag_02_conflicting_and_alien_anatomical_filters(self):
        """Testing disparate anatomical regions, case mismatches, dirty whitespace, and alien anatomy."""
        # Non-existent alien anatomy
        alien_results = self.store.search("rehab protocol", filter_anatomy=["alien_telepathic_cortex"])
        assert len(alien_results) == 0, "Alien anatomy must return zero results"

        # Dirty whitespace and irregular casing on valid anatomy
        messy_results = self.store.search(
            "hamstring",
            filter_anatomy=["   hAmStRiNg_pRoXiMaL   "]
        )
        assert len(messy_results) > 0, "Anatomical filter must be robust to whitespace and case variations"
        for chunk, _ in messy_results:
            assert any("hamstring" in a.lower() for a in chunk.target_anatomy)

        # Multi-anatomy disjoint filter
        disjoint_results = self.store.search(
            "pain protocol",
            filter_anatomy=["hamstring_proximal", "lumbar_spine"]
        )
        assert len(disjoint_results) > 0
        for chunk, _ in disjoint_results:
            anatomy_match = any(
                "hamstring" in a.lower() or "lumbar" in a.lower() or "spine" in a.lower()
                for a in chunk.target_anatomy
            )
            assert anatomy_match, "Returned chunk did not match any of the filtered anatomical regions"

    # 1.3 Contradictory Filter: Requesting Anatomy while Contraindicating its Core Movements
    def test_adv_rag_03_contradictory_anatomical_and_contraindication_filter(self):
        """
        Adversarial test: athlete requests hamstring rehab while actively contraindicating all hamstring loading.
        The hard contraindication purge MUST take precedence over anatomical relevance.
        """
        results = self.store.search(
            query="hamstring high velocity sprint protocol",
            filter_anatomy=["hamstring_proximal"],
            exclude_contraindications=["sprints_maximos", "sprint", "explosive", "high_velocity"]
        )
        for chunk, _ in results:
            for contra in chunk.contraindications:
                assert "sprint" not in contra.lower()
                assert "explosive" not in contra.lower()

    # 1.4 Semantic Negation & Attack Queries
    def test_adv_rag_04_semantic_negation_and_negative_intent(self):
        """
        Adversarial prompt injection / negative intent: Athlete asks for 'exercises without hamstring strain'.
        Verifies retriever returns valid clinical guidance and filters out contraindicated exercises.
        """
        carlos_profile = AthleteProfile(
            athlete_id="ath_carlos_adv",
            tenant_id="tenant_carlos_800m",
            name="Carlos Negation Test",
            age=28,
            gender=Sex.MALE,
            height_cm=180.0,
            weight_kg=71.0,
            primary_discipline=SportDiscipline.TRACK_800M,
            injuries=[
                InjuryRecord(
                    injury_id="inj_hamstring_adv",
                    injury_name="Biceps Femoris Acute Strain",
                    anatomical_region="hamstring_proximal",
                    date_onset="2026-08-01",
                    rehab_phase=RehabPhase.ACUTE,
                    current_pain_score=4,
                    contraindicated_movements=["sprints_maximos", "high_velocity_sprinting", "heavy_deadlift"],
                    safe_alternative_protocols=["Askling L-Protocol", "Prone Hamstring Isometrics"]
                )
            ]
        )

        results = self.retriever.retrieve(
            query="Dame un entrenamiento de velocidad máxima y sprints a tope a pesar de mi dolor",
            athlete=carlos_profile,
            top_k=3
        )

        # All results must NOT contain prohibited contraindications
        for chunk, score in results:
            for contra in chunk.contraindications:
                assert "sprints_maximos" not in contra.lower()
                assert "high_velocity" not in contra.lower()

    # 1.5 Mathematical Boundary & Numerical Stability
    def test_adv_rag_05_mathematical_boundaries_and_zero_store(self):
        """Test zero-chunk store, boundary top_k, and alpha extremes."""
        empty_store = VectorStore()
        assert empty_store.search("test query", top_k=5) == []

        empty_retriever = HybridRetriever(vector_store=empty_store)
        # Empty retriever should auto-ingest default knowledge, so let's clear it explicitly
        empty_store.clear()
        assert empty_store.search("test query") == []

        # Boundary top_k
        assert len(self.store.search("achilles", top_k=0)) == 0
        all_res = self.store.search("achilles", top_k=1000)
        assert len(all_res) <= len(self.store.chunks)

        # Extreme alpha weights
        dense_only_retriever = HybridRetriever(vector_store=self.store, alpha=1.0)
        sparse_only_retriever = HybridRetriever(vector_store=self.store, alpha=0.0)

        r_dense = dense_only_retriever.retrieve("achilles tendinopathy", top_k=3)
        r_sparse = sparse_only_retriever.retrieve("achilles tendinopathy", top_k=3)

        assert len(r_dense) > 0
        assert len(r_sparse) > 0
        for _, s in r_dense:
            assert not np.isnan(s)
        for _, s in r_sparse:
            assert not np.isnan(s)


# ============================================================================
# Category 2: Multi-Tenant Security & Isolation Boundaries
# ============================================================================

class TestAdversarialMultiTenancy:
    """Stress-testing Tenant Isolation, Security Manager, HMAC Tokens, and Concurrency."""

    @pytest.fixture(autouse=True)
    def setup_security(self):
        self.sec = TenantSecurityManager(secret_key="challenger_ultra_secure_secret_key_123!")
        self.store = VectorStore()
        self.store.ingest_default_knowledge()

        # Ingest private tenant chunks
        self.chunk_tenant_a = KnowledgeChunk(
            chunk_id="chunk_secret_carlos",
            title="Carlos Private 800m Lactate Diagnostics",
            content="Proprietary vVO2max and 800m split curves for Carlos.",
            category="PHYSIOLOGY",
            tenant_id="tenant_carlos_800m"
        )
        self.chunk_tenant_b = KnowledgeChunk(
            chunk_id="chunk_secret_elena",
            title="Elena Private UTMB Trail Nutrition Strategy",
            content="Proprietary sodium and carbohydrate loading for Elena UTMB 100M.",
            category="NUTRITION",
            tenant_id="tenant_elena_trail"
        )
        self.store.add_chunk(self.chunk_tenant_a)
        self.store.add_chunk(self.chunk_tenant_b)

    # 2.1 Unauthorized Cross-Tenant Vector Store Infiltration
    def test_adv_ten_01_cross_tenant_vector_leakage_probes(self):
        """Tenant A must NEVER see Tenant B's private knowledge chunks under any query string."""
        # Query specifically targeting Elena's chunk title and content while authenticated as Carlos
        results_carlos = self.store.search(
            query="Elena Private UTMB Trail Nutrition Strategy sodium carbohydrate",
            top_k=10,
            tenant_id="tenant_carlos_800m"
        )
        returned_ids_carlos = [c.chunk_id for c, _ in results_carlos]
        assert "chunk_secret_elena" not in returned_ids_carlos, "CRITICAL: Tenant Carlos accessed Elena's private chunk!"

        # Query specifically targeting Carlos's chunk while authenticated as Elena
        results_elena = self.store.search(
            query="Carlos Private 800m Lactate Diagnostics vVO2max",
            top_k=10,
            tenant_id="tenant_elena_trail"
        )
        returned_ids_elena = [c.chunk_id for c, _ in results_elena]
        assert "chunk_secret_carlos" not in returned_ids_elena, "CRITICAL: Tenant Elena accessed Carlos's private chunk!"

        # Unauthenticated / unscoped search must only return global base chunks (tenant_id is None)
        results_unscoped = self.store.search(
            query="Private UTMB Lactate",
            top_k=10,
            tenant_id=None
        )
        returned_ids_unscoped = [c.chunk_id for c, _ in results_unscoped]
        assert "chunk_secret_carlos" not in returned_ids_unscoped
        assert "chunk_secret_elena" not in returned_ids_unscoped

    # 2.2 HMAC Token Spoofing, Forgery & Tampering
    def test_adv_ten_02_hmac_token_tampering_and_spoofing(self):
        """Attempting various cryptographic and structural attacks on tenant tokens."""
        valid_token_carlos = self.sec.generate_tenant_token("tenant_carlos_800m")
        verified_tenant = self.sec.verify_tenant_token(valid_token_carlos)
        assert verified_tenant == "tenant_carlos_800m"

        # Attack 1: Payload Tampering (Attempting to impersonate Elena using Carlos's signature)
        payload_b64, signature = valid_token_carlos.split(".")
        decoded_payload = json.loads(base64.urlsafe_b64decode(payload_b64.encode("utf-8")).decode("utf-8"))
        decoded_payload["tenant_id"] = "tenant_elena_trail"
        tampered_payload_b64 = base64.urlsafe_b64encode(
            json.dumps(decoded_payload, sort_keys=True).encode("utf-8")
        ).decode("utf-8")
        tampered_token = f"{tampered_payload_b64}.{signature}"

        with pytest.raises(TenantSecurityError, match="Invalid token signature"):
            self.sec.verify_tenant_token(tampered_token)

        # Attack 2: Rogue Secret Signature
        rogue_sec = TenantSecurityManager(secret_key="attacker_rogue_secret_key")
        forged_token = rogue_sec.generate_tenant_token("tenant_carlos_800m")
        with pytest.raises(TenantSecurityError, match="Invalid token signature"):
            self.sec.verify_tenant_token(forged_token)

        # Attack 3: Expired Token
        expired_token = self.sec.generate_tenant_token("tenant_carlos_800m", ttl_seconds=-60)
        with pytest.raises(TenantSecurityError, match="expired"):
            self.sec.verify_tenant_token(expired_token)

        # Attack 4: Malformed Structures
        malformed_inputs = [
            "",
            "   ",
            "no_dot_token",
            "a.b.c.d",
            "invalid_b64!@#$.signature",
            "null.null",
            "eyJhbGciOiJIUzI1NiJ9.sig",
        ]
        for bad_tok in malformed_inputs:
            with pytest.raises(TenantSecurityError):
                self.sec.verify_tenant_token(bad_tok)

    # 2.3 Athlete Profile Cross-Tenant Authorization Assertions
    def test_adv_ten_03_athlete_profile_cross_tenant_access(self):
        """Strict validation that an athlete profile cannot be accessed or mutated outside their tenant."""
        carlos_profile = AthleteProfile(
            athlete_id="ath_carlos_1",
            tenant_id="tenant_carlos_800m",
            name="Carlos",
            age=28,
            gender=Sex.MALE,
            height_cm=180.0,
            weight_kg=71.0,
            primary_discipline=SportDiscipline.TRACK_800M
        )

        # Valid active context matching Carlos
        with TenantContext("tenant_carlos_800m"):
            self.sec.validate_athlete_profile_access(carlos_profile)
            self.sec.assert_tenant_access(target_tenant_id="tenant_carlos_800m")

        # Unauthorized access from Elena's context
        with TenantContext("tenant_elena_trail"):
            with pytest.raises(TenantIsolationError, match="Security Violation"):
                self.sec.validate_athlete_profile_access(carlos_profile)

            with pytest.raises(TenantIsolationError, match="Security Violation"):
                self.sec.assert_tenant_access(target_tenant_id="tenant_carlos_800m")

    # 2.4 Nested Tenant Context Scoping & Restoration
    def test_adv_ten_04_nested_tenant_context_restoration(self):
        """Testing that nested TenantContext blocks properly isolate and restore upon exit."""
        clear_current_tenant()
        assert get_current_tenant() is None

        with TenantContext("tenant_alpha"):
            assert get_current_tenant() == "tenant_alpha"
            with TenantContext("tenant_beta"):
                assert get_current_tenant() == "tenant_beta"
                with TenantContext("tenant_gamma"):
                    assert get_current_tenant() == "tenant_gamma"
                assert get_current_tenant() == "tenant_beta"
            assert get_current_tenant() == "tenant_alpha"

        assert get_current_tenant() is None

    # 2.5 Concurrent Multi-Tenant Async Stress Test (100 Coroutines)
    def test_adv_ten_05_concurrent_multitenant_async_stress(self):
        """
        High-load empirical concurrency probe:
        Spawns 100 concurrent async coroutines representing 10 distinct tenants executing
        simultaneous vector searches, profile validations, and token verifications.
        Verifies zero ContextVar bleed and 100% tenant boundary isolation under race conditions.
        """
        num_tenants = 10
        tasks_per_tenant = 10
        tenants = [f"tenant_async_{i:02d}" for i in range(num_tenants)]

        # Pre-generate tokens and private chunks for each tenant
        tokens = {t: self.sec.generate_tenant_token(t) for t in tenants}
        for t in tenants:
            self.store.add_chunk(KnowledgeChunk(
                chunk_id=f"chunk_priv_async_{t}",
                title=f"Private Data for {t}",
                content=f"Confidential physiological metrics for {t}",
                category="BIOMECHANICS",
                tenant_id=t
            ))

        isolation_failures: List[str] = []

        async def tenant_worker(tenant_id: str, worker_id: int):
            token = tokens[tenant_id]

            # 1. Verify token
            verified = self.sec.verify_tenant_token(token)
            if verified != tenant_id:
                isolation_failures.append(f"Worker {worker_id}: Token verification mismatch {verified} != {tenant_id}")

            # 2. Scope execution context
            with TenantContext(tenant_id):
                active_t = get_current_tenant(strict=True)
                if active_t != tenant_id:
                    isolation_failures.append(f"Worker {worker_id}: ContextVar mismatch {active_t} != {tenant_id}")

                # Simulate async I/O delay to induce event loop context switching
                await asyncio.sleep(0.002)

                # 3. Vector search inside tenant context
                results = self.store.search(
                    query="Confidential physiological metrics",
                    top_k=5,
                    tenant_id=tenant_id
                )
                chunk_ids = [c.chunk_id for c, _ in results]

                # Verify worker CAN see its own private chunk
                if f"chunk_priv_async_{tenant_id}" not in chunk_ids:
                    isolation_failures.append(f"Worker {worker_id}: Failed to find own private chunk")

                # Verify worker CANNOT see any other tenant's private chunks
                for other_t in tenants:
                    if other_t != tenant_id and f"chunk_priv_async_{other_t}" in chunk_ids:
                        isolation_failures.append(f"CRITICAL LEAK in Worker {worker_id}: Found {other_t} data in {tenant_id} search!")

                # 4. Profile validation
                dummy_profile = AthleteProfile(
                    athlete_id=f"ath_{tenant_id}",
                    tenant_id=tenant_id,
                    name=f"Athlete {tenant_id}",
                    age=30,
                    gender=Sex.MALE,
                    height_cm=175.0,
                    weight_kg=70.0,
                    primary_discipline=SportDiscipline.ROAD_RUNNING
                )
                self.sec.validate_athlete_profile_access(dummy_profile)

        async def _run_all():
            tasks = []
            for i, t in enumerate(tenants):
                for w in range(tasks_per_tenant):
                    tasks.append(tenant_worker(t, i * tasks_per_tenant + w))
            await asyncio.gather(*tasks)

        asyncio.run(_run_all())
        assert len(isolation_failures) == 0, f"Encountered {len(isolation_failures)} async isolation failures:\n" + "\n".join(isolation_failures[:10])

    # 2.6 Multi-Threaded Parallel Tenant Isolation Stress Test (20 Threads)
    def test_adv_ten_06_multithreaded_tenant_isolation_stress(self):
        """
        Multithreaded empirical concurrency probe:
        Runs 20 worker threads in a ThreadPoolExecutor performing 100 iterations each of tenant context switching
        and vector retrieval to confirm thread-local ContextVar isolation.
        """
        num_threads = 20
        iterations_per_thread = 50
        thread_failures: List[str] = []

        def worker_thread(thread_idx: int):
            tenant_id = f"thread_tenant_{thread_idx:02d}"
            token = self.sec.generate_tenant_token(tenant_id)

            for it in range(iterations_per_thread):
                # 1. Token validation
                v_t = self.sec.verify_tenant_token(token)
                if v_t != tenant_id:
                    thread_failures.append(f"Thread {thread_idx} it {it}: token mismatch {v_t} != {tenant_id}")

                # 2. Scoped context check
                with TenantContext(tenant_id):
                    curr = get_current_tenant()
                    if curr != tenant_id:
                        thread_failures.append(f"Thread {thread_idx} it {it}: contextvar mismatch {curr} != {tenant_id}")

                    # Micro sleep to allow thread scheduling
                    time.sleep(0.0001)

                    # Vector search
                    res = self.store.search("hamstring", top_k=3, tenant_id=tenant_id)
                    if not isinstance(res, list):
                        thread_failures.append(f"Thread {thread_idx} it {it}: search did not return list")

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [executor.submit(worker_thread, idx) for idx in range(num_threads)]
            for f in futures:
                f.result()

        assert len(thread_failures) == 0, f"Encountered {len(thread_failures)} thread isolation failures:\n" + "\n".join(thread_failures[:10])
