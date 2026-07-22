# Claude adapter

Use [`skills/build-apex-brand-reports/SKILL.md`](../../skills/build-apex-brand-reports/SKILL.md) as the single operational contract. Claude products do not all expose the same native skill installation mechanism, so select the method actually supported by the environment.

## `CLAUDE.md` fragment

```markdown
When asked to create, install, update, or validate branded Oracle APEX reports, read `/path/to/oracle-apex-brand-report-kit/skills/build-apex-brand-reports/SKILL.md` first and follow its routed references. Do not duplicate or rewrite the skill. Read this project's instructions before action and preserve the four-layer ownership boundary.
```

If the environment supports project knowledge or reusable instruction files, add the skill directory without changing its contents. If it does not, tell the agent to read the central `SKILL.md` and only the references it routes for the task. The agent still needs file editing and command execution; browser, database, PDF, and spreadsheet capabilities are optional but required to claim their respective validations.

Claude Code can perform the identity extraction and generate the PL/SQL/HTML/CSS/JavaScript consumer files without Python. The copied `requirements.txt` is needed only when choosing to run the optional deterministic scaffolder or validators.

Update by replacing the referenced skill directory with a verified tagged version, then compare the consumer runtime through the agent-native or optional scripted upgrade flow. Never auto-edit global Claude configuration.
