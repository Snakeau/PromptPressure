# Contributing to PromptPressure

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/PromptPressure.git
   cd PromptPressure
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```
4. Run tests to verify setup:
   ```bash
   pytest
   ```

## Development Workflow

1. Create a branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests:
   ```bash
   pytest
   ```
4. Commit with a clear message:
   ```bash
   git commit -m "feat: add new scenario for XSS detection"
   ```
5. Push and open a Pull Request

## Commit Messages

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` — new feature or scenario
- `fix:` — bug fix
- `docs:` — documentation only
- `test:` — adding or updating tests
- `refactor:` — code restructuring without behavior change

## Adding New Scenarios

Scenarios live in `promptpressure/suites/scenarios.py`. Each scenario needs:

- A unique ID (e.g., `PI-21`, `DX-09`)
- A severity level (`critical`, `high`, `medium`, `low`)
- A title and prompt
- Detection keywords for response analysis

After adding a scenario, register it in `promptpressure/suites/registry.py` and add a test.

## Code Style

- Python 3.11+
- Type hints where practical
- Keep dependencies minimal — avoid adding new ones unless necessary

## Reporting Issues

- Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) for bugs
- Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) for ideas

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
