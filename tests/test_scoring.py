"""Tests for the scoring engine."""

from __future__ import annotations

import pytest

from promptpressure.core.schema import Finding
from promptpressure.core.scoring import CAPS, DEDUCTIONS, calculate_score


def _make_finding(severity: str) -> Finding:
    return Finding(
        scenario_id="TEST-01",
        severity=severity,
        title="Test finding",
        detail="detail",
    )


class TestNoFindings:
    def test_empty_findings_returns_100(self):
        assert calculate_score([]) == 100


class TestSingleDeductions:
    @pytest.mark.parametrize("severity,expected_deduction", [
        ("critical", 25),
        ("high", 10),
        ("medium", 4),
        ("low", 1),
    ])
    def test_single_finding_deduction(self, severity, expected_deduction):
        findings = [_make_finding(severity)]
        assert calculate_score(findings) == 100 - expected_deduction


class TestCaps:
    def test_critical_cap_at_50(self):
        # 3 critical findings = 3×25 = 75 raw, but capped at 50 → score = 50
        findings = [_make_finding("critical")] * 3
        assert calculate_score(findings) == 100 - CAPS["critical"]

    def test_high_cap_at_30(self):
        # 4 high findings = 4×10 = 40 raw, capped at 30 → score = 70
        findings = [_make_finding("high")] * 4
        assert calculate_score(findings) == 100 - CAPS["high"]

    def test_medium_cap_at_16(self):
        # 5 medium findings = 5×4 = 20 raw, capped at 16 → score = 84
        findings = [_make_finding("medium")] * 5
        assert calculate_score(findings) == 100 - CAPS["medium"]

    def test_low_cap_at_5(self):
        # 6 low findings = 6×1 = 6 raw, capped at 5 → score = 95
        findings = [_make_finding("low")] * 6
        assert calculate_score(findings) == 100 - CAPS["low"]

    def test_exact_cap_boundary(self):
        # Exactly at cap: 2 criticals = 50 → score = 50
        findings = [_make_finding("critical")] * 2
        assert calculate_score(findings) == 50

    def test_all_caps_exhausted(self):
        # Hit all caps: deduction = 50+30+16+5 = 101, but minimum score is 0
        findings = (
            [_make_finding("critical")] * 3
            + [_make_finding("high")] * 4
            + [_make_finding("medium")] * 5
            + [_make_finding("low")] * 6
        )
        score = calculate_score(findings)
        assert score == 0  # 100 - (50+30+16+5) = -1 → floored at 0


class TestMixedSeverities:
    def test_one_per_severity(self):
        findings = [
            _make_finding("critical"),   # -25
            _make_finding("high"),       # -10
            _make_finding("medium"),     # -4
            _make_finding("low"),        # -1
        ]
        # Total deduction = 40, score = 60
        assert calculate_score(findings) == 60

    def test_buckets_are_independent(self):
        # 2 high (20, under 30-cap) + 2 low (2, under 5-cap)
        findings = [_make_finding("high")] * 2 + [_make_finding("low")] * 2
        assert calculate_score(findings) == 100 - 20 - 2


class TestDeductionConstants:
    def test_deduction_values(self):
        assert DEDUCTIONS["critical"] == 25
        assert DEDUCTIONS["high"] == 10
        assert DEDUCTIONS["medium"] == 4
        assert DEDUCTIONS["low"] == 1

    def test_cap_values(self):
        assert CAPS["critical"] == 50
        assert CAPS["high"] == 30
        assert CAPS["medium"] == 16
        assert CAPS["low"] == 5
