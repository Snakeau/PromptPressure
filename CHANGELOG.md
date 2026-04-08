# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.1] - 2026-04-08

### Added
- `doctor` CLI command for environment diagnostics

### Fixed
- Updated release workflow action versions

## [0.1.0] - 2026-04-08

### Added
- Initial open-core local scanner implementation
- 55 adversarial scenarios across 4 suites:
  - **PI** — Prompt Injection (20 scenarios)
  - **SP** — System Prompt Disclosure (12 scenarios)
  - **DX** — Data Exfiltration (8 scenarios)
  - **TA** — Tool Abuse (15 scenarios)
- CLI commands: `scan`, `list-suites`, `mock-agent`, `doctor`
- Scoring engine with severity-based deductions and caps
- Mock vulnerable AI agent server (3 modes)
- OpenAI-compatible endpoint targeting
- JSON result output with findings and transcripts
- GitHub Action (`scan-action`) for CI/CD integration
- PyPI package distribution
- 6 scan modes: `quick_check`, `full`, `pi_suite`, `sp_suite`, `dx_suite`, `ta_suite`

[0.1.1]: https://github.com/Snakeau/PromptPressure/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/Snakeau/PromptPressure/releases/tag/v0.1.0
