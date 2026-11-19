"""
Aegis Coach — Live Production Smoke Test Suite in Pytest (Milestone 4)
Target: https://aegis-intervals-sync.uranuslabs.workers.dev
"""

import json
import ssl
import urllib.request
import urllib.error
import pytest

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"
AEGIS_KEY = "4cvqxm8a5intat925ttdcmpja"
SSL_CTX = ssl._create_unverified_context()

def test_live_production_root_and_security_headers():
    req = urllib.request.Request(f"{BASE_URL}/", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        assert resp.status == 200
        headers = {k.lower(): v for k, v in dict(resp.headers).items()}
        for header in [
            "content-security-policy",
            "strict-transport-security",
            "x-frame-options",
            "x-content-type-options",
            "referrer-policy",
            "permissions-policy"
        ]:
            assert header in headers, f"Missing header: {header}"

def test_live_production_service_worker():
    req = urllib.request.Request(f"{BASE_URL}/sw.js", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        assert resp.status == 200
        ct = resp.headers.get("Content-Type", "")
        assert "application/javascript" in ct or "text/javascript" in ct

def test_live_production_manifest():
    req = urllib.request.Request(f"{BASE_URL}/manifest.json", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert data.get("name") == "Aegis Coach"

def test_live_production_get_profile_unauthorized():
    req = urllib.request.Request(f"{BASE_URL}/api/get_profile", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(req, context=SSL_CTX)
    assert exc_info.value.code == 401

def test_live_production_save_gym_session_unauthorized():
    payload = json.dumps({"date": "2026-11-16", "routine_id": 1}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/save_gym_session",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisSmokeTest/1.0"},
        method="POST"
    )
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(req, context=SSL_CTX)
    assert exc_info.value.code == 401

def test_live_production_webhook_unauthorized():
    payload = json.dumps({"update_id": 1, "message": {"text": "/start"}}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/webhook",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisSmokeTest/1.0"},
        method="POST"
    )
    with pytest.raises(urllib.error.HTTPError) as exc_info:
        urllib.request.urlopen(req, context=SSL_CTX)
    assert exc_info.value.code == 401

def test_live_production_get_profile_authorized():
    req = urllib.request.Request(
        f"{BASE_URL}/api/get_profile",
        headers={
            "X-Aegis-Key": AEGIS_KEY,
            "User-Agent": "AegisSmokeTest/1.0"
        }
    )
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert isinstance(data, dict)
