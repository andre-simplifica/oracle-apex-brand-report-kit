# Validation evidence for v0.3.0

Version 0.3.0 adds brand-neutral application-layout contracts for structured
headers, responsive actions, simple filters, Home heroes, and package-rendered
help. It does not change the recorded synthetic runtime, PDF, or XLSX artifacts
below. Repository tests verify that the guidance is packaged and routed while
consumer-specific identity, packages, pages, permissions, and business actions
remain local; consumer-side APEX runtime validation remains mandatory.

## Automated

```text
python -m unittest discover -s tests -v
31 tests passed

python skill-creator/scripts/quick_validate.py skills/build-apex-brand-reports
Skill is valid!

python skills/build-apex-brand-reports/scripts/validate_sensitive_data.py .
OK: no sensitive-data patterns found
```

The suite covers schemas, focus and text contrast, CSS-token injection, deterministic packaging, packaged optional dependencies, the no-Python runtime contract, dry-run, initial creation, overwrite protection, force, repeat creation rejection, update preservation, engine conflict detection, manifests, unresolved placeholders, native Dynamic Content architecture, PDFs, XLSX types, and sensitive-data patterns.

## Neutral application-layout contract

The packaged skill contains 37 files, including
`references/application-layout-patterns.md`. The repository test asserts that
this reference is routed from `SKILL.md`, packaged, and free of the originating
consumer's package names, page IDs, CSS namespace, and identity.

A fresh synthetic consumer dry-run planned 12 files without writing. The same
configuration then produced and validated all 12 files successfully. The
deterministic `build-apex-brand-reports-0.3.0.zip` generated during this
validation has SHA-256
`a7c9f9fdce8359ea6695259ac4c0d1512bfefb7b5311325ec4d90b4d62ff846d`.

## Browser

The synthetic HTML was inspected in Chromium 150 at 1440×900, 768×900, 390×844, and 320×700 CSS pixels. Tested states included hero, band, compact, text, and no header; full screen present and absent; portrait and landscape; short and long tables; keyboard focus; hover/disabled styling; reduced-motion CSS; and a contained horizontally scrollable mobile table. No page-level horizontal overflow or tested console error remained.

## PDF

| Artifact | Pages | A4 points | Result |
|---|---:|---|---|
| `acme-harbor-portrait.pdf` | 2 | 594.96 × 841.92 | Every rendered page inspected |
| `acme-harbor-landscape.pdf` | 2 | 841.92 × 594.96 | Every rendered page inspected |
| `acme-harbor-long-table.pdf` | 4 | 594.96 × 841.92 | Every rendered page inspected |

All three PDFs are tagged and contain no embedded JavaScript. Poppler rendered all eight pages to PNG. Inspection covered margins, clipping, overflow, table headers, row integrity, empty pages, document header/footer, colors, and readability. The central runtime deliberately avoids nesting business tables in an outer repeated table shell because Chromium can clip later fragments; repeated data-table headers are the reliable contract.

## XLSX

`acme-harbor-operations.xlsx` is a real Open XML workbook with one `Operations` sheet, business headings, a native date, native numbers, accents, an autofilter, and the unsafe-looking value `=2+3` stored as text rather than a formula. The workbook opened without repair and its rendered sheet image was visually inspected. Its SHA-256 is `3d9cc48a0c8abaaaed5996042da326fde0262383fd5f78acdbc43992f1e9ac36`.

## Compatibility evidence

The agent-native contract does not require Python for extraction or APEX runtime. Optional Python scripts, the static browser example, browser PDFs, and the synthetic XLSX are confirmed by the evidence above. Oracle APEX 24.2 and Oracle Database 26ai remain `expected-not-tested`: templates were reviewed statically, but consumer-side DEV compilation and authenticated runtime validation are required before deployment.
