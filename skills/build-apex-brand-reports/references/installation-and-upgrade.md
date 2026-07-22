# Installation and upgrade

## Install the skill

Install from a tagged release, a verified Git commit, or a local copy. Copy only `skills/build-apex-brand-reports` into the chosen skill directory, then install the two pinned Python libraries from that directory's `requirements.txt`. Do not mutate global configuration automatically. Validate with the official skill validator after copying.

## Scaffold a consumer

1. Validate `brand-profile` and `report-profile`.
2. Commit or stash the consumer project's scoped work so Git can provide rollback.
3. Run `scaffold_project.py --dry-run` and review every path and diff.
4. Run without `--dry-run` only after confirming ownership and local conventions.
5. Validate `.apex-brand-report-kit/installation-manifest.json` and generated files.
6. Review PL/SQL and Page Designer instructions before any compilation or APEX change.

The scaffolder never connects, compiles, commits, pushes, or overwrites an existing file without `--force`. It writes the manifest last.

## Upgrade the runtime

Run `--update --dry-run`. The scaffolder compares current files with manifest checksums. It updates engine-managed files only when unchanged since installation. It preserves theme-managed and project-owned files. A modified engine file is a conflict; review it, merge deliberately, and rerun. `--force` is an explicit override for reviewed engine conflicts, not a way to replace themes or business code.

After applying, validate the scaffold and run browser, PDF, and spreadsheet regression checks. Roll back with the consumer project's Git history if validation fails.
