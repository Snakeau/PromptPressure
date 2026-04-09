# Promotion Texts

Ready-to-post texts for different platforms. Adapt as needed.

---

## Hacker News (Show HN)

**Title:** Show HN: PromptPressure – Red-team your AI agents from the terminal

**Text:**
```
Hi HN,

I built PromptPressure — an open-source CLI tool that runs adversarial security
scenarios against any OpenAI-compatible AI endpoint and produces a scored report.

Problem: LLM-powered agents are increasingly deployed in production, but there's
no easy way to check if they leak system prompts, follow injected instructions,
or can be tricked into calling dangerous tools. Commercial red-teaming platforms
exist but they're expensive and opaque.

PromptPressure runs 55 scenarios across 4 categories:
- Prompt Injection (20 scenarios)
- System Prompt Disclosure (12 scenarios)
- Data Exfiltration (8 scenarios)
- Tool Abuse (15 scenarios)

It works locally, outputs JSON, and integrates as a GitHub Action for CI/CD gating.
Comes with a mock vulnerable server for demos.

pip install promptpressure
promptpressure scan --url https://your-agent/v1 --mode quick_check

MIT licensed. Feedback and scenario contributions welcome.

https://github.com/Snakeau/PromptPressure
```

---

## Reddit r/netsec

**Title:** PromptPressure: open-source CLI red-teaming scanner for LLM agents (55 adversarial scenarios)

**Text:**
```
Released an open-source tool for automated adversarial testing of AI/LLM endpoints.

Runs 55 scenarios covering prompt injection, system prompt disclosure,
data exfiltration, and tool abuse (SSRF, code exec, email exfil, SQLi).

Works against any OpenAI-compatible endpoint. Outputs scored JSON reports
with severity-based findings. Ships with a GitHub Action for CI/CD.

Includes a mock vulnerable AI server with 3 modes for demos and testing.

Install: pip install promptpressure
GitHub: https://github.com/Snakeau/PromptPressure

MIT license. Looking for feedback from the security community — especially
on scenario coverage and detection heuristics.
```

---

## Reddit r/LocalLLaMA

**Title:** Built an open-source red-teaming tool to test your local LLM agents for security issues

**Text:**
```
If you're running local LLM agents with OpenAI-compatible APIs (llama.cpp server,
Ollama, vLLM, etc.), PromptPressure can test them for common vulnerabilities:

- Does your agent leak its system prompt?
- Can it be jailbroken with prompt injection?
- Will it exfiltrate data if asked cleverly?
- Can it be tricked into calling dangerous tools?

55 adversarial scenarios, runs entirely locally, outputs a scored JSON report.

pip install promptpressure
promptpressure scan --url http://localhost:8080/v1 --mode full

Includes a built-in mock vulnerable server to see what a bad scan looks like.

Source: https://github.com/Snakeau/PromptPressure
```

---

## Reddit r/cybersecurity

**Title:** Open-source AI red-teaming scanner — 55 adversarial scenarios for LLM agent security testing

**Text:**
```
PromptPressure is an open-source CLI tool that pressure-tests AI agents and
LLM endpoints for security weaknesses.

4 test suites:
- PI: Prompt Injection (persona hijacking, instruction override, encoding tricks)
- SP: System Prompt Disclosure (direct requests, refusal analysis, metadata leaks)
- DX: Data Exfiltration (PII extraction, secret enumeration, context dumping)
- TA: Tool Abuse (SSRF, code execution, email exfil, SQL injection via tools)

Designed for DevSecOps — integrates as a GitHub Action to gate deployments
on AI security scores.

MIT license, Python 3.11+.

https://github.com/Snakeau/PromptPressure
```

---

## Twitter/X

### Thread (3 tweets):

**Tweet 1:**
```
🔴 Released PromptPressure — open-source CLI to red-team your AI agents.

55 adversarial scenarios. 4 attack categories. Scored JSON reports.

pip install promptpressure

Works against any OpenAI-compatible endpoint.

github.com/Snakeau/PromptPressure
```

**Tweet 2:**
```
What it tests:
→ Prompt injection (20 scenarios)
→ System prompt disclosure (12)
→ Data exfiltration (8)
→ Tool abuse — SSRF, code exec, SQLi (15)

Runs locally. Ships with a GitHub Action for CI/CD gating.
```

**Tweet 3:**
```
Includes a built-in mock vulnerable AI server for demos:

promptpressure mock-agent --mode tool_abuse_sim
promptpressure scan --url http://localhost:8010 --mode full

MIT license. Contributions welcome — especially new attack scenarios.
```

---

## LinkedIn

**Text:**
```
Excited to share PromptPressure — an open-source tool I built for
automated security testing of AI agents.

As LLM-powered applications move into production, security testing
hasn't kept pace. PromptPressure fills this gap:

→ 55 adversarial scenarios across 4 categories
→ Tests prompt injection, system prompt leaks, data exfiltration, and tool abuse
→ Works against any OpenAI-compatible endpoint
→ Produces scored security reports (JSON)
→ Integrates as a GitHub Action for CI/CD security gates

It runs entirely locally — no data leaves your machine.

The tool is MIT-licensed and designed for DevSecOps teams who want
to add AI security testing to their pipeline without vendor lock-in.

Install: pip install promptpressure
Source: https://github.com/Snakeau/PromptPressure

Looking for feedback from the AI security and DevSecOps community.
What scenarios would you add?

#AISecurity #LLM #RedTeaming #DevSecOps #OpenSource #CyberSecurity
```

---

## Dev.to / Medium article title ideas

1. "How I Built an Open-Source AI Red-Teaming Tool in Python"
2. "55 Ways Your AI Agent Can Be Attacked (and How to Test for Them)"
3. "Adding AI Security Testing to Your CI/CD Pipeline with PromptPressure"
4. "Why Every LLM Agent Needs a Security Scan Before Production"

---

## Awesome Lists to submit to

- `awesome-llm-security` — PR to add PromptPressure
- `awesome-ai-security` — PR to add
- `awesome-pentest` — PR to add under AI/LLM section
- `awesome-devsecops` — PR to add under testing tools

To submit: fork the repo, add a line in the appropriate section, open a PR.
