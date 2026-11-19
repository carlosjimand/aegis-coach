"""
Aegis Coach — Tenancy Package
==============================
Exposes tenant context managers, isolation exceptions, and security policy validators.
"""

from poc.tenancy.context import (
    TenantContext,
    TenantIsolationError,
    TenantSecurityError,
    TenantNotFoundError,
    get_current_tenant,
    set_current_tenant,
    clear_current_tenant,
)
from poc.tenancy.security import (
    TenantSecurityManager,
)

__all__ = [
    "TenantContext",
    "TenantIsolationError",
    "TenantSecurityError",
    "TenantNotFoundError",
    "get_current_tenant",
    "set_current_tenant",
    "clear_current_tenant",
    "TenantSecurityManager",
]
