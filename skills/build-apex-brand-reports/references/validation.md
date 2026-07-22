# Validation

## Static and scaffold checks

- Validate skill structure and frontmatter with the official validator.
- Validate all schemas and example profiles.
- Run unit tests for create, dry-run, required values, schema failures, overwrite protection, force, update, theme/business preservation, conflicts, manifest, security scan, packaging, and synthetic example.
- Scan for unresolved placeholders, credentials, private URLs, production-like data, and unexpected files.
- Package and install the skill into a temporary custom directory; validate the installed copy.

## Browser matrix

Test the flow `document loads -> toolbar action responds -> document remains readable` at desktop, tablet, mobile, and narrow widths. Verify page identity, meaningful DOM, no framework/error overlay, console health, keyboard focus, hover, disabled state, overflow, clipping, alignment, tables, cards, indicators, every header variant, footer, full-screen enabled/disabled, refresh idempotency, and reduced motion.

## Print, PDF, and spreadsheet

Follow [print-and-pdf.md](print-and-pdf.md) and [excel-export.md](excel-export.md). Generate real files. Inspect every PDF page image and all workbook sheets. Test portrait, landscape, long table, accents, native types, unsafe strings, empty data, and safe errors.

## Forward tests

Use two clean agent contexts: one with a local URL source and one with PDF or image sources. Provide the skill path and task only, not expected conclusions. Verify that each agent finds the routed references, builds valid profiles, generates a dry-run scaffold, preserves all four layers, toggles features, and proposes real PDF/XLSX validation without leaking private data. Remove test artifacts between runs.

## Evidence

Record exact commands, versions, file counts, page counts, viewports, and limitations. Never claim compilation, browser coverage, PDF inspection, spreadsheet opening, or compatibility that was not executed.
