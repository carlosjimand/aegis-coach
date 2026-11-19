"""
Aegis Coach — Dual-Mode Embedding Adapter
=========================================
Provides vector embeddings for sports science and clinical rehabilitation RAG.
Supports:
1. `DeterministicEmbeddingAdapter`: 100% offline, deterministic semantic-aware feature vectorizer.
2. `OpenAIEmbeddingAdapter`: Live provider for OpenAI embeddings API with graceful fallback.
"""

from __future__ import annotations

import re
import math
import hashlib
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import numpy as np

from poc.config import get_config


class BaseEmbeddingAdapter(ABC):
    """Abstract interface for text embedding generation."""

    @abstractmethod
    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string into a float vector."""
        pass

    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of text strings into float vectors."""
        pass


class DeterministicEmbeddingAdapter(BaseEmbeddingAdapter):
    """
    High-fidelity offline deterministic embedding engine.
    Combines domain-specific semantic feature projections, character/word n-gram TF-IDF weighting,
    and murmur/md5 hashing to produce stable, normalized cosine embeddings without cloud dependencies.
    """

    # Domain-specific semantic clusters for sports science & medicine
    SEMANTIC_CLUSTERS: Dict[str, List[str]] = {
        "hamstring_rehab": [
            "hamstring", "isquiotibial", "isquio", "biceps femoris", "semitendinosus", "semimembranosus",
            "askling", "extender", "diver", "glider", "hsr", "heavy slow resistance", "nordic",
            "knee flexion", "myotendinous", "desgarro", "rotura", "ischial", "sprint"
        ],
        "achilles_rehab": [
            "achilles", "aquiles", "tendon", "tendinopathy", "tendinitis", "alfredson", "silbernagel",
            "heel drop", "gastrocnemius", "soleus", "soleo", "gemelo", "calf raise", "plantar"
        ],
        "patellar_rehab": [
            "patellar", "rotuliano", "rodilla", "knee", "spanish squat", "sentadilla espanola",
            "jumper", "quadriceps", "cuadriceps", "rectus femoris", "vastus", "isometric"
        ],
        "lumbar_spine": [
            "lumbar", "spine", "columna", "disc", "hernia", "protrusion", "mcgill", "bird-dog",
            "side plank", "curl-up", "neutral spine", "trap bar", "hip thrust", "deadlift", "peso muerto"
        ],
        "marathon_nutrition": [
            "carbohydrate", "carbohidrato", "hidratos", "glycogen", "glucogeno", "loading", "carga",
            "fodmap", "maltodextrin", "gel", "fructose", "fructosa", "glucose", "marathon", "maraton", "gastrointestinal"
        ],
        "altitude_physiology": [
            "altitude", "altitud", "hypoxia", "hipoxia", "mountain", "montana", "hydration",
            "hidratacion", "acclimatization", "aclimatacion", "ferritin", "po2", "ams"
        ],
        "track_potentiation_pap": [
            "pap", "post-activation", "potentiation", "potenciacion", "800m", "track", "pista",
            "medio fondo", "squat", "hex bar", "jump", "neuromuscular", "rate of force development"
        ],
        "autonomic_fatigue_acwr": [
            "hrv", "vfc", "rmssd", "autonomic", "crash", "fatigue", "fatiga", "acwr", "ctl", "atl",
            "tsb", "trimp", "overtraining", "sobreentrenamiento", "recovery", "recuperacion", "sleep"
        ],
        "cardio_trauma_redflags": [
            "chest pain", "pecho", "dolor agudo", "syncope", "desmayo", "opresion", "dyspnea",
            "falta de aire", "hematoma", "chasquido", "emergency", "urgencia", "medico", "red flag"
        ]
    }

    def __init__(self, dimension: int = 128, seed: int = 42):
        self.dimension = dimension
        self.seed = seed
        self.cluster_keys = list(self.SEMANTIC_CLUSTERS.keys())
        self.cluster_dim_size = 8  # Dedicated dimensions per semantic cluster

    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into lowercase alphanumeric words."""
        cleaned = re.sub(r"[^\w\s-]", " ", text.lower())
        tokens = [t.strip() for t in cleaned.split() if len(t.strip()) > 1]
        return tokens

    def _hash_token(self, token: str, dim_range: int) -> int:
        """Deterministically hashes a token to an index within dim_range."""
        h = int(hashlib.md5(f"{self.seed}:{token}".encode("utf-8")).hexdigest(), 16)
        return h % dim_range

    def embed_text(self, text: str) -> List[float]:
        """
        Creates a deterministic 128-dimensional normalized embedding vector.
        Features are divided into:
        - Structured Semantic Cluster Projections (Dimensions 0 to 71)
        - Substring / N-gram & Bag-of-Words Hashing (Dimensions 72 to 127)
        """
        vec = np.zeros(self.dimension, dtype=np.float64)
        tokens = self._tokenize(text)
        normalized_text = text.lower()

        if not tokens:
            # Return neutral unit vector
            vec[0] = 1.0
            return vec.tolist()

        # 1. Semantic Cluster Scoring
        for idx, (cluster_name, keywords) in enumerate(self.SEMANTIC_CLUSTERS.items()):
            cluster_score = 0.0
            for kw in keywords:
                if kw in normalized_text:
                    # Multi-word phrase or exact word bonus
                    weight = 2.5 if " " in kw else 1.2
                    cluster_score += weight

            if cluster_score > 0:
                base_dim = (idx * self.cluster_dim_size) % (self.dimension // 2)
                for offset in range(self.cluster_dim_size):
                    dim_idx = base_dim + offset
                    if dim_idx < self.dimension:
                        # Spread cluster signal with alternating harmonic weights
                        sign = 1.0 if offset % 2 == 0 else 0.5
                        vec[dim_idx] += cluster_score * sign

        # 2. General Lexical Hashing (Word unigrams & bigrams)
        for i, token in enumerate(tokens):
            # Term frequency / position weighting
            weight = 1.0 / math.sqrt(i + 1.0)
            hash_idx = self._hash_token(token, self.dimension)
            vec[hash_idx] += weight * 1.5

            # Bigrams
            if i < len(tokens) - 1:
                bigram = f"{token}_{tokens[i+1]}"
                bigram_hash = self._hash_token(bigram, self.dimension)
                vec[bigram_hash] += weight * 2.0

            # Character 3-grams for morphological stem capture
            if len(token) >= 3:
                for c_idx in range(len(token) - 2):
                    trigram = token[c_idx:c_idx+3]
                    tri_hash = self._hash_token(trigram, self.dimension)
                    vec[tri_hash] += 0.3

        # 3. L2 Unit Normalization (||v||_2 = 1.0)
        norm = np.linalg.norm(vec)
        if norm > 1e-9:
            vec = vec / norm
        else:
            vec[0] = 1.0

        return vec.tolist()

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a collection of text strings."""
        return [self.embed_text(t) for t in texts]


class OpenAIEmbeddingAdapter(BaseEmbeddingAdapter):
    """
    Live OpenAI embedding provider with seamless fallback to DeterministicEmbeddingAdapter.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "text-embedding-3-small",
        dimension: int = 128
    ):
        self.config = get_config()
        self.api_key = api_key or self.config.openai_api_key
        self.model = model
        self.dimension = dimension
        self.fallback_adapter = DeterministicEmbeddingAdapter(dimension=dimension)

    def embed_text(self, text: str) -> List[float]:
        """Embeds text using OpenAI API if configured, otherwise falls back to deterministic engine."""
        if not self.config.live_mode or not self.api_key:
            return self.fallback_adapter.embed_text(text)

        try:
            # Attempt live OpenAI call
            import urllib.request
            import json

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "input": text,
                "model": self.model
            }
            req = urllib.request.Request(
                "https://api.openai.com/v1/embeddings",
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=5.0) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["data"][0]["embedding"]
        except Exception:
            # Safe deterministic fallback
            return self.fallback_adapter.embed_text(text)

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embeds batch of texts."""
        return [self.embed_text(t) for t in texts]


def get_embedding_adapter() -> BaseEmbeddingAdapter:
    """Factory helper returning appropriate adapter based on active configuration."""
    config = get_config()
    if config.live_mode and config.openai_api_key:
        return OpenAIEmbeddingAdapter(
            api_key=config.openai_api_key,
            dimension=config.embedding_dim
        )
    return DeterministicEmbeddingAdapter(
        dimension=config.embedding_dim,
        seed=config.deterministic_seed
    )
