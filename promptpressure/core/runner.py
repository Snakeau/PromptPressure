"""Scan runner – orchestrates scenarios against a target and produces a ScanResult."""

from __future__ import annotations

from promptpressure.core.schema import Finding, ScanResult, Transcript, badge_for_score
from promptpressure.core.scoring import calculate_score
from promptpressure.suites.registry import get_scenarios
from promptpressure.target.openai_like import OpenAILikeClient


def run_scan(
    url: str,
    mode: str = "quick_check",
    headers: dict[str, str] | None = None,
    scanner_version: str = "",
    timeout: int = 30,
    on_scenario_start: object = None,
) -> ScanResult:
    """Execute a full scan and return a :class:`ScanResult`.

    Parameters
    ----------
    url:
        Base URL of the OpenAI-like target (the client appends ``/v1/chat/completions``).
    mode:
        One of the registered mode names (e.g. ``quick_check``, ``full``).
    headers:
        Extra HTTP headers (e.g. ``{"Authorization": "Bearer …"}``).
    scanner_version:
        Version string embedded in the result metadata.
    timeout:
        Per-request timeout in seconds.
    on_scenario_start:
        Optional callable ``(scenario_id, name) -> None`` called before each scenario.
    """
    scenarios = get_scenarios(mode)
    client = OpenAILikeClient(url, headers=headers, timeout=timeout)
    result = ScanResult(target_url=url, mode=mode, scanner_version=scanner_version)

    for scenario in scenarios:
        sid = scenario["id"]
        name = scenario["name"]
        prompt = scenario["prompt"]
        default_severity = scenario["default_severity"]
        check_fn = scenario["check"]

        if callable(on_scenario_start):
            on_scenario_start(sid, name)  # type: ignore[call-arg]

        response_text = ""
        status_code = 0
        error: str | None = None

        try:
            response_text, status_code = client.chat(prompt)
        except RuntimeError as exc:
            error = str(exc)
            response_text = ""
            status_code = 0

        transcript = Transcript(
            scenario_id=sid,
            request={"prompt": prompt[:300]},
            response_text=response_text,
            status_code=status_code,
            error=error,
        )
        result.transcripts.append(transcript)

        if error:
            # Connection/parse errors are logged but don't create a finding
            continue

        triggered, detail = check_fn(response_text)
        if triggered:
            finding = Finding(
                scenario_id=sid,
                severity=default_severity,
                title=name,
                detail=detail,
                request_excerpt=prompt[:200],
                response_excerpt=response_text[:300],
            )
            result.findings.append(finding)

    result.score = calculate_score(result.findings)
    result.badge = badge_for_score(result.score)
    return result
