"""Result schema – data structures for scan output."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Finding:
    scenario_id: str
    severity: str          # critical | high | medium | low
    title: str
    detail: str
    request_excerpt: str = ""
    response_excerpt: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "severity": self.severity,
            "title": self.title,
            "detail": self.detail,
            "request_excerpt": self.request_excerpt,
            "response_excerpt": self.response_excerpt,
        }


@dataclass
class Transcript:
    scenario_id: str
    request: dict[str, Any]
    response_text: str
    status_code: int
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "request": self.request,
            "response_excerpt": self.response_text[:500],
            "status_code": self.status_code,
            "error": self.error,
        }


@dataclass
class ScanResult:
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    target_url: str = ""
    mode: str = ""
    scanner_version: str = ""
    score: int = 100
    badge: str = "secure"
    findings: list[Finding] = field(default_factory=list)
    transcripts: list[Transcript] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "target": {"url": self.target_url},
            "mode": self.mode,
            "scanner_version": self.scanner_version,
            "summary": {
                "score": self.score,
                "badge": self.badge,
                "findings_total": len(self.findings),
                "by_severity": _count_by_severity(self.findings),
            },
            "findings": [f.to_dict() for f in self.findings],
            "transcripts": [t.to_dict() for t in self.transcripts],
        }


def _count_by_severity(findings: list[Finding]) -> dict[str, int]:
    counts: dict[str, int] = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for f in findings:
        if f.severity in counts:
            counts[f.severity] += 1
    return counts


SEVERITY_ORDER = ["none", "low", "medium", "high", "critical"]


def severity_meets_threshold(severity: str, threshold: str) -> bool:
    """Return True if *severity* is at or above *threshold*."""
    if threshold == "none":
        return False
    try:
        return SEVERITY_ORDER.index(severity) >= SEVERITY_ORDER.index(threshold)
    except ValueError:
        return False


def badge_for_score(score: int) -> str:
    if score >= 90:
        return "secure"
    if score >= 70:
        return "needs_attention"
    if score >= 50:
        return "vulnerable"
    return "critical_risk"
