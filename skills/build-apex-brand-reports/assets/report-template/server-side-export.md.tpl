# Server-side export process

Status: **{{EXPORT_STATUS}}**

Configured project-owned procedure: `{{EXPORT_PROCESS}}`

Use this short APEX page-process source after implementing and compiling the confirmed project-owned procedure:

```plsql
{{EXPORT_PROCESS_BLOCK}}
```

When enabled, create authorized APEX page processes for the fixed requests `ABRK_EXPORT_XLSX` and/or `ABRK_EXPORT_CSV`. The generated toolbar submits those requests through `apex.submit` and first dispatches a cancelable `abrkexport` DOM event for consumers that use an established custom download flow. When both formats are disabled, the generated document contains no export buttons and this file intentionally contains no executable process call.

The procedure must enforce the same authorization, organizational scope, filters, locale, and timezone as `{{OWNER_PACKAGE}}.{{REPORT_FUNCTION}}`. For Oracle APEX 24.2, confirm the installed signatures before using `APEX_EXEC.OPEN_QUERY_CONTEXT`, `APEX_DATA_EXPORT.EXPORT`, and `APEX_DATA_EXPORT.DOWNLOAD`. Close the `APEX_EXEC` context in success and exception paths. Preserve numbers and dates as native types, use business headings, neutralize untrusted text that begins with `=`, `+`, `-`, or `@`, and use a safe filename.

Do not copy a query into the report-kit engine. The query and process remain project-owned.
