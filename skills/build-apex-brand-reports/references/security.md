# Security

- Never version credentials, tokens, cookies, wallets, private keys, session values, private URLs, real API responses, production data, customer data, real usernames, or internal identifiers.
- Never put a secret in a CLOB, HTML, JavaScript, browser storage, PDF, XLSX, CSV, screenshot, log, issue, or test fixture.
- Apply server-side authorization to pages, regions, processes, downloads, package functions, queries, and organizational scope. Hidden controls are not authorization.
- Use binds. Avoid dynamic SQL. When unavoidable, validate identifiers with `DBMS_ASSERT`, keep a fixed query shape, and never concatenate untrusted predicates.
- Escape text and attributes, validate URL schemes, constrain filenames, scope CSS, and avoid unsafe HTML passthrough.
- Neutralize spreadsheet-injection prefixes for untrusted text while retaining genuine numeric and date types.
- Respect project locks and publication rules. Do not compile in production without explicit authorization.
- Preserve unrelated local changes and never let an update silently overwrite consumer customizations.
- Confirm licenses before publishing assets or code. Do not copy proprietary skill content into the project.

Run `validate_sensitive_data.py` at the repository root and again against every generated consumer scaffold. Treat matches as findings to review, not permission to auto-redact source.
