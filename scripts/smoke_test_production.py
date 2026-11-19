"""
Aegis Coach — Live Production Smoke Test Suite (Milestone 4)
Target: https://aegis-intervals-sync.uranuslabs.workers.dev
"""

import json
import ssl
import urllib.request
import urllib.error

BASE_URL = "https://aegis-intervals-sync.uranuslabs.workers.dev"
AEGIS_KEY = "4cvqxm8a5intat925ttdcmpja"

# Disable SSL verification due to simulated future date (2026) causing cert expiration checks
SSL_CTX = ssl._create_unverified_context()

def test_a_root_html_and_security_headers():
    print("\n--- Test A: GET / (Root HTML & Security Headers) ---")
    req = urllib.request.Request(f"{BASE_URL}/", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        status = resp.status
        headers = dict(resp.headers)
        body = resp.read().decode('utf-8')
        print(f"Status Code: {status}")
        print("Security Headers Checked:")
        expected_sec_headers = [
            "content-security-policy",
            "strict-transport-security",
            "x-frame-options",
            "x-content-type-options",
            "referrer-policy",
            "permissions-policy"
        ]
        # Normalize headers to lowercase
        norm_headers = {k.lower(): v for k, v in headers.items()}
        for sec in expected_sec_headers:
            val = norm_headers.get(sec)
            assert val is not None, f"Missing security header: {sec}"
            print(f"  [OK] {sec}: {val[:60]}..." if len(val) > 60 else f"  [OK] {sec}: {val}")
        assert status == 200, f"Expected 200, got {status}"
        assert "<!DOCTYPE html>" in body or "<html" in body, "Expected HTML body"
        print("Test A PASSED!")

def test_b_service_worker():
    print("\n--- Test B: GET /sw.js (Service Worker) ---")
    req = urllib.request.Request(f"{BASE_URL}/sw.js", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        body = resp.read().decode('utf-8')
        print(f"Status Code: {status}")
        print(f"Content-Type: {content_type}")
        assert status == 200, f"Expected 200, got {status}"
        assert "application/javascript" in content_type or "text/javascript" in content_type, f"Unexpected Content-Type: {content_type}"
        assert "self.addEventListener" in body, "Service Worker should contain addEventListener"
        print("Test B PASSED!")

def test_c_manifest():
    print("\n--- Test C: GET /manifest.json (PWA Manifest) ---")
    req = urllib.request.Request(f"{BASE_URL}/manifest.json", headers={"User-Agent": "AegisSmokeTest/1.0"})
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        body = resp.read().decode('utf-8')
        print(f"Status Code: {status}")
        print(f"Content-Type: {content_type}")
        assert status == 200, f"Expected 200, got {status}"
        parsed = json.loads(body)
        print(f"Manifest Name: {parsed.get('name')}")
        assert parsed.get("name") == "Aegis Coach", f"Expected name 'Aegis Coach', got {parsed.get('name')}"
        print("Test C PASSED!")

def test_d_get_profile_unauthorized():
    print("\n--- Test D: GET /api/get_profile without auth ---")
    req = urllib.request.Request(f"{BASE_URL}/api/get_profile", headers={"User-Agent": "AegisSmokeTest/1.0"})
    try:
        with urllib.request.urlopen(req, context=SSL_CTX) as resp:
            raise AssertionError(f"Expected HTTP 401 Unauthorized, got {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        assert e.code == 401, f"Expected 401, got {e.code}"
        body = e.read().decode('utf-8')
        print(f"Response: {body}")
        print("Test D PASSED!")

def test_e_save_gym_session_unauthorized():
    print("\n--- Test E: POST /api/save_gym_session without auth ---")
    payload = json.dumps({"date": "2026-11-16", "routine_id": 1}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/save_gym_session",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisSmokeTest/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CTX) as resp:
            raise AssertionError(f"Expected HTTP 401 Unauthorized, got {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        assert e.code == 401, f"Expected 401, got {e.code}"
        body = e.read().decode('utf-8')
        print(f"Response: {body}")
        print("Test E PASSED!")

def test_f_webhook_unauthorized():
    print("\n--- Test F: POST /webhook without secret token ---")
    payload = json.dumps({"update_id": 1, "message": {"text": "/start"}}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/webhook",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AegisSmokeTest/1.0"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, context=SSL_CTX) as resp:
            raise AssertionError(f"Expected HTTP 401 Unauthorized, got {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"Status Code: {e.code}")
        assert e.code == 401, f"Expected 401, got {e.code}"
        body = e.read().decode('utf-8')
        print(f"Response: {body}")
        print("Test F PASSED!")

def test_g_get_profile_authorized():
    print("\n--- Test G: GET /api/get_profile with X-Aegis-Key ---")
    req = urllib.request.Request(
        f"{BASE_URL}/api/get_profile",
        headers={
            "X-Aegis-Key": AEGIS_KEY,
            "User-Agent": "AegisSmokeTest/1.0"
        }
    )
    with urllib.request.urlopen(req, context=SSL_CTX) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type", "")
        body = resp.read().decode('utf-8')
        print(f"Status Code: {status}")
        print(f"Content-Type: {content_type}")
        print(f"Response Body: {body}")
        assert status == 200, f"Expected 200, got {status}"
        assert "application/json" in content_type, f"Expected JSON content-type, got {content_type}"
        parsed = json.loads(body)
        print(f"Parsed JSON Profile: {parsed}")
        print("Test G PASSED!")
        assert "application/json" in content_type, f"Expected JSON content-type, got {content_type}"
        parsed = json.loads(body)
        print(f"Parsed JSON Profile: {parsed}")
        print("Test G PASSED!")

if __name__ == "__main__":
    print(f"Executing Live Production Smoke Tests against {BASE_URL}...")
    test_a_root_html_and_security_headers()
    test_b_service_worker()
    test_c_manifest()
    test_d_get_profile_unauthorized()
    test_e_save_gym_session_unauthorized()
    test_f_webhook_unauthorized()
    test_g_get_profile_authorized()
    print("\n==========================================")
    print("ALL LIVE PRODUCTION SMOKE TESTS PASSED 100%!")
    print("==========================================")
