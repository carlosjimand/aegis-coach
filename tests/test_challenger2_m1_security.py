"""
Aegis Coach — Challenger 2 Empirical Stress Test Suite (Milestone 1)
===================================================================
Adversarial stress-testing of:
1. safeJsonStringify against script breakout, comments, Unicode separators, nested payloads.
2. escapeHtml against HTML attribute and tag injection vectors.
3. SECURITY_HEADERS strict compliance (CSP, XFO, XCTO, HSTS, Referrer, Permissions).
4. Direct Node.js subprocess invocation importing production cloudflare/src/index.ts.
"""

import json
import os
import re
import subprocess
import pytest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_TS_PATH = os.path.join(ROOT_DIR, 'cloudflare', 'src', 'index.ts')


def run_node_code(code: str) -> dict:
    """Run JS/TS code via node --experimental-strip-types."""
    proc = subprocess.run(
        ["node", "--experimental-strip-types", "-e", code],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    return {
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip()
    }


class TestChallenger2SafeJsonStringify:
    """Stress testing safeJsonStringify edge cases."""

    def test_script_tag_breakout_prevention(self):
        """Verify </script><script>alert(1)</script> is disarmed and round-trippable."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        const payload = '</script><script>alert(1)</script>';
        const serialized = safeJsonStringify({ payload });
        const hasScriptClose = serialized.toLowerCase().includes('</script>');
        const hasScriptOpen = serialized.toLowerCase().includes('<script>');
        const parsed = JSON.parse(serialized);
        console.log(JSON.stringify({
            serialized,
            hasScriptClose,
            hasScriptOpen,
            roundtrip: parsed.payload === payload
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0, f"Node failed: {res['stderr']}"
        data = json.loads(res["stdout"])
        assert not data["hasScriptClose"], "safeJsonStringify must NOT output raw </script>"
        assert not data["hasScriptOpen"], "safeJsonStringify must NOT output raw <script>"
        assert "\\u003c/script\\u003e" in data["serialized"]
        assert data["roundtrip"] is True, "JSON.parse must restore original payload"

    def test_html_comment_breakout_prevention(self):
        """Verify <!-- HTML comment open tags are disarmed."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        const payload = '<!-- <script>alert(1)</script> -->';
        const serialized = safeJsonStringify({ payload });
        const hasComment = serialized.includes('<!--');
        const parsed = JSON.parse(serialized);
        console.log(JSON.stringify({
            serialized,
            hasComment,
            roundtrip: parsed.payload === payload
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0, f"Node failed: {res['stderr']}"
        data = json.loads(res["stdout"])
        assert not data["hasComment"], "safeJsonStringify must NOT output raw <!--"
        assert "\\u003c!--" in data["serialized"]
        assert data["roundtrip"] is True

    def test_unicode_line_separators_u2028_u2029(self):
        """Verify U+2028 and U+2029 are replaced with escaped sequences."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        const payload = 'Line1\\u2028Line2\\u2029Line3';
        const serialized = safeJsonStringify({ payload });
        const hasRaw2028 = serialized.includes('\\u2028');
        const hasRaw2029 = serialized.includes('\\u2029');
        const hasEscaped2028 = serialized.includes('\\\\u2028');
        const hasEscaped2029 = serialized.includes('\\\\u2029');
        const parsed = JSON.parse(serialized);
        console.log(JSON.stringify({
            hasRaw2028,
            hasRaw2029,
            hasEscaped2028,
            hasEscaped2029,
            roundtrip: parsed.payload === payload
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0, f"Node failed: {res['stderr']}"
        data = json.loads(res["stdout"])
        assert not data["hasRaw2028"], "Must not contain unescaped raw U+2028"
        assert not data["hasRaw2029"], "Must not contain unescaped raw U+2029"
        assert data["hasEscaped2028"], "Must contain escaped \\\\u2028"
        assert data["hasEscaped2029"], "Must contain escaped \\\\u2029"
        assert data["roundtrip"] is True

    def test_nested_objects_and_arrays(self):
        """Verify deep nested structures containing nasty payloads serialize cleanly."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        const deep = {
            a: {
                b: [
                    { x: '</script>' },
                    { y: '<!--' },
                    { z: '\\u2028' }
                ]
            }
        };
        const serialized = safeJsonStringify(deep);
        const hasBad = serialized.includes('</script>') || serialized.includes('<!--');
        const parsed = JSON.parse(serialized);
        console.log(JSON.stringify({
            hasBad,
            roundtrip: parsed.a.b[0].x === '</script>' && parsed.a.b[2].z === '\\u2028'
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert not data["hasBad"]
        assert data["roundtrip"] is True

    def test_backticks_and_quotes_handling(self):
        """Verify quotes and backticks behave safely."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        const payload = {
            tick: '`',
            quote: '"',
            code: '`${alert(1)}`',
            sql: "'; DROP TABLE users; --"
        };
        const serialized = safeJsonStringify(payload);
        const parsed = JSON.parse(serialized);
        console.log(JSON.stringify({
            roundtrip: JSON.stringify(parsed) === JSON.stringify(payload)
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert data["roundtrip"] is True

    def test_null_and_undefined_behavior(self):
        """Verify null serializes to 'null', and document undefined behavior."""
        js_code = """
        import { safeJsonStringify } from './cloudflare/src/index.ts';
        let nullResult = safeJsonStringify(null);
        let undefThrew = false;
        try {
            safeJsonStringify(undefined);
        } catch (e) {
            undefThrew = true;
        }
        console.log(JSON.stringify({
            nullResult,
            undefThrew
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert data["nullResult"] == "null"
        # In JavaScript JSON.stringify(undefined) returns undefined, so undefined.replace throws TypeError.
        assert data["undefThrew"] is True, "safeJsonStringify(undefined) throws TypeError"


class TestChallenger2EscapeHtml:
    """Stress testing escapeHtml against injection vectors."""

    def test_html_tag_injection_vectors(self):
        """Verify tag injection vectors (<img onerror>, <script>) are neutralized."""
        js_code = """
        import { escapeHtml } from './cloudflare/src/index.ts';
        const v1 = escapeHtml('<img src=x onerror=alert(1)>');
        const v2 = escapeHtml('"><script>alert(1)</script>');
        console.log(JSON.stringify({
            v1_has_raw_tag: v1.includes('<') || v1.includes('>'),
            v1_escaped: v1,
            v2_has_raw_tag: v2.includes('<') || v2.includes('>') || v2.includes('"'),
            v2_escaped: v2
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert not data["v1_has_raw_tag"]
        assert "&lt;img src=x onerror=alert(1)&gt;" in data["v1_escaped"]
        assert not data["v2_has_raw_tag"]
        assert "&quot;&gt;&lt;script&gt;alert(1)&lt;/script&gt;" in data["v2_escaped"]

    def test_attribute_breakout_quotes(self):
        """Verify single and double quote injection cannot break HTML attribute contexts."""
        js_code = """
        import { escapeHtml } from './cloudflare/src/index.ts';
        const singleQuote = escapeHtml("' onmouseover='alert(1)'");
        const doubleQuote = escapeHtml('" onmouseover="alert(1)"');
        console.log(JSON.stringify({
            single_has_raw: singleQuote.includes("'"),
            single_escaped: singleQuote,
            double_has_raw: doubleQuote.includes('"'),
            double_escaped: doubleQuote
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert not data["single_has_raw"]
        assert "&#39;" in data["single_escaped"]
        assert not data["double_has_raw"]
        assert "&quot;" in data["double_escaped"]

    def test_ampersands_and_non_strings(self):
        """Verify ampersands are escaped and null/undefined return empty string."""
        js_code = """
        import { escapeHtml } from './cloudflare/src/index.ts';
        console.log(JSON.stringify({
            amp: escapeHtml('A & B'),
            nullVal: escapeHtml(null),
            undefVal: escapeHtml(undefined),
            zero: escapeHtml(0),
            boolFalse: escapeHtml(false)
        }));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        data = json.loads(res["stdout"])
        assert data["amp"] == "A &amp; B"
        assert data["nullVal"] == ""
        assert data["undefVal"] == ""
        assert data["zero"] == "0"
        assert data["boolFalse"] == "false"


class TestChallenger2SecurityHeaders:
    """Stress testing SECURITY_HEADERS specification compliance."""

    def test_security_headers_structure(self):
        """Verify all mandatory security headers exist and meet strict criteria."""
        js_code = """
        import { SECURITY_HEADERS } from './cloudflare/src/index.ts';
        console.log(JSON.stringify(SECURITY_HEADERS));
        """
        res = run_node_code(js_code)
        assert res["returncode"] == 0
        headers = json.loads(res["stdout"])

        # CSP Verification
        csp = headers.get("Content-Security-Policy", "")
        assert csp, "Content-Security-Policy must be defined"
        assert "default-src 'self'" in csp
        assert "frame-ancestors 'none'" in csp
        # Strict CSP: no wildcards in script-src or style-src
        script_src = re.search(r"script-src\s+([^;]+)", csp)
        style_src = re.search(r"style-src\s+([^;]+)", csp)
        assert script_src, "CSP must contain script-src directive"
        assert "*" not in script_src.group(1), f"script-src must NOT contain wildcard '*': {script_src.group(1)}"
        assert style_src, "CSP must contain style-src directive"
        assert "*" not in style_src.group(1), f"style-src must NOT contain wildcard '*': {style_src.group(1)}"

        # X-Frame-Options
        assert headers.get("X-Frame-Options") == "DENY", "X-Frame-Options must be DENY"

        # X-Content-Type-Options
        assert headers.get("X-Content-Type-Options") == "nosniff", "X-Content-Type-Options must be nosniff"

        # HSTS
        hsts = headers.get("Strict-Transport-Security", "")
        assert hsts, "Strict-Transport-Security must be defined"
        max_age_match = re.search(r"max-age=(\d+)", hsts)
        assert max_age_match, "HSTS must have max-age directive"
        max_age = int(max_age_match.group(1))
        assert max_age >= 31536000, f"HSTS max-age must be at least 1 year (31536000), got {max_age}"
        assert "includeSubDomains" in hsts, "HSTS must include includeSubDomains"
        assert "preload" in hsts, "HSTS must include preload"

        # Referrer-Policy
        assert headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

        # Permissions-Policy
        perms = headers.get("Permissions-Policy", "")
        assert "camera=()" in perms
        assert "microphone=()" in perms
        assert "geolocation=()" in perms

    def test_worker_html_and_api_responses_attach_security_headers(self):
        """Verify index.ts attaches SECURITY_HEADERS across all endpoints."""
        with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
            ts_code = f.read()

        # HTML response includes SECURITY_HEADERS
        assert "...SECURITY_HEADERS" in ts_code, "HTML and API responses must spread SECURITY_HEADERS"
        assert "headers: { \"Content-Type\": \"application/json\", ...SECURITY_HEADERS }" in ts_code
