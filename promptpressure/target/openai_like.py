"""OpenAI-like HTTP target client.

Sends a minimal POST /v1/chat/completions payload and returns the assistant
message text.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any


class OpenAILikeClient:
    """Thin wrapper around urllib to call an OpenAI-compatible chat endpoint."""

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        timeout: int = 30,
    ) -> None:
        self.url = url.rstrip("/")
        # Ensure path ends at /v1/chat/completions
        if not self.url.endswith("/v1/chat/completions"):
            self.url = self.url.rstrip("/") + "/v1/chat/completions"
        self.headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if headers:
            self.headers.update(headers)
        self.timeout = timeout

    def chat(self, user_message: str, model: str = "gpt-3.5-turbo") -> tuple[str, int]:
        """Send a single-turn chat request.

        Returns (assistant_text, http_status_code).
        Raises RuntimeError on connection / parse errors.
        """
        payload: dict[str, Any] = {
            "model": model,
            "messages": [{"role": "user", "content": user_message}],
            "max_tokens": 512,
            "temperature": 0,
        }
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            self.url,
            data=body,
            headers=self.headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            status = exc.code
            try:
                data = json.loads(exc.read().decode())
            except Exception:
                data = {}
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Connection failed: {exc.reason}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Invalid JSON response: {exc}") from exc

        text = _extract_text(data)
        return text, status


def _extract_text(data: dict[str, Any]) -> str:
    """Extract assistant message from an OpenAI-format response dict."""
    try:
        return data["choices"][0]["message"]["content"] or ""
    except (KeyError, IndexError, TypeError):
        # Fallback: return whatever we got as a string
        return json.dumps(data)


def headers_from_strings(raw: list[str]) -> dict[str, str]:
    """Parse ``['Key: Value', ...]`` into a dict."""
    result: dict[str, str] = {}
    for item in raw:
        if ":" in item:
            key, _, value = item.partition(":")
            result[key.strip()] = value.strip()
    return result
