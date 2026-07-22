# Oracle APEX modal page {{MODAL_PAGE_ID}}

## Mandatory runtime contract

- Use a native Dynamic Content region whose source directly calls a PL/SQL `RETURN CLOB` function.
- Keep essential HTML, scoped CSS, and idempotent JavaScript in the returned CLOB.
- Do not depend on an iframe, external frontend server, CDN, or proprietary plug-in.
- Treat Static Application Files and separate XLSX/CSV processes as optional integrations only.

- Application: `{{APPLICATION_ID}}`
- Page mode: Modal Dialog
- Authorization scheme: `{{AUTHORIZATION_SCHEME}}`
- Region type: Dynamic Content
- Region template: use the consuming project's blank/no-chrome template
- Region source: `return {{OWNER_PACKAGE}}.{{REPORT_FUNCTION}};`
- Items to Submit: `{{ITEMS_TO_SUBMIT}}`
- Default orientation: `{{ORIENTATION}}`
- Locale/timezone: `{{LOCALE}}` / `{{TIMEZONE}}`

Apply server-side authorization to the page, region, report function, query, organizational scope, and every download process. Configure refresh only for the report region and submit every context item it reads. Keep XLSX/CSV as separate Before Header or Ajax/download processes according to the project's established pattern. Invoke the modal through its real source page when dialog checksums or session context apply.

Do not place report HTML, CSS, JavaScript, queries, or business rules directly on the page. Do not edit a versioned APEX export unless the consuming project explicitly permits that route.
