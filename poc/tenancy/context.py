"""
Aegis Coach — Multi-Tenant Context Manager
==========================================
Thread-safe and async-safe context manager enforcing strict tenant boundaries
across all database queries, vector retrieval, and agent executions.
"""

from __future__ import annotations

import contextvars
from typing import Optional, Any


# ContextVar holding the active tenant ID for the current execution context
_current_tenant_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    "current_tenant", default=None
)


class TenantIsolationError(PermissionError):
    """Raised when an operation attempts to access or mutate foreign tenant data."""
    pass


class TenantSecurityError(ValueError):
    """Raised when tenant authentication or token validation fails."""
    pass


class TenantNotFoundError(LookupError):
    """Raised when a specified tenant ID does not exist."""
    pass


class TenantContext:
    """
    Context manager for scoping execution to a specific tenant ID.

    Usage:
        with TenantContext("tenant_carlos_800m"):
            # All operations inside this block are bound to tenant_carlos_800m
            profile = load_profile()
    """

    def __init__(self, tenant_id: str):
        if not tenant_id or not isinstance(tenant_id, str):
            raise TenantSecurityError("tenant_id must be a non-empty string.")
        self.tenant_id = tenant_id.strip()
        self._token: Optional[contextvars.Token] = None

    def __enter__(self) -> TenantContext:
        self._token = _current_tenant_var.set(self.tenant_id)
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._token is not None:
            _current_tenant_var.reset(self._token)

    async def __aenter__(self) -> TenantContext:
        return self.__enter__()

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.__exit__(exc_type, exc_val, exc_tb)


def get_current_tenant(strict: bool = False) -> Optional[str]:
    """
    Returns the currently active tenant ID from ContextVar.
    If strict=True and no tenant is active, raises TenantIsolationError.
    """
    tenant_id = _current_tenant_var.get()
    if strict and (tenant_id is None or not tenant_id.strip()):
        raise TenantIsolationError("No active TenantContext is set in the current execution context.")
    return tenant_id


def set_current_tenant(tenant_id: str) -> None:
    """Sets the active tenant ID globally for the current context."""
    if not tenant_id or not isinstance(tenant_id, str):
        raise TenantSecurityError("tenant_id must be a non-empty string.")
    _current_tenant_var.set(tenant_id.strip())


def clear_current_tenant() -> None:
    """Clears the active tenant ID from the current context."""
    _current_tenant_var.set(None)
