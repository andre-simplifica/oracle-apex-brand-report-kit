# Changelog

All notable changes follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## [Unreleased]

### Added

- Documented optional `$oracle-apex-echarts` interoperability without making charts, the plug-in, or its bundle a dependency of the core report contract.

## [0.1.2] - 2026-07-22

### Changed

- Localized generated runtime actions, emission metadata, safe errors, filenames, and examples for Portuguese locales while preserving the English fallback.
- Marked the document root with the configured language and localized its emission date format.
- Removed the modal blueprint assumption that every report function is argument-free; consumers must use the confirmed PL/SQL signature and binds.
- Scoped scaffold validation and sensitive-data checks to manifest-declared kit files so unrelated consumer modules cannot create false failures.
- Bumped the generated runtime to `0.1.1` and the installable skill to `0.1.2`.

## [0.1.1] - 2026-07-22

### Changed

- Reclassified Python, PyYAML, `jsonschema`, Poppler, and Git as optional reference/QA tooling rather than Oracle APEX runtime requirements.
- Added an agent-native workflow for Codex, Claude Code, and other capable agents to extract a visual identity and generate the PL/SQL runtime without Python.
- Clarified no-Python installation, validation, upgrade, and adapter guidance for PL/SQL developers.

## [0.1.0] - 2026-07-22

### Added

- Installable `build-apex-brand-reports` skill and adapters for Codex, Claude, and generic agents.
- Versioned schemas for brand, report, and installation profiles.
- Deterministic Oracle APEX scaffold with dry-run, update, conflict detection, manifests, and checksums.
- Generic PL/SQL `RETURN CLOB` runtime, scoped theme, modal-page blueprint, and server-side XLSX/CSV guidance.
- Synthetic responsive example, portrait/landscape PDFs, rendered page images, and a typed XLSX workbook.
- Automated structure, security, scaffold, schema, packaging, and artifact tests.

[Unreleased]: https://github.com/andre-simplifica/oracle-apex-brand-report-kit/compare/v0.1.2...HEAD
[0.1.2]: https://github.com/andre-simplifica/oracle-apex-brand-report-kit/releases/tag/v0.1.2
[0.1.1]: https://github.com/andre-simplifica/oracle-apex-brand-report-kit/releases/tag/v0.1.1
[0.1.0]: https://github.com/andre-simplifica/oracle-apex-brand-report-kit/releases/tag/v0.1.0
