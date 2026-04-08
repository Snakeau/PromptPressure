"""Scenario registry – maps modes/suites to scenario lists."""

from __future__ import annotations

from promptpressure.suites.scenarios import (
    ALL_SCENARIOS,
    DX_SCENARIOS,
    PI_SCENARIOS,
    SP_SCENARIOS,
    TA_SCENARIOS,
)

# quick_check: first 5 from each suite
_QUICK_PI = PI_SCENARIOS[:5]
_QUICK_SP = SP_SCENARIOS[:5]
_QUICK_DX = DX_SCENARIOS[:4]
_QUICK_TA = TA_SCENARIOS[:5]
_QUICK_CHECK = _QUICK_PI + _QUICK_SP + _QUICK_DX + _QUICK_TA

MODES: dict[str, dict] = {
    "quick_check": {
        "scenarios": _QUICK_CHECK,
        "description": "Rapid scan – first scenarios from each suite",
    },
    "full": {
        "scenarios": ALL_SCENARIOS,
        "description": "Complete scan – all scenarios across all suites",
    },
    "pi_suite": {
        "scenarios": PI_SCENARIOS,
        "description": "Prompt Injection suite (PI-01…PI-20)",
    },
    "sp_suite": {
        "scenarios": SP_SCENARIOS,
        "description": "System Prompt Disclosure suite (SP-01…SP-12)",
    },
    "dx_suite": {
        "scenarios": DX_SCENARIOS,
        "description": "Data Exfiltration suite (DX-01…DX-08)",
    },
    "ta_suite": {
        "scenarios": TA_SCENARIOS,
        "description": "Tool Abuse suite (TA-01…TA-15)",
    },
}


def get_scenarios(mode: str) -> list[dict]:
    """Return scenario list for *mode*. Raises KeyError if unknown."""
    return MODES[mode]["scenarios"]


def all_scenario_ids() -> list[str]:
    return [s["id"] for s in ALL_SCENARIOS]
