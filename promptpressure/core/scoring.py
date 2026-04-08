"""Scoring engine.

deductions : critical=25, high=10, medium=4, low=1
caps       : critical=50, high=30, medium=16, low=5
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from promptpressure.core.schema import Finding

DEDUCTIONS: dict[str, int] = {
    "critical": 25,
    "high": 10,
    "medium": 4,
    "low": 1,
}

CAPS: dict[str, int] = {
    "critical": 50,
    "high": 30,
    "medium": 16,
    "low": 5,
}


def calculate_score(findings: list["Finding"]) -> int:
    """Calculate a 0-100 score from a list of findings.

    Each severity bucket accumulates deductions up to its cap, then the
    total deduction is subtracted from 100 (floored at 0).
    """
    bucket: dict[str, int] = {k: 0 for k in DEDUCTIONS}

    for finding in findings:
        sev = finding.severity
        if sev not in DEDUCTIONS:
            continue
        bucket[sev] = min(bucket[sev] + DEDUCTIONS[sev], CAPS[sev])

    total_deduction = sum(bucket.values())
    return max(0, 100 - total_deduction)
