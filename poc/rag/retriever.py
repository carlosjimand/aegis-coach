"""
Aegis Coach — Hybrid Search Retriever
======================================
Combines dense vector similarity with sparse keyword / anatomical scoring,
reranking, and clinical citation formatting for agent context injection.
"""

from __future__ import annotations

import re
from typing import List, Dict, Any, Optional, Tuple
from poc.rag.vector_store import VectorStore, KnowledgeChunk
from poc.models.athlete import AthleteProfile


class HybridRetriever:
    """
    Hybrid Search Retriever integrating dense semantic similarity with sparse keyword matching,
    clinical contraindication filtering, and structured markdown citation rendering.
    """

    def __init__(self, vector_store: Optional[VectorStore] = None, alpha: float = 0.70):
        """
        Args:
            vector_store: VectorStore instance (initializes default if None).
            alpha: Weight for dense vector similarity (0.0 to 1.0). (1 - alpha) is lexical weight.
        """
        self.vector_store = vector_store or VectorStore()
        self.alpha = alpha

        # Ensure knowledge base is populated
        if not self.vector_store.chunks:
            self.vector_store.ingest_default_knowledge()

    @staticmethod
    def _compute_lexical_score(query: str, chunk: KnowledgeChunk) -> float:
        """
        Computes BM25-style lexical keyword overlap between query and chunk (title + content + anatomy).
        """
        query_words = set(re.findall(r"\w+", query.lower()))
        if not query_words:
            return 0.0

        corpus_text = f"{chunk.title} {chunk.content} {' '.join(chunk.target_anatomy)} {' '.join(chunk.contraindications)}".lower()
        matched = sum(1 for w in query_words if len(w) > 2 and w in corpus_text)
        return min(1.0, matched / max(1.0, float(len(query_words))))

    def retrieve(
        self,
        query: str,
        athlete: Optional[AthleteProfile] = None,
        top_k: int = 3,
        category: Optional[str] = None,
        discipline: Optional[str] = None,
        tenant_id: Optional[str] = None
    ) -> List[Tuple[KnowledgeChunk, float]]:
        """
        Executes hybrid retrieval:
        1. Derives active contraindications and target anatomy from athlete profile if provided.
        2. Queries VectorStore for dense semantic candidates.
        3. Blends dense score and sparse lexical score: Score = alpha * Dense + (1 - alpha) * Lexical.
        4. Returns top_k highest scoring chunks with final composite scores.
        """
        filter_anatomy: Optional[List[str]] = None
        exclude_contra: Optional[List[str]] = None
        rehab_phase: Optional[str] = None

        if athlete:
            exclude_contra = athlete.active_contraindications
            active_injuries = athlete.active_injuries
            if active_injuries:
                filter_anatomy = [inj.anatomical_region for inj in active_injuries]
                rehab_phase = active_injuries[0].rehab_phase.value

        # Fetch dense candidates with pre-filtering
        dense_results = self.vector_store.search(
            query=query,
            top_k=max(top_k * 2, 5),
            filter_anatomy=filter_anatomy,
            exclude_contraindications=exclude_contra,
            rehab_phase=rehab_phase,
            category=category,
            discipline=discipline,
            tenant_id=tenant_id
        )

        # Re-score using hybrid combination
        hybrid_results: List[Tuple[KnowledgeChunk, float]] = []
        for chunk, dense_score in dense_results:
            lexical_score = self._compute_lexical_score(query, chunk)
            composite_score = (self.alpha * dense_score) + ((1.0 - self.alpha) * lexical_score)
            hybrid_results.append((chunk, round(composite_score, 4)))

        # Sort descending by composite score
        hybrid_results.sort(key=lambda x: x[1], reverse=True)
        return hybrid_results[:top_k]

    @staticmethod
    def format_clinical_context(chunks_with_scores: List[Tuple[KnowledgeChunk, float]]) -> str:
        """
        Formats retrieved scientific chunks into clean, structured Markdown for agent system prompt injection.
        """
        if not chunks_with_scores:
            return "No scientific literature found matching the search criteria."

        sections = ["### 📚 Sports Science & Clinical Evidence Context:"]
        for idx, (chunk, score) in enumerate(chunks_with_scores, 1):
            citations_str = "; ".join(
                f"{c.get('authors', 'Unknown')} ({c.get('year', 'N/A')}), *{c.get('title', '')}*, {c.get('journal', '')}"
                for c in chunk.citations
            ) if chunk.citations else "Clinical Guideline Consensus"

            section = (
                f"**[{idx}] {chunk.title}** (Relevance Score: {score:.2f} | Evidence: {chunk.evidence_level})\n"
                f"- **Target Anatomy**: {', '.join(chunk.target_anatomy) if chunk.target_anatomy else 'General'}\n"
                f"- **Rehab Phase**: {chunk.rehab_phase or 'All Phases'}\n"
                f"- **Clinical Protocol**: {chunk.content}\n"
                f"- **Contraindications**: {', '.join(chunk.contraindications) if chunk.contraindications else 'None specified'}\n"
                f"- **Scientific Citation**: {citations_str}\n"
            )
            sections.append(section)

        return "\n".join(sections)
