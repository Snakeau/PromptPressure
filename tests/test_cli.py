"""CLI tests for user-facing commands."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from promptpressure import __version__
from promptpressure.cli import app

runner = CliRunner()


class TestDoctorCommand:
    def test_doctor_without_args_succeeds(self):
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        assert "PromptPressure Doctor" in result.stdout
        assert f"version {__version__}" in result.stdout
        assert "WARN: not provided" in result.stdout

    def test_doctor_rejects_invalid_auth_header(self):
        result = runner.invoke(app, ["doctor", "--auth-header", "Bearer token"])
        assert result.exit_code == 0
        assert "FAIL: Header must use 'Key: Value' format." in result.stdout

    def test_doctor_rejects_invalid_url(self):
        result = runner.invoke(app, ["doctor", "--url", "localhost:8010"])
        assert result.exit_code == 0
        assert "FAIL: use a full http:// or https:// URL" in result.stdout

    def test_doctor_validates_output_path(self, tmp_path: Path):
        output_path = tmp_path / "results.json"
        result = runner.invoke(app, ["doctor", "--output-json", str(output_path)])
        assert result.exit_code == 0
        assert "OK: output path is writable:" in result.stdout
