import pytest
import os
import sys
import subprocess
from datetime import datetime
from unittest.mock import patch, MagicMock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import scripts.sync_coaching_engine as sync_engine


class TestSyncCoachingEngineHardening:
    """Empirical challenge tests for scripts/sync_coaching_engine.py."""

    def test_default_newest_date_is_today_or_later(self):
        """Verify that default newest_date evaluates to current date dynamically."""
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        with patch.object(sync_engine.session, 'get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = [{"id": "act_1"}]
            mock_get.return_value = mock_resp
            
            # Call with default (no arguments)
            activities = sync_engine.fetch_activities()
            assert len(activities) == 1
            
            # Assert url contains today's date
            called_url = mock_get.call_args[0][0]
            assert f"newest={today_str}" in called_url, f"Expected newest={today_str} in URL {called_url}"
            assert f"oldest=2026-08-15" in called_url

    def test_explicit_newest_date_override(self):
        """Verify that explicit newest_date is respected."""
        with patch.object(sync_engine.session, 'get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = []
            mock_get.return_value = mock_resp
            
            sync_engine.fetch_activities(oldest_date='2026-11-01', newest_date='2026-11-28')
            called_url = mock_get.call_args[0][0]
            assert "oldest=2026-11-01" in called_url
            assert "newest=2026-11-28" in called_url

    def test_wellness_default_newest_date_is_today(self):
        """Verify that wellness fetch defaults newest_date to today dynamically."""
        today_str = datetime.now().strftime('%Y-%m-%d')
        with patch.object(sync_engine.session, 'get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = []
            mock_get.return_value = mock_resp
            
            sync_engine.fetch_wellness()
            called_url = mock_get.call_args[0][0]
            assert f"newest={today_str}" in called_url

    def test_session_adapter_and_retry_configuration(self):
        """Verify that session is mounted with HTTPAdapter with proper retry backoff."""
        assert 'https://' in sync_engine.session.adapters
        assert 'http://' in sync_engine.session.adapters
        
        adapter = sync_engine.session.adapters['https://']
        assert adapter is not None
        assert hasattr(adapter, 'max_retries')
        
        retry = adapter.max_retries
        assert retry.total == 3, f"Expected retry total 3, got {retry.total}"
        assert retry.backoff_factor == 1, f"Expected backoff_factor 1, got {retry.backoff_factor}"
        assert set(retry.status_forcelist) == {429, 500, 502, 503, 504}
        assert retry.raise_on_status is False

    def test_all_api_calls_enforce_timeout(self):
        """Empirically verify that every single fetch function passes DEFAULT_TIMEOUT to session.get."""
        expected_timeout = (5.0, 25.0)
        assert sync_engine.DEFAULT_TIMEOUT == expected_timeout
        
        with patch.object(sync_engine.session, 'get') as mock_get:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.json.return_value = {}
            mock_resp.content = b""
            mock_get.return_value = mock_resp
            
            # 1. fetch_activities
            sync_engine.fetch_activities()
            assert mock_get.call_args[1].get('timeout') == expected_timeout
            
            # 2. fetch_activity_detail
            sync_engine.fetch_activity_detail('test_id')
            assert mock_get.call_args[1].get('timeout') == expected_timeout
            
            # 3. fetch_activity_intervals
            sync_engine.fetch_activity_intervals('test_id')
            assert mock_get.call_args[1].get('timeout') == expected_timeout
            
            # 4. fetch_activity_fit_laps
            sync_engine.fetch_activity_fit_laps('test_id')
            assert mock_get.call_args[1].get('timeout') == expected_timeout
            
            # 5. fetch_wellness
            sync_engine.fetch_wellness()
            assert mock_get.call_args[1].get('timeout') == expected_timeout


class TestWorkerAdversarialExecution:
    """Execute the Node.js adversarial suite directly from pytest."""

    def test_run_node_adversarial_suite(self):
        """Runs tests/test_adversarial_worker_m1.mjs ensuring all 28 adversarial assertions pass."""
        compiled_worker = os.path.join(BASE_DIR, 'tests', 'worker_compiled.mjs')
        index_ts = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
        
        # Ensure fresh build if missing or outdated
        if not os.path.isfile(compiled_worker) or os.path.getmtime(index_ts) > os.path.getmtime(compiled_worker):
            subprocess.run(
                ['npx', 'esbuild', index_ts, '--format=esm', f'--outfile={compiled_worker}'],
                cwd=BASE_DIR,
                check=True,
                shell=True
            )

        script_path = os.path.join(BASE_DIR, 'tests', 'test_adversarial_worker_m1.mjs')
        assert os.path.isfile(script_path), "test_adversarial_worker_m1.mjs must exist"
        
        result = subprocess.run(
            ['node', script_path],
            cwd=BASE_DIR,
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Node adversarial tests failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        assert "ALL CHALLENGE TESTS PASSED: 28/28" in result.stdout
