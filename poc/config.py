"""
Aegis Coach — Configuration Module
===================================
Defines global application settings, environment mode toggles (MOCK vs LIVE),
embedding dimensions, and filesystem paths for the Proof of Concept core engine.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field


# Base paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
POC_ROOT = Path(__file__).resolve().parent
DATA_DIR = POC_ROOT / "data"


class AegisConfig(BaseModel):
    """Global configuration settings for Aegis Coach PoC engine."""

    # Execution Mode
    mock_mode: bool = Field(
        default_factory=lambda: os.getenv("AEGIS_MOCK_MODE", "true").lower() in ("true", "1", "yes"),
        description="When True, runs in 100% offline deterministic mode with zero external cloud dependencies."
    )
    live_mode: bool = Field(
        default_factory=lambda: os.getenv("AEGIS_LIVE_MODE", "false").lower() in ("true", "1", "yes"),
        description="When True and API keys are present, enables live OpenAI/Anthropic providers."
    )

    # API Keys (Optional)
    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key for live LLM and embedding requests."
    )
    anthropic_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"),
        description="Anthropic API key for live Claude requests."
    )

    # File Paths
    data_dir: Path = Field(default=DATA_DIR)
    medical_knowledge_path: Path = Field(default_factory=lambda: DATA_DIR / "medical_knowledge.json")
    sample_workouts_path: Path = Field(default_factory=lambda: DATA_DIR / "sample_workouts.json")
    user_profiles_path: Path = Field(default_factory=lambda: DATA_DIR / "user_profiles.json")

    # Embedding & Vector Store Settings
    embedding_dim: int = Field(default=128, description="Dimensionality of vector embeddings.")
    deterministic_seed: int = Field(default=42, description="Random seed for deterministic hashing vectors.")
    vector_similarity_threshold: float = Field(default=0.60, description="Minimum cosine similarity for RAG retrieval.")
    default_top_k: int = Field(default=3, description="Default number of chunks retrieved by RAG.")

    # Multi-Agent & LLM Settings
    default_llm_model: str = Field(default="gpt-4o-mini", description="Target default model for agent reasoning.")
    clinical_llm_model: str = Field(default="gpt-4o", description="Target model for complex medical/rehab reasoning.")
    max_context_tokens: int = Field(default=4096, description="Maximum context window budget.")
    temperature: float = Field(default=0.2, description="Sampling temperature for deterministic outputs.")

    # Multi-Tenancy Settings
    default_tenant_id: str = Field(default="tenant_carlos_800m", description="Default tenant ID for single-tenant or CLI tests.")
    strict_tenant_isolation: bool = Field(default=True, description="Enforce strict exception raising on cross-tenant access.")
    tenant_token_secret: str = Field(
        default_factory=lambda: os.getenv("AEGIS_SECRET_KEY", "aegis-coach-insecure-dev-secret-key-2026"),
        description="HMAC secret key for tenant token signing."
    )

    # Banister Physiology Parameters
    banister_ctl_time_constant: int = Field(default=42, description="Time constant (days) for Chronic Training Load (Fitness).")
    banister_atl_time_constant: int = Field(default=7, description="Time constant (days) for Acute Training Load (Fatigue).")
    acwr_danger_threshold: float = Field(default=1.50, description="ACWR spike threshold flagging acute injury risk.")
    acwr_sweet_spot_min: float = Field(default=0.80, description="Lower bound of optimal ACWR training zone.")
    acwr_sweet_spot_max: float = Field(default=1.30, description="Upper bound of optimal ACWR training zone.")


# Global singleton instance
_config_instance: Optional[AegisConfig] = None


def get_config() -> AegisConfig:
    """Retrieve the global Aegis Coach configuration instance."""
    global _config_instance
    if _config_instance is None:
        _config_instance = AegisConfig()
    return _config_instance


def reset_config(new_config: Optional[AegisConfig] = None) -> AegisConfig:
    """Reset or override the global configuration (useful for testing)."""
    global _config_instance
    _config_instance = new_config if new_config is not None else AegisConfig()
    return _config_instance
