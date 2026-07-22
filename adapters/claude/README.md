# Claude adapter

Use [`skills/build-apex-brand-reports/SKILL.md`](../../skills/build-apex-brand-reports/SKILL.md) as the single operational contract. Claude products do not all expose the same native skill installation mechanism, so select the method actually supported by the environment.

## `CLAUDE.md` fragment

```markdown
When asked to create, install, update, or validate branded Oracle APEX reports, read `/path/to/oracle-apex-brand-report-kit/skills/build-apex-brand-reports/SKILL.md` first and follow its routed references. Do not duplicate or rewrite the skill. Read this project's instructions before action and preserve the four-layer ownership boundary.
```

If the environment supports project knowledge or reusable instruction files, add the skill directory without changing its contents. If it does not, tell the agent to read the central `SKILL.md` and only the references it routes for the task. The agent still needs file editing and command execution; browser, database, PDF, and spreadsheet capabilities are optional but required to claim their respective validations.

Install the two pinned Python dependencies from the copied skill's `requirements.txt` before running its validation or scaffolding scripts.

Update by replacing the referenced skill directory with a verified tagged version, then run the consumer runtime's dry-run upgrade flow. Never auto-edit global Claude configuration.
