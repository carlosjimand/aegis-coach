"""
Aegis Coach — Vector Knowledge Store
====================================
Vector store implementation with cosine similarity math, chunk ingestion,
tenant-scoped namespaces, and clinical metadata filtering (anatomy, contraindications, rehab phase).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union
import numpy as np
from pydantic import BaseModel, Field

from poc.config import get_config
from poc.rag.embeddings import BaseEmbeddingAdapter, get_embedding_adapter


class KnowledgeChunk(BaseModel):
    """Structured clinical sports science literature chunk."""

    chunk_id: str = Field(..., description="Unique chunk identifier.")
    title: str = Field(..., description="Descriptive title of the protocol or study.")
    content: str = Field(..., description="Full text body with protocol details.")
    category: str = Field(
        default="REHABILITATION",
        description="Category (REHABILITATION, BIOMECHANICS, NUTRITION, PERIODIZATION, PHYSIOLOGY, SAFETY_TRIAGE)."
    )
    discipline: Optional[str] = Field(
        default=None,
        description="Applicable sport discipline (TRACK_800M, TRAIL_RUNNING, MARATHON, etc.)."
    )
    target_anatomy: List[str] = Field(
        default_factory=list,
        description="Anatomical structures addressed (e.g. 'hamstring_proximal', 'achilles_tendon')."
    )
    contraindications: List[str] = Field(
        default_factory=list,
        description="Pathologies or movements where this protocol is contraindicated or dangerous."
    )
    rehab_phase: Optional[str] = Field(
        default=None,
        description="Clinical phase (ACUTE, SUBACUTE, REMODELING, RETURN_TO_SPORT, MAINTENANCE)."
    )
    evidence_level: str = Field(
        default="CLINICAL_GUIDELINE",
        description="Evidence grade (SYSTEMATIC_REVIEW, RCT, CLINICAL_GUIDELINE, EXPERT_CONSENSUS)."
    )
    citations: List[Dict[str, str]] = Field(default_factory=list, description="Academic citations.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom properties & parameters.")
    embedding: Optional[List[float]] = Field(default=None, description="Dense vector embedding.")
    tenant_id: Optional[str] = Field(
        default=None,
        description="Optional tenant ID. If None, chunk is globally available in the sports medicine base."
    )


class VectorStore:
    """
    In-memory vector store providing high-performance cosine similarity search
    with strict multi-tenant isolation and clinical metadata pre-filtering.
    """

    def __init__(self, embedding_adapter: Optional[BaseEmbeddingAdapter] = None):
        self.config = get_config()
        self.embedding_adapter = embedding_adapter or get_embedding_adapter()
        self.chunks: Dict[str, KnowledgeChunk] = {}
        self._vectors: Optional[np.ndarray] = None
        self._chunk_id_list: List[str] = []

    def _rebuild_index(self) -> None:
        """Rebuilds the NumPy array index for vector matrix operations."""
        self._chunk_id_list = list(self.chunks.keys())
        if not self._chunk_id_list:
            self._vectors = None
            return

        vector_list = []
        for cid in self._chunk_id_list:
            chunk = self.chunks[cid]
            if chunk.embedding is None:
                # Generate embedding if missing
                chunk.embedding = self.embedding_adapter.embed_text(f"{chunk.title} {chunk.content}")
            vector_list.append(chunk.embedding)

        self._vectors = np.array(vector_list, dtype=np.float64)

    def add_chunk(self, chunk: KnowledgeChunk) -> None:
        """Adds a single chunk and re-indexes."""
        if chunk.embedding is None:
            chunk.embedding = self.embedding_adapter.embed_text(f"{chunk.title} {chunk.content}")
        self.chunks[chunk.chunk_id] = chunk
        self._rebuild_index()

    def add_chunks(self, chunks: List[KnowledgeChunk]) -> int:
        """Adds multiple chunks and re-indexes once."""
        texts_to_embed = []
        chunks_needing_embed = []

        for chunk in chunks:
            if chunk.embedding is None:
                texts_to_embed.append(f"{chunk.title} {chunk.content}")
                chunks_needing_embed.append(chunk)

        if texts_to_embed:
            embeddings = self.embedding_adapter.embed_batch(texts_to_embed)
            for c, emb in zip(chunks_needing_embed, embeddings):
                c.embedding = emb

        for chunk in chunks:
            self.chunks[chunk.chunk_id] = chunk

        self._rebuild_index()
        return len(chunks)

    def ingest_json_file(self, file_path: Union[str, Path], tenant_id: Optional[str] = None) -> int:
        """Loads knowledge chunks from a JSON dataset file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Knowledge dataset file not found at: {path}")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        chunks: List[KnowledgeChunk] = []
        for item in data:
            if tenant_id is not None and "tenant_id" not in item:
                item["tenant_id"] = tenant_id
            chunks.append(KnowledgeChunk(**item))

        return self.add_chunks(chunks)

    def ingest_default_knowledge(self) -> int:
        """Loads standard medical and sports science knowledge base from config path."""
        return self.ingest_json_file(self.config.medical_knowledge_path)

    @staticmethod
    def compute_cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
        """
        Computes cosine similarity between two vectors:
        Cosine Similarity = (a . b) / (||a||_2 * ||b||_2)
        """
        norm_a = np.linalg.norm(vec_a)
        norm_b = np.linalg.norm(vec_b)
        if norm_a < 1e-9 or norm_b < 1e-9:
            return 0.0
        return float(np.dot(vec_a, vec_b) / (norm_a * norm_b))

    def search(
        self,
        query: str,
        top_k: int = 3,
        filter_anatomy: Optional[List[str]] = None,
        exclude_contraindications: Optional[List[str]] = None,
        rehab_phase: Optional[str] = None,
        category: Optional[str] = None,
        discipline: Optional[str] = None,
        tenant_id: Optional[str] = None
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """
        Executes vector cosine similarity search with clinical metadata pre-filtering:
        1. Tenant Scoping: Global chunks + Chunks owned by active tenant.
        2. Contraindication Purge: Drops chunks matching any active contraindication.
        3. Anatomical Pre-Filter: Filters by target anatomy if provided.
        4. Category & Discipline Filters: Constrains domain scope.
        5. Score Boosting: +0.20 boost for matching athlete's active rehabilitation phase.
        """
        if not self.chunks or self._vectors is None or len(self._vectors) == 0:
            return []

        query_vec = np.array(self.embedding_adapter.embed_text(query), dtype=np.float64)
        norm_q = np.linalg.norm(query_vec)
        if norm_q < 1e-9:
            return []

        # Vectorized dot products
        norms_d = np.linalg.norm(self._vectors, axis=1)
        # Avoid division by zero
        norms_d[norms_d < 1e-9] = 1e-9
        raw_similarities = np.dot(self._vectors, query_vec) / (norms_d * norm_q)

        candidate_results: List[Tuple[KnowledgeChunk, float]] = []

        # Normalize filter parameters for robust case-insensitive matching
        norm_exclude_contra = [c.lower().strip() for c in (exclude_contraindications or []) if c]
        norm_filter_anatomy = [a.lower().strip() for a in (filter_anatomy or []) if a]

        for idx, cid in enumerate(self._chunk_id_list):
            chunk = self.chunks[cid]
            base_score = float(raw_similarities[idx])

            # 1. Multi-Tenant Scoping Rule:
            # Accessible if chunk is global (tenant_id is None) OR matches requested tenant_id
            if chunk.tenant_id is not None:
                if tenant_id is None or chunk.tenant_id != tenant_id:
                    continue  # Strictly isolated: foreign tenant chunk hidden

            # 2. Hard Contraindication Filter Rule:
            # If the chunk has contraindications that intersect with athlete's active contraindications, purge it
            if norm_exclude_contra:
                chunk_contra_norm = [c.lower().strip() for c in chunk.contraindications]
                has_forbidden_contra = False
                for active_c in norm_exclude_contra:
                    for chunk_c in chunk_contra_norm:
                        if active_c in chunk_c or chunk_c in active_c:
                            has_forbidden_contra = True
                            break
                    if has_forbidden_contra:
                        break
                if has_forbidden_contra:
                    continue  # Purged due to clinical contraindication

            # 3. Anatomical Pre-Filter:
            if norm_filter_anatomy:
                chunk_anatomy_norm = [a.lower().strip() for a in chunk.target_anatomy]
                anatomy_match = False
                for fa in norm_filter_anatomy:
                    for ca in chunk_anatomy_norm:
                        if fa in ca or ca in fa:
                            anatomy_match = True
                            break
                    if anatomy_match:
                        break
                if not anatomy_match:
                    continue  # Excluded due to anatomical mismatch

            # 4. Category & Discipline Filters:
            if category and chunk.category.upper() != category.upper():
                continue
            if discipline and chunk.discipline and chunk.discipline.upper() != discipline.upper():
                continue

            # 5. Dynamic Score Boosting:
            final_score = base_score
            if rehab_phase and chunk.rehab_phase:
                if chunk.rehab_phase.upper() == rehab_phase.upper():
                    final_score += 0.20  # Clinical phase alignment bonus

            candidate_results.append((chunk, round(final_score, 4)))

        # Sort descending by final score
        candidate_results.sort(key=lambda x: x[1], reverse=True)
        return candidate_results[:top_k]

    def clear(self) -> None:
        """Wipes all stored chunks from memory."""
        self.chunks.clear()
        self._vectors = None
        self._chunk_id_list = []
