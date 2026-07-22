# Server-side XLSX and CSV

## Preflight

Confirm the exact APEX version and the installed signatures of `APEX_EXEC` and `APEX_DATA_EXPORT`. Confirm the authorized query, binds, column types, labels, filters, permissions, locale, timezone, filename, empty-data behavior, and spreadsheet-injection policy. Do not assume an API exists because it is documented for another version.

## Implementation pattern

When supported, open a local query context with `APEX_EXEC`, export with `APEX_DATA_EXPORT`, close the context in success and exception paths, then call `APEX_DATA_EXPORT.DOWNLOAD` from a separate authorized APEX page process. Keep the query and bind construction in the consumer's business layer.

Preserve numbers as numbers and dates as dates. Use business headings. Omit internal IDs unless requested. Apply the same filters, authorization, and organizational scope as the visible report. Sanitize the filename. For untrusted values intended as text, neutralize leading `=`, `+`, `-`, or `@` before export. Do not generate XLSX client-side from rendered HTML.

## Validation

Open or parse the real workbook. Verify ZIP/Open XML integrity, sheet name, headers, rows, columns, filters, native types, dates, numbers, accents, formulas, and absence of repair warnings. Inspect all cells for dangerous formula prefixes and sensitive data. Verify CSV encoding, delimiters, quoting, line endings, and injection handling separately.
