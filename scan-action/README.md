# PromptPressure Scan Action

Reusable GitHub Action to run an automated AI red-team scan against any
OpenAI-compatible endpoint as part of your CI/CD pipeline.

## Inputs

| Input | Required | Default | Description |
|---|---|---|---|
| `url` | ✅ | — | Target base URL (OpenAI-compatible endpoint) |
| `mode` | | `quick_check` | Scan mode: `quick_check`, `full`, `pi_suite`, `sp_suite`, `dx_suite`, `ta_suite` |
| `output-json` | | `promptpressure-results.json` | Path to write results JSON |
| `fail-on` | | `high` | Fail step if any finding ≥ this severity: `none`, `low`, `medium`, `high`, `critical` |
| `auth-header` | | — | Authorization header, e.g. `Authorization: Bearer sk-...` |
| `extra-headers` | | — | Additional headers, one per line: `Key: Value` |
| `python-version` | | `3.11` | Python version for the runner |

## Outputs

| Output | Description |
|---|---|
| `score` | Overall security score (0–100) |
| `badge` | Score label: `secure`, `needs_attention`, `vulnerable`, `critical_risk` |
| `findings-count` | Total number of findings |

## Usage Examples

### Basic scan with fail-on-high (CI gate)

```yaml
name: AI Security Scan

on:
  push:
    branches: [main]
  pull_request:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run PromptPressure scan
        uses: Snakeau/PromptPressure/scan-action@main
        with:
          url: 'https://api.openai.com/v1'
          auth-header: 'Authorization: Bearer ${{ secrets.OPENAI_API_KEY }}'
          mode: quick_check
          fail-on: high
```

### Full scan against a custom endpoint

```yaml
      - name: Full AI red-team scan
        uses: Snakeau/PromptPressure/scan-action@main
        with:
          url: 'https://my-agent.example.com'
          auth-header: 'Authorization: Bearer ${{ secrets.AGENT_API_KEY }}'
          mode: full
          fail-on: critical
          output-json: security-report.json
```

### Scan and display results without failing

```yaml
      - name: Scan (advisory only)
        id: pp_scan
        uses: Snakeau/PromptPressure/scan-action@main
        with:
          url: 'https://my-agent.example.com'
          fail-on: none

      - name: Print score
        run: |
          echo "Score: ${{ steps.pp_scan.outputs.score }}"
          echo "Badge: ${{ steps.pp_scan.outputs.badge }}"
          echo "Findings: ${{ steps.pp_scan.outputs.findings-count }}"
```

### Scan a local mock agent (for testing the action itself)

```yaml
jobs:
  scan-mock:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install and start mock agent
        run: |
          pip install -e .
          promptpressure mock-agent --port 8010 --mode leaky_system_prompt &
          sleep 2

      - name: Run scan against mock
        uses: Snakeau/PromptPressure/scan-action@main
        with:
          url: 'http://localhost:8010'
          mode: quick_check
          fail-on: none   # mock is intentionally vulnerable
```

### Using extra headers

```yaml
      - name: Scan with custom headers
        uses: Snakeau/PromptPressure/scan-action@main
        with:
          url: 'https://my-agent.example.com'
          auth-header: 'Authorization: Bearer ${{ secrets.API_KEY }}'
          extra-headers: |
            X-Custom-Header: my-value
            X-Tenant-ID: acme-corp
```

## Scan Modes

| Mode | Scenarios | Description |
|---|---|---|
| `quick_check` | 19 | Rapid scan – representative selection from each suite |
| `full` | 55 | Complete scan – all scenarios |
| `pi_suite` | 20 | Prompt Injection (PI-01…PI-20) |
| `sp_suite` | 12 | System Prompt Disclosure (SP-01…SP-12) |
| `dx_suite` | 8 | Data Exfiltration (DX-01…DX-08) |
| `ta_suite` | 15 | Tool Abuse (TA-01…TA-15) |

## Score Badges

| Score | Badge | Meaning |
|---|---|---|
| 90–100 | `secure` | No significant findings |
| 70–89 | `needs_attention` | Minor vulnerabilities found |
| 50–69 | `vulnerable` | Significant vulnerabilities present |
| 0–49 | `critical_risk` | Critical vulnerabilities – do not deploy |
