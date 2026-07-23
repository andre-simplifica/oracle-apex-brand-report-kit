# Oracle APEX Brand Report Kit

An open-source, agent-ready kit for turning an approved visual identity into maintainable Oracle APEX reports, dashboards, printable documents, browser PDFs, and server-side XLSX/CSV exports.

The repository contains one installable skill, deterministic consumer scaffolding, versioned schemas, generic PL/SQL `RETURN CLOB` templates, a thin-modal blueprint, upgrade manifests, synthetic examples, and validation tooling. The core contract works with Codex, Claude, or any agent that can read Markdown, edit files, and run tools; it does not pretend that every agent has the same native skill mechanism.

The mandatory runtime target is a native Oracle APEX **Dynamic Content** region whose source directly calls a PL/SQL function that `RETURN`s a `CLOB`. The generated CLOB carries the essential HTML, scoped CSS, and idempotent JavaScript, so the report does not depend on an iframe, an external frontend server, a CDN, or a proprietary plug-in. Static Application Files and server-side exports are optional enhancements, never prerequisites for rendering.

> This project is not affiliated with or endorsed by Oracle. Never point the scaffold at production or compile generated source without the consuming project's explicit authorization and controls.

## Problem solved

Branded APEX reports often mix CSS, queries, page behavior, print rules, logos, and authorization in one page or package. That makes a visual refresh risky and makes runtime updates overwrite business customizations. This kit separates those concerns and records file ownership so a reusable engine can evolve without replacing a project's theme, queries, or access rules.

## Architecture

| Layer | Owns | Must not own |
|---|---|---|
| Technical engine | Safe CLOB construction, semantic HTML, scoped CSS hooks, print/PDF behavior, responsive/accessibility behavior, idempotent JS, partial refresh | Brand, queries, app/page IDs, real users, business permissions |
| Visual theme | Licensed logo/assets, tokens, typography, colors, components, breakpoints, print tokens | Business queries or rules |
| Document structure | Header, hero, context, filters, indicators, cards, tables, notes, alerts, signatures, footer, empty/error states | Engine internals or domain ownership |
| Business content | Queries, binds, filters, metrics, scope, permissions, labels, public report function | Reusable engine implementation |

Every consumer receives a manifest that classifies engine-managed, theme-managed, and project-owned files and stores SHA-256 checksums. Runtime upgrades update only unchanged engine-managed files by default.

## Repository layout

```text
skills/build-apex-brand-reports/  central skill, references, scripts, templates
adapters/                         Codex, Claude, and generic-agent adapters
schemas/                          brand, report, and installation contracts
examples/synthetic-company/       original synthetic identity and outputs
tests/                            unit, security, scaffold, and artifact tests
.github/                          CI and community templates
```

## Oracle APEX runtime requirements

- Oracle APEX 24.2 and an Oracle Database environment confirmed by the consumer project.
- One native Dynamic Content region calling a project-owned PL/SQL `RETURN CLOB` function.
- A supported browser for responsive rendering, printing, and Save as PDF.
- Project-approved SQLcl or Page Designer access, locks, and DEV authorization for installation.

**Python is not required by Oracle APEX, the database, the Dynamic Content region, the PL/SQL developer, or the end user.** The generated runtime is PL/SQL, HTML, CSS, and JavaScript only.

## Agent capabilities

Codex, Claude Code, or another capable agent can follow the central `SKILL.md` without Python. It needs to read the official visual source and project instructions, inspect the authorized files or pages, edit the consumer repository, and use the available browser, PDF, database, and spreadsheet tools required by the requested validation.

## Optional reference tooling

- Python 3.10 or newer runs the repository's deterministic scaffolder, validators, tests, and package builder.
- `jsonschema==4.25.1` validates the formal Draft 2020-12 contracts in that optional Python path.
- `PyYAML==6.0.2` safely parses the human-editable YAML configuration in that optional Python path.
- Git provides reviewable diffs and rollback.
- Poppler `pdfinfo` and `pdftoppm` automate PDF inspection when equivalent PDF tooling is unavailable to the agent.

These tools strengthen repeatability and CI; they are not APEX runtime dependencies or prerequisites for agent-led brand extraction.

## Install the skill

### From GitHub

```bash
git clone --depth 1 https://github.com/andre-simplifica/oracle-apex-brand-report-kit.git
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R oracle-apex-brand-report-kit/skills/build-apex-brand-reports "${CODEX_HOME:-$HOME/.codex}/skills/"
```

### From a release

Download `build-apex-brand-reports-0.2.1.zip` from the `v0.2.1` release, verify the published checksum, and extract the `build-apex-brand-reports` directory into `${CODEX_HOME:-$HOME/.codex}/skills/` or another trusted skill directory. No Python installation is required to let a capable agent read and follow the skill.

### From a local checkout

```bash
cp -R skills/build-apex-brand-reports "${CODEX_HOME:-$HOME/.codex}/skills/"
```

### Into a custom directory

```bash
mkdir -p /path/to/custom-skills
cp -R skills/build-apex-brand-reports /path/to/custom-skills/
```

No installer changes global agent configuration. See [Codex](adapters/codex/README.md), [Claude](adapters/claude/README.md), and [generic-agent](adapters/generic/README.md) adapters.

## Optional: enable deterministic Python tooling

Only install these dependencies when you want to run the bundled scaffolder, validators, tests, or package builder:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## Create the first theme

1. Give the agent one official source: public URL, authorized authenticated app, HTML, website, PDF, rendered slides, images, screenshots, asset directory, or brand manual.
2. Require complete navigation, responsive inspection, original-asset discovery, license review, contrast validation, and token provenance.
3. Store the extracted identity only in the authorized consumer project.
4. Check it against the versioned `brand-profile` contract. A capable agent may do this directly. When the optional Python tooling is enabled, also run:

```bash
python skills/build-apex-brand-reports/scripts/validate_theme.py /path/to/brand-profile.json
```

The public repository includes only the original synthetic Acme Harbor identity.

## Optional Apache ECharts integration

When a report explicitly requests a chart, install and invoke
[`$oracle-apex-echarts`](https://github.com/andre-simplifica/oracle-apex-echarts)
from release
[`v1.0.1`](https://github.com/andre-simplifica/oracle-apex-echarts/releases/tag/v1.0.1).
This kit remains responsible for the document, header, filters, KPIs, cards,
tables, print/export, and CLOB composition. Oracle APEX ECharts owns ChartSpec,
chart rendering, lifecycle, accessibility, and its offline bundle.

Embed the chart through `PK_APEX_ECHARTS` inside the Dynamic Content report and
load its shared assets through one approved `RUNTIME_ONLY` plug-in region. Keep
business SQL and authorization in the project-owned domain package. Do not copy
ECharts core files into this repository or a report CLOB, and keep essential
text or tabular content functional when the chart is unavailable. See the
[integration contract](skills/build-apex-brand-reports/references/oracle-apex-echarts.md).

## Configure a report

Copy `examples/synthetic-company/report-kit.yaml` and replace only values confirmed in the consumer project. Important fields include:

```yaml
packages:
  engine: PK_ABRK_ENGINE
  theme: PK_PROJECT_THEME
  owner: PK_EXISTING_DOMAIN
  report_function: FUNC_REPORT_HTML
  export_process: PK_EXISTING_DOMAIN.PROC_EXPORT
apex:
  application_id: 100
  modal_page_id: 900
  authorization_scheme: Confirmed scheme name
theme:
  profile: brand-profile.json
  header: {variant: hero, size: large, show_logo: true}
features: {fullscreen: true, print: true, pdf: true, xlsx: true, csv: false}
document:
  orientation: portrait
  repeat_table_header: true
  show_emission_user: true
  show_emission_datetime: true
  toolbar: full
  toolbar_position: above-header
  content_width: 1180px
  economy_print: false
```

All values must conform to [`report-profile.schema.json`](schemas/report-profile.schema.json). The optional validator enforces the contract deterministically. When XLSX or CSV is enabled, a confirmed project-owned export procedure is required.

## Agent-native workflow without Python

1. Read the consumer project's instructions and the central [`SKILL.md`](skills/build-apex-brand-reports/SKILL.md).
2. Inspect the complete authorized visual source with the agent's browser, PDF, image, presentation, or file tools.
3. Create consumer-owned brand and report profiles following the versioned schemas as contracts.
4. Read and render the templates under `skills/build-apex-brand-reports/assets/`, or create equivalent files that preserve the same engine/theme/document/business boundaries.
5. Review every target path and diff before writing. Never connect, compile, commit, or push implicitly.
6. Configure the native Dynamic Content region, compile only in the authorized DEV environment, and validate the real runtime and PDFs.
7. State which optional deterministic validators were not executed; do not turn their absence into a Python requirement.

See [Agent-native workflow](skills/build-apex-brand-reports/references/agent-native-workflow.md) for the complete operational contract.

## Optional deterministic scaffolder

Always inspect a dry run first:

```bash
python skills/build-apex-brand-reports/scripts/scaffold_project.py \
  --target /path/to/project \
  --config /path/to/report-kit.yaml \
  --platform apex \
  --dry-run
```

Apply only after reviewing paths and diffs:

```bash
python skills/build-apex-brand-reports/scripts/scaffold_project.py \
  --target /path/to/project \
  --config /path/to/report-kit.yaml \
  --platform apex
```

The script never connects to a database, compiles, commits, pushes, or silently overwrites files. Use `--force` only for an explicitly reviewed initial collision. Validate the result:

```bash
python skills/build-apex-brand-reports/scripts/validate_scaffold.py /path/to/project
```

## Create the first report

The scaffold generates a project-owned function example that belongs inside the confirmed existing domain package. Replace only its synthetic composition with authorized queries, binds, metrics, labels, permission checks, and organizational scope. Do not move business SQL into the engine or theme.

Configure a thin modal page in Page Designer:

- Modal Dialog page.
- One native Dynamic Content region using the project's blank/no-chrome template.
- Mandatory short source: `return EXISTING_PACKAGE.FUNC_REPORT_HTML;`.
- No iframe, external frontend runtime, CDN, or proprietary plug-in.
- Explicit context items and `Items to Submit`.
- Server-side authorization on page, region, report function, query, scope, and downloads.
- Separate XLSX/CSV processes.

The generated blueprint records the exact application/page values and expected integration points. The scaffold does not edit APEX exports.

The local HTTP server used to inspect the synthetic example is only a repository QA harness. It is not part of the generated consumer runtime.

## Print and PDF

The visual document uses its own HTML/CSS. It supports portrait and landscape A4, repeated data-table headers, stable first/last document header and footer, atomic blocks, long tables, scoped print colors, an optional economy mode, browser Print, and Save as PDF. It does not wrap business tables in a second repeated table shell: Chromium can clip later nested fragments. Repeated document shells are therefore a documented browser-specific enhancement, not a default runtime promise; repeated column headers are the reliable tabular contract.

Save as PDF opens the browser print path; the browser or operating system controls the final destination and can override a suggested filename. A tabular PDF export is not treated as a substitute for the branded visual document.

Validation requires real PDFs, `pdfinfo`, rendering every page to PNG, and visual inspection of every image. The synthetic outputs live under `examples/synthetic-company/output/`.

## XLSX and CSV

Exports remain separate authorized server-side processes. After confirming the installed APEX version and signatures, prefer `APEX_EXEC` for the query context and `APEX_DATA_EXPORT` for XLSX/CSV. Keep query construction in the consumer package.

When XLSX or CSV is enabled, the generated toolbar submits the fixed APEX request `ABRK_EXPORT_XLSX` or `ABRK_EXPORT_CSV`. Create a server-side page process with the matching request condition and call the configured project-owned procedure there. The toolbar also dispatches a cancelable `abrkexport` event before the default `apex.submit`, allowing an established consumer download flow to take over without changing the engine.

Preserve native numbers and dates, business headings, filters, authorization, locale, and timezone. Neutralize untrusted text beginning with `=`, `+`, `-`, or `@`. Never generate XLSX from rendered HTML in the browser. Validate the real workbook's Open XML integrity, native cell types, accents, filters, formulas, and sensitive-data absence.

## Update safely

```bash
python skills/build-apex-brand-reports/scripts/scaffold_project.py \
  --target /path/to/project \
  --config /path/to/report-kit.yaml \
  --platform apex \
  --update \
  --dry-run
```

After review, rerun without `--dry-run`. The update compares current engine files with recorded checksums. It preserves theme-managed and project-owned files. Modified engine files cause a conflict; merge deliberately or use `--force` only after explicit review. Keep Git available for rollback.

## Security

- Never commit credentials, tokens, cookies, wallets, private URLs, production data, authenticated screenshots, real API responses, or unlicensed brand assets.
- Use binds and server-side authorization; hidden buttons are not authorization.
- Escape HTML and attributes, validate URL schemes and filenames, and keep CSS scoped.
- Do not compile in production without explicit authorization and project locks.
- Scan both the repository and generated scaffold:

```bash
python skills/build-apex-brand-reports/scripts/validate_sensitive_data.py .
```

Report vulnerabilities through GitHub private vulnerability reporting; see [SECURITY.md](SECURITY.md).

## Validation and tests

```bash
python -m unittest discover -s tests -v
python /path/to/skill-creator/scripts/quick_validate.py skills/build-apex-brand-reports
python skills/build-apex-brand-reports/scripts/package_skill.py --output dist/build-apex-brand-reports-0.2.1.zip
```

CI validates the skill, schemas, scripts, initial scaffold, dry-run, update preservation, conflict detection, placeholders, security scan, synthetic theme, PDFs, XLSX, examples, and deterministic package.

See the recorded [validation evidence](tests/VALIDATION.md) and the two independent [forward tests](tests/FORWARD_TESTS.md).

## Compatibility

| Surface | Status in v0.2.1 | Evidence |
|---|---|---|
| Agent-native workflow without Python | Contract confirmed | Central skill, schemas, templates, adapters, and explicit manual review path |
| Optional Python 3.10+ tooling | Confirmed by CI/local tests | Schema, scaffold, update, scan, package, and artifact tests |
| HTML/CSS/JS synthetic runtime | Confirmed in the recorded test browser | Desktop, tablet, mobile, narrow, controls, and print states |
| Browser-generated PDF | Confirmed for recorded synthetic outputs | Portrait, landscape, and long-table PDFs rendered page by page |
| XLSX artifact | Confirmed for the synthetic workbook | Open XML structure, sheet, headers, native types, accents, and injection-safe text |
| Oracle APEX 24.2 | Expected, not compiled by this repository | API pattern cross-checked; consumer must confirm signatures and compile in DEV |
| Oracle Database 26ai | Expected, not compiled by this repository | Repository-only PL/SQL templates; consumer compilation remains mandatory |
| Other APEX/Database versions | Unknown | Inspect installed APIs before use |

## Limitations

- The kit cannot grant permission to reuse a brand or asset.
- Browser print engines vary in pagination, counters, repeated fixed content, colors, and filename handling.
- The scaffold cannot infer consumer queries, packages, page items, authorization, organizational scope, or locks.
- A repository-only test cannot claim Oracle compilation or real APEX runtime behavior.
- Agents without browser, database, PDF, or spreadsheet tools must report those validations as untested.

## Prompt for first use

```text
Use $build-apex-brand-reports.

Oracle APEX project:
{{PROJECT_PATH}}

Official visual identity source:
{{URL_PDF_IMAGES_OR_DIRECTORY}}

Application and environment:
{{APPLICATION_AND_ENVIRONMENT}}

Goal:
Create an Oracle APEX report or dashboard with modal visualization,
printing, PDF, and XLSX export.

Report:
{{FUNCTIONAL_DESCRIPTION}}

Existing business package:
{{EXISTING_PACKAGE}}

Desired function:
{{RETURN_CLOB_FUNCTION}}

Filters:
{{FILTERS}}

Access policy:
{{AUTHORIZATION_AND_SCOPE}}

Features:
- full screen: {{YES_OR_NO}}
- print: {{YES_OR_NO}}
- PDF: {{YES_OR_NO}}
- XLSX: {{YES_OR_NO}}
- CSV: {{YES_OR_NO}}
- orientation: {{PORTRAIT_OR_LANDSCAPE}}
- header: {{HERO_BAND_COMPACT_TEXT_NONE}}
- footer: {{FULL_COMPACT_NONE}}

Instructions:
- read the project instructions first;
- extract the complete identity from the named source;
- do not derive the theme from existing APEX screens;
- keep engine, theme, document, and business content separate;
- do not invent objects;
- perform preflight and project locks;
- keep the modal page thin;
- apply server-side security;
- generate real PDF and XLSX files;
- validate desktop, tablet, and mobile;
- render and inspect every PDF page;
- inspect XLSX types and security;
- never version credentials, real data, or unauthorized assets;
- implement and validate the complete flow;
- preserve project conventions and publication policy.
```

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md), [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md), and [SECURITY.md](SECURITY.md). Licensed under [Apache-2.0](LICENSE).
