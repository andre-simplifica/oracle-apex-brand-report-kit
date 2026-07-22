# Installation and upgrade

## Install the skill

Install from a tagged release, a verified Git commit, or a local copy. Copy only `skills/build-apex-brand-reports` into the chosen skill directory. A capable agent can read and use the skill without Python. Install the pinned libraries from `requirements.txt` only for the optional scaffolder, validators, tests, or package builder. Do not mutate global configuration automatically.

## Choose the execution path

- **Agent-native:** read [agent-native-workflow.md](agent-native-workflow.md), inspect and render the contracts/templates directly, review every diff, and report which optional automation was not run.
- **Optional deterministic tooling:** install `requirements.txt`, validate the profiles, and run the scaffolder with `--dry-run` before writing.

## Scaffold a consumer

1. Review `brand-profile` and `report-profile` against their schemas.
2. Preserve a reviewable rollback path for the consumer project.
3. Review every proposed path and diff; use `scaffold_project.py --dry-run` when the optional tooling is enabled.
4. Write only after confirming ownership and local conventions.
5. Review `.apex-brand-report-kit/installation-manifest.json` and generated files when using the scaffolder; record equivalent ownership when using the agent-native path.
6. Review PL/SQL and Page Designer instructions before any compilation or APEX change.

The scaffolder never connects, compiles, commits, pushes, or overwrites an existing file without `--force`. It writes the manifest last.

## Upgrade the runtime

With the optional tooling, run `--update --dry-run`; the scaffolder compares current files with manifest checksums. Without Python, compare the tagged engine templates and installed ownership/checksum evidence directly. In both paths, update only unchanged engine-managed files, preserve theme-managed and project-owned files, stop on conflicts, and retain rollback evidence. `--force` is only for reviewed engine conflicts.

After applying, validate the scaffold and run browser, PDF, and spreadsheet regression checks. Roll back with the consumer project's Git history if validation fails.
