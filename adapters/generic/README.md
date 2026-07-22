# Generic agent adapter

## Short prompt

```text
Read /path/to/oracle-apex-brand-report-kit/skills/build-apex-brand-reports/SKILL.md and follow only the references it routes for this task. Read the consumer project's instructions first. Keep engine, theme, document structure, and business content separate. Run dry-run and validation before any write or publication.
```

## Minimum capabilities

- Read Markdown, JSON, YAML, SQL, PL/SQL, CSS, and JavaScript.
- Edit files without silently overwriting unrelated work.
- Run Python commands and inspect diffs.
- Respect explicit authorization boundaries.

Without a browser, the agent may scaffold but must not claim responsive or interaction validation. Without database access, it must keep PL/SQL repository-only and report compilation as untested. Without PDF rendering, it must not claim page-by-page PDF inspection. Without spreadsheet tooling, it must not claim XLSX typing or repair validation.

Agents without a native skill mechanism should read the central contract manually and load only the referenced file needed for the current phase. Do not create a separate implementation of the skill.

The copied skill is self-describing: install the pinned libraries from `skills/build-apex-brand-reports/requirements.txt` before running its Python scripts.
