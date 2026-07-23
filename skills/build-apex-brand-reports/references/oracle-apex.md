# Oracle APEX integration

## Mandatory native runtime contract

The primary runtime is a native Dynamic Content region. Its source must directly `return EXISTING_PACKAGE.FUNC_REPORT_HTML;`, where the function returns a `CLOB`. Essential HTML, scoped CSS, and idempotent JavaScript travel in that CLOB. Do not substitute an iframe, external frontend server, CDN, or proprietary plug-in. Optional Static Application Files and XLSX/CSV processes may complement the report but may not be required for its core rendering.

## Preflight

Confirm the real APEX version, database version, application ID, page ID, parsing schema, existing package ownership, page-item contract, authorization scheme, locale, timezone, DEV connection, lock policy, and Page Designer/export policy. Inspect sibling components before choosing templates. Do not compile or modify APEX from the scaffold.

For an operational dashboard or visual modernization, read [operational-dashboard-visual-system.md](operational-dashboard-visual-system.md). Inspect the actual rendered DOM and the package that emits it before deciding that CSS overrides are sufficient. Preserve queries, links, authorization, and metrics, but replace legacy component anatomy when it prevents the approved hierarchy.

## PL/SQL runtime

- Keep package spec and body separate.
- Return HTML from functions as `CLOB`; do not use `HTP.P` for new report functions.
- Use temporary CLOBs and `DBMS_LOB.WRITEAPPEND` for large output. Keep VARCHAR2 chunks within PL/SQL limits.
- Escape untrusted text with `APEX_ESCAPE.HTML`, escape attributes with `APEX_ESCAPE.HTML_ATTRIBUTE`, validate URL schemes, and whitelist enum-like configuration.
- Keep CSS beneath a runtime root class and avoid global selectors.
- Express reusable card tones through scoped CSS custom properties or semantic classes. Resolve those properties from the consumer theme; never hardcode the palette of an experience-reference application.
- Bind JavaScript once per root and tolerate repeated initialization. In APEX, subscribe to the jQuery `apexafterrefresh` event with a namespace (for example, `apexafterrefresh.abrk`); use the native DOM event only as a non-APEX fallback. Reinitialize both roots contained by the refreshed region and a refreshed element that is itself a runtime root, without duplicating listeners.
- Return business-safe empty and error states. Log sanitized diagnostics through the consumer's approved mechanism; never expose raw exceptions.
- Supply `p_toolbar_html` only for trusted, project-owned custom markup. Escape every dynamic label or attribute before composing it; never pass database or page-item text through as raw HTML.

## Business function

Place the public report function in the existing package selected by the project. Let it enforce authorization and organizational scope, execute queries with binds, create semantic content blocks, and call engine open/close functions. Do not create a domain package merely because an example uses one.

## Thin modal page

Configure through Page Designer when exports are not approved for direct editing:

1. Create or reuse the confirmed modal page.
2. Add one native Dynamic Content region using the project's blank/no-chrome template.
3. Set the source to a short direct call to the confirmed `RETURN CLOB` function, for example `return EXISTING_PACKAGE.FUNC_REPORT_HTML;`.
4. Add only context items and list every required `Items to Submit` value.
5. Apply the authorization scheme to the page, region, process, download, business function, query, and organizational scope as applicable.
6. Add refresh behavior and separate XLSX/CSV server processes. Keep download branches and stop-engine behavior explicit.
7. Test the modal through its real originating flow when checksums or dialog context apply.

Document the exact page, region, type, source, template, items, Items to Submit, authorization, processes, sequence, conditions, branches, and Dynamic Actions.
