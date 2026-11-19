"""
Aegis Coach — Multi-Tenant Security & Isolation Policy Engine
=============================================================
Provides HMAC-based tenant token generation, signature verification, and
strict boundary validation preventing cross-tenant data leakage or spoofing.
"""

from __future__ import annotations

import hmac
import hashlib
import time
import base64
import json
from typing import Dict, Any, Optional

from poc.config import get_config
from poc.tenancy.context import (
    TenantIsolationError,
    TenantSecurityError,
    get_current_tenant
)
from poc.models.athlete import AthleteProfile


class TenantSecurityManager:
    """
    Manages tenant authentication tokens and enforces cross-tenant isolation boundaries.
    """

    def __init__(self, secret_key: Optional[str] = None):
        self.config = get_config()
        self.secret_key = (secret_key or self.config.tenant_token_secret).encode("utf-8")

    def generate_tenant_token(self, tenant_id: str, ttl_seconds: int = 86400) -> str:
        """
        Generates a secure HMAC-SHA256 signed token for a tenant.
        Token format: base64(payload_json).signature_hex
        """
        if not tenant_id:
            raise TenantSecurityError("Cannot generate token for empty tenant_id.")

        payload = {
            "tenant_id": tenant_id,
            "iat": int(time.time()),
            "exp": int(time.time()) + ttl_seconds
        }
        payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode("utf-8")

        signature = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).hexdigest()
        return f"{payload_b64}.{signature}"

    def verify_tenant_token(self, token: str) -> str:
        """
        Validates HMAC signature and expiration of a tenant token.
        Returns the verified tenant_id or raises TenantSecurityError.
        """
        if not token or "." not in token:
            raise TenantSecurityError("Malformed or missing tenant token.")

        parts = token.split(".")
        if len(parts) != 2:
            raise TenantSecurityError("Invalid token structure.")

        payload_b64, signature = parts

        try:
            payload_bytes = base64.urlsafe_b64decode(payload_b64.encode("utf-8"))
            expected_sig = hmac.new(self.secret_key, payload_bytes, hashlib.sha256).hexdigest()

            if not hmac.compare_digest(signature, expected_sig):
                raise TenantSecurityError("Invalid token signature: potential cross-tenant tampering detected.")

            payload = json.loads(payload_bytes.decode("utf-8"))
            if time.time() > payload.get("exp", 0):
                raise TenantSecurityError("Tenant token has expired.")

            return payload["tenant_id"]
        except (ValueError, KeyError) as e:
            raise TenantSecurityError(f"Failed to parse tenant token: {str(e)}")

    def assert_tenant_access(
        self,
        target_tenant_id: str,
        active_tenant_id: Optional[str] = None
    ) -> None:
        """
        Asserts that the active tenant context matches the target resource's tenant ID.
        Raises TenantIsolationError if there is a mismatch.
        """
        current = active_tenant_id or get_current_tenant()
        if not current:
            # If no active context is set, check strict setting
            if self.config.strict_tenant_isolation:
                raise TenantIsolationError(
                    f"Access Denied: Unscoped operation attempted on tenant '{target_tenant_id}'."
                )
            return

        if current != target_tenant_id:
            raise TenantIsolationError(
                f"Security Violation: Tenant '{current}' is unauthorized to access resources belonging to tenant '{target_tenant_id}'."
            )

    def validate_athlete_profile_access(
        self,
        athlete: AthleteProfile,
        expected_tenant_id: Optional[str] = None
    ) -> None:
        """
        Verifies that an athlete profile belongs to the expected tenant.
        """
        target_tenant = athlete.tenant_id
        self.assert_tenant_access(target_tenant, active_tenant_id=expected_tenant_id)
