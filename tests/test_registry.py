"""Tests for the scenario registry completeness."""

from __future__ import annotations

import re

import pytest

from promptpressure.suites.registry import MODES, get_scenarios
from promptpressure.suites.scenarios import (
    ALL_SCENARIOS,
    DX_SCENARIOS,
    PI_SCENARIOS,
    SP_SCENARIOS,
    TA_SCENARIOS,
)


class TestScenarioCounts:
    def test_pi_count(self):
        assert len(PI_SCENARIOS) == 20

    def test_sp_count(self):
        assert len(SP_SCENARIOS) == 12

    def test_dx_count(self):
        assert len(DX_SCENARIOS) == 8

    def test_ta_count(self):
        assert len(TA_SCENARIOS) == 15

    def test_total_count(self):
        assert len(ALL_SCENARIOS) == 55


class TestScenarioIdFormat:
    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_id_format(self, scenario):
        """Each scenario ID must match PI-NN, SP-NN, DX-NN, or TA-NN."""
        assert re.fullmatch(r"(PI|SP|DX|TA)-\d{2}", scenario["id"]), (
            f"Bad ID format: {scenario['id']}"
        )

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_suite_matches_id_prefix(self, scenario):
        prefix = scenario["id"].split("-")[0]
        assert scenario["suite"] == prefix

    def test_all_ids_unique(self):
        ids = [s["id"] for s in ALL_SCENARIOS]
        assert len(ids) == len(set(ids)), "Duplicate scenario IDs found"


class TestScenarioIdSequence:
    def test_pi_ids(self):
        ids = [s["id"] for s in PI_SCENARIOS]
        expected = [f"PI-{i:02d}" for i in range(1, 21)]
        assert ids == expected

    def test_sp_ids(self):
        ids = [s["id"] for s in SP_SCENARIOS]
        expected = [f"SP-{i:02d}" for i in range(1, 13)]
        assert ids == expected

    def test_dx_ids(self):
        ids = [s["id"] for s in DX_SCENARIOS]
        expected = [f"DX-{i:02d}" for i in range(1, 9)]
        assert ids == expected

    def test_ta_ids(self):
        ids = [s["id"] for s in TA_SCENARIOS]
        expected = [f"TA-{i:02d}" for i in range(1, 16)]
        assert ids == expected


class TestScenarioFields:
    required_fields = {"id", "suite", "name", "prompt", "default_severity", "check"}
    valid_severities = {"critical", "high", "medium", "low"}

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_has_required_fields(self, scenario):
        missing = self.required_fields - set(scenario.keys())
        assert not missing, f"{scenario['id']} missing fields: {missing}"

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_valid_severity(self, scenario):
        assert scenario["default_severity"] in self.valid_severities

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_prompt_is_nonempty(self, scenario):
        assert scenario["prompt"].strip(), f"{scenario['id']} has empty prompt"

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_check_is_callable(self, scenario):
        assert callable(scenario["check"]), f"{scenario['id']} check is not callable"

    @pytest.mark.parametrize("scenario", ALL_SCENARIOS)
    def test_check_returns_tuple(self, scenario):
        triggered, detail = scenario["check"]("sample response text")
        assert isinstance(triggered, bool)
        assert isinstance(detail, str)


class TestModeRegistry:
    def test_all_modes_exist(self):
        expected = {"quick_check", "full", "pi_suite", "sp_suite", "dx_suite", "ta_suite"}
        assert expected.issubset(set(MODES.keys()))

    def test_quick_check_count(self):
        assert len(get_scenarios("quick_check")) == 19

    def test_full_count(self):
        assert len(get_scenarios("full")) == 55

    def test_pi_suite_count(self):
        assert len(get_scenarios("pi_suite")) == 20

    def test_sp_suite_count(self):
        assert len(get_scenarios("sp_suite")) == 12

    def test_dx_suite_count(self):
        assert len(get_scenarios("dx_suite")) == 8

    def test_ta_suite_count(self):
        assert len(get_scenarios("ta_suite")) == 15

    def test_unknown_mode_raises(self):
        with pytest.raises(KeyError):
            get_scenarios("nonexistent_mode")
