# Codex adapter

Codex uses the central [`SKILL.md`](../../skills/build-apex-brand-reports/SKILL.md) directly. This adapter adds installation and invocation examples; it is not a second implementation.

## Install from GitHub

```bash
git clone --depth 1 https://github.com/andre-simplifica/oracle-apex-brand-report-kit.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R oracle-apex-brand-report-kit/skills/build-apex-brand-reports "${CODEX_HOME:-$HOME/.codex}/skills/"
```

No Python installation is required for Codex to read the skill, inspect the visual source, and create the Oracle APEX runtime. To use the optional deterministic scaffolder and validators, install their pinned dependencies separately:

```bash
python -m pip install -r "${CODEX_HOME:-$HOME/.codex}/skills/build-apex-brand-reports/requirements.txt"
```

## Install from a release

Download `build-apex-brand-reports-0.3.0.zip`, verify the release and checksum, then extract its `build-apex-brand-reports` directory into `${CODEX_HOME:-$HOME/.codex}/skills/`. Restart or open a new Codex task so discovery refreshes. Install `requirements.txt` only if you choose to run the optional Python scripts.

## Install locally or in a custom directory

```bash
cp -R skills/build-apex-brand-reports "${CODEX_HOME:-$HOME/.codex}/skills/"
cp -R skills/build-apex-brand-reports /path/to/custom-skills/
```

Do not modify global Codex settings automatically. If a custom directory is not discovered natively, reference the absolute `SKILL.md` path in the task.

## Optional `AGENTS.md` fragment

```markdown
For branded Oracle APEX application screens, dashboards, help experiences, and reports, use `$build-apex-brand-reports`. Read the project instructions and confirm the existing domain package, APEX version, authorization, locks, and publication policy before changing files or the database. Keep engine, theme, document structure, and business content separate.
```

## Invoke

```text
Use $build-apex-brand-reports.

Project Oracle APEX: /path/to/project
Official visual identity source: /path/or/url
Application and environment: app 100, DEV
Goal: create a responsive application screen and a modal report with print, PDF, and XLSX.
Existing business package: PK_REPORTS
Desired RETURN CLOB function: FUNC_OPERATIONS_REPORT
Access policy: CONFIRMED_AUTHORIZATION_SCHEME and organization scope
```

## Update

Install the newer tagged skill into a temporary directory, compare it with the installed copy, then replace the skill directory. In each consumer project, either use the agent-native comparison workflow or run the optional `scaffold_project.py --update --dry-run`. Inspect every diff and preserve theme and business files.
