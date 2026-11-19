"""
Aegis Coach — RAG Package
=========================
Exposes vector stores, embedding adapters, knowledge chunks, and hybrid retrieval engines.
"""

from poc.rag.embeddings import (
    BaseEmbeddingAdapter,
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

__all__ = [
    "BaseEmbeddingAdapter",
    "DeterministicEmbeddingAdapter",
    "OpenAIEmbeddingAdapter",
    "get_embedding_adapter",
    "KnowledgeChunk",
    "VectorStore",
    "HybridRetriever",
]
