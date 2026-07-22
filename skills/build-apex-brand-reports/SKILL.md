---
name: build-apex-brand-reports
description: Build, install, update, maintain, and validate branded Oracle APEX reports and dashboards implemented as PL/SQL RETURN CLOB documents, with responsive layouts, A4 print/PDF, thin modal pages, server-side XLSX/CSV exports, optional Oracle APEX ECharts integration, and project-owned authorization. Use agent-native tools without requiring Python to extract an approved visual identity from URLs, authenticated apps, HTML, websites, PDFs, slides, images, screenshots, asset directories, or brand manuals; convert it into versioned theme/report profiles; scaffold a reusable runtime; or validate browser, print, PDF, spreadsheet, and chart output.
---

# Build APEX Brand Reports

## Establish the contract

1. Read the consuming repository's `AGENTS.md`, `CLAUDE.md`, local instructions, package conventions, APEX profile, lock policy, compilation policy, and publication rules.
2. Confirm the repository, environment, APEX version, database version, application, page, existing business package, report function, authorization scheme, locale, timezone, and enabled exports.
3. Treat inspection, planning, repository edits, database compilation, Page Designer changes, and publication as separate authorization boundaries.
4. Never invent packages, tables, columns, page items, APIs, permissions, queries, or business rules.
5. Keep the source of brand truth explicit. Do not derive a theme from legacy APEX screens when the user names an official source.
6. Separate **brand identity** from **product experience**. Colors, typography, logos, and assets come from the authorized brand source; component anatomy, density, hierarchy, and interaction grammar may come from a separately approved product reference. Record both sources and never let a legacy DOM silently dictate the new design.

Read [architecture.md](references/architecture.md) before designing or changing layer boundaries. Read [security.md](references/security.md) for every task.

## Enforce the primary runtime contract

- The mandatory target is a native Oracle APEX Dynamic Content region whose source directly calls a project-owned PL/SQL function that `RETURN`s a `CLOB`.
- The returned CLOB must contain everything essential to render and operate the report: semantic HTML, scoped CSS, and idempotent JavaScript.
- Never make the runtime depend on an iframe, external frontend server, CDN, or proprietary plug-in. Treat Static Application Files, Page Designer enhancements, and server-side XLSX/CSV processes as complementary integrations only.
- Never require Python, PyYAML, `jsonschema`, Poppler, or Git for the generated APEX runtime or for agent-led identity extraction. Treat bundled Python scripts as optional deterministic tooling only.
- Reject or redesign a scaffold that cannot render its core report when optional external CSS/JavaScript files or export processes are absent.
- When charts are explicitly requested and `$oracle-apex-echarts` is available, keep the report's essential text/table content independent from that optional chart layer. Never copy an ECharts bundle or integration runtime into this kit or a returned CLOB.

## Route the task

- For brand extraction, source navigation, asset licensing, token provenance, and responsive evidence, read [brand-extraction.md](references/brand-extraction.md).
- For operational dashboards, compact shells, action toolbars, KPI surfaces, cards, section hierarchy, responsive composition, tooltips, and visual modernization, read [operational-dashboard-visual-system.md](references/operational-dashboard-visual-system.md).
- For PL/SQL packages, `RETURN CLOB`, Dynamic Content, thin modal pages, Page Designer, partial refresh, and authorization placement, read [oracle-apex.md](references/oracle-apex.md).
- For A4 portrait/landscape, browser print, PDF generation, page breaking, and page-by-page inspection, read [print-and-pdf.md](references/print-and-pdf.md).
- For `APEX_EXEC`, `APEX_DATA_EXPORT`, XLSX/CSV typing, spreadsheet injection, and workbook inspection, read [excel-export.md](references/excel-export.md).
- For first installation, manifests, deterministic scaffolding, or release installation, read [installation-and-upgrade.md](references/installation-and-upgrade.md).
- For creating, installing, or maintaining a consumer without Python, read [agent-native-workflow.md](references/agent-native-workflow.md).
- For runtime upgrades, conflict handling, theme preservation, or maintenance, read both [architecture.md](references/architecture.md) and [installation-and-upgrade.md](references/installation-and-upgrade.md).
- For browser, responsive, print, PDF, spreadsheet, security, or forward validation, read [validation.md](references/validation.md) plus the output-specific reference.
- For an explicitly requested Apache ECharts chart, read [oracle-apex-echarts.md](references/oracle-apex-echarts.md) and use `$oracle-apex-echarts`; keep this skill responsible for the document and that skill responsible for the chart.

## Create a new implementation

1. Inspect the official identity source completely with the tools appropriate to its format. Record pages, sections, states, viewports, assets, licenses, and limitations.
2. When the user also names an approved application or dashboard as an experience reference, inspect its rendered states and real component implementation separately. Extract reusable composition and interaction rules without copying its brand, data, or business language.
3. Write the visual-system specification before implementation: identity tokens, dashboard shell, action toolbar, component anatomy, information hierarchy, responsive layout, semantic accents, focus/tooltip behavior, reduced motion, and the explicit legacy patterns that must not survive.
4. Create a consumer-owned `brand-profile` that validates against `schemas/brand-profile.schema.json`. Preserve provenance for every important token and asset decision.
5. Create a `report-profile` that validates against `schemas/report-profile.schema.json`. Set package names only after confirming they exist or are explicitly authorized.
6. Review both profiles against the versioned schemas. If the optional Python tooling is available, add deterministic validation and a write-free scaffold preview:

   ```bash
   python skills/build-apex-brand-reports/scripts/validate_theme.py brand-profile.json
   python skills/build-apex-brand-reports/scripts/scaffold_project.py \
     --target /path/to/project --config report-kit.yaml --platform apex --dry-run
   ```

7. With or without the scripts, review the complete target file list and diffs before writing. Apply only when the target and ownership are correct.
8. Keep engine, theme, document composition, and business content in separate files and package responsibilities.
9. Implement the public report function in the confirmed consumer-owned domain package. Keep queries, filters, metrics, organizational scope, and permission checks there.
10. If a chart was explicitly requested, let the same domain package produce its authorized ChartSpec and embed `PK_APEX_ECHARTS` output in the report CLOB. Require one approved `RUNTIME_ONLY` loader and an essential textual or tabular fallback; do not emit `<script src>` or bundle bytes.
11. Configure the mandatory native Dynamic Content region through Page Designer. A thin modal page is the default host unless the project explicitly authorizes another native APEX page route.
12. Implement XLSX/CSV as separate server-side processes only after confirming the real APEX API version and query types.
13. Compile or publish only when explicitly authorized by the request and local policy. Acquire and release project locks when required.

## Install

Read [installation-and-upgrade.md](references/installation-and-upgrade.md). Prefer a tagged release or verified commit. Do not modify global agent configuration automatically. A capable agent may install and render the templates without Python. When using the optional scaffolder, run `--dry-run` before the first write. In every path, inspect managed files before compilation.

## Update

Prefer the optional scaffolder with `--update --dry-run` for deterministic upgrades. Without Python, compare the tagged engine templates, installed manifest, and consumer files directly before editing. Update only engine-managed files by default. Preserve theme-managed and project-owned files. Stop on checksum conflicts; never overwrite them silently. Use `--force` only after an explicit review and retain rollback evidence.

## Maintain

Change the central runtime only for behavior reusable across consumers. Change a consumer theme only for that consumer's visual identity. Change document composition for layout requirements. Keep business queries and authorization in the consumer package. Backport community improvements through the central repository rather than copying private business code upstream.

## Validate

1. Run the official skill validator and repository tests when their tooling is available; otherwise perform the equivalent contract review and report the omitted automation.
2. Validate the scaffold, schemas, placeholders, managed-file checksums, sensitive-data scan, and package artifact with the strongest available tools.
3. Exercise initial creation, dry-run, overwrite protection, force, update, theme/business preservation, and conflict detection.
4. Inspect desktop, tablet, mobile, narrow layout, keyboard focus, partial refresh, and reduced motion. For dashboards, also verify the identity/context/actions shell, toolbar authorization, region-scoped refresh, root-scoped fullscreen, one spacing rhythm, related KPIs as one hierarchy, no orphan fourth card at wide widths, and non-repeating kicker/title/summary lines.
5. Produce real portrait, landscape, and long-table PDFs; render every page to images and inspect every image.
6. Produce a real XLSX; inspect sheet name, headers, rows, columns, native numbers, native dates, accents, formulas, filters, and unsafe leading characters.
7. Test an empty state and a safe error state. Never expose raw Oracle/APEX errors to end users.
8. When ECharts is used, test the report with the chart available and unavailable; essential narrative, KPIs, tables, authorization, print, and export must remain functional.
9. Report what was executed, what remained repository-only, the exact compatibility evidence, and every untested environment.

## Preserve security boundaries

- Use binds and server-side authorization. Never rely on hidden buttons.
- Escape text and attributes, validate URLs and filenames, scope CSS, and keep JavaScript idempotent.
- Never put credentials, tokens, cookies, private URLs, customer data, real usernames, private assets, or raw API responses in source, CLOBs, HTML, JavaScript, logs, examples, screenshots, PDFs, or spreadsheets.
- Never connect, compile, commit, push, or overwrite from the scaffolder.
- Keep the public repository synthetic and license-compatible. Store a real company's extracted theme only in its authorized consumer project.
