## 2026-08-26T20:04:17Z

**Assignment**: Implement Milestone M3 — PoC Core Engine, Data Models & Sports Science RAG.
**Working Directory**: `c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\worker_m3`
**Parent Agent**: `orchestrator_1` (`a66dfe4b-740c-46bd-bcd7-21f2cd29b6f3`)

**Files Owned Exclusively**:
- `poc/config.py`
- `poc/models/__init__.py`
- `poc/models/athlete.py`
- `poc/models/conversation.py`
- `poc/data/medical_knowledge.json`
- `poc/data/sample_workouts.json`
- `poc/data/user_profiles.json`
- `poc/rag/__init__.py`
- `poc/rag/embeddings.py`
- `poc/rag/vector_store.py`
- `poc/rag/retriever.py`
- `poc/tenancy/__init__.py`
- `poc/tenancy/context.py`
- `poc/tenancy/security.py`

**Key Requirements**:
1. `poc/config.py`: Global configuration, settings, support for `MOCK_MODE` (offline deterministic execution on Windows with zero external cloud dependencies) and `LIVE_MODE` (OpenAI/Anthropic provider when configured).
2. `poc/models/athlete.py`: Pydantic / Dataclass models for `AthleteProfile`, `InjuryRecord`, `RecoveryMetrics`, `BiometricState` (including Banister TRIMP, CTL, ATL, TSB, ACWR calculation methods).
3. `poc/models/conversation.py`: Models for `UserQuery`, `DomainIntent`, `AgentResponse`, `ExecutionTrace`, `SafetyViolation`.
4. `poc/data/medical_knowledge.json`: Rich sports science and clinical rehabilitation protocol dataset covering:
   - Proximal hamstring strain & Askling H-protocol / HSR protocols.
   - Achilles tendinopathy & Alfredson eccentric loading.
   - Patellar tendinopathy & Spanish squats / isometrics.
   - Lumbar disc herniation / McGill Big 3 & neutral spine protocols.
   - Marathon carbohydrate loading (Burke et al.) & Low-FODMAP guidance.
   - Altitude acclimatization & hydration.
   - Post-Activation Potentiation (PAP) for 800m track runners.
5. `poc/data/sample_workouts.json` & `poc/data/user_profiles.json`: Multi-tenant user profiles (e.g. Carlos 800m/trail hamstring profile, marathoner profile, overtrained profile, strength profile).
6. `poc/rag/embeddings.py`: Dual-mode embedding provider:
   - `DeterministicEmbeddingAdapter`: Hash/TF-IDF vectorizer producing stable normalized cosine embeddings offline.
   - `OpenAIEmbeddingAdapter`: Live provider.
7. `poc/rag/vector_store.py`: Vector store implementation with cosine similarity math, chunk ingestion, and hard metadata filtering (`filter_anatomy`, `exclude_contraindications`, `rehab_phase`).
8. `poc/rag/retriever.py`: Hybrid search retriever with metadata filtering, score boosting, and clinical citation formatting.
9. `poc/tenancy/context.py` & `poc/tenancy/security.py`: `TenantContext` manager and token/isolation security rules ensuring zero cross-tenant data leakage.
