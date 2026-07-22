# Architecture

## Four layers

1. **Technical engine** owns CLOB construction, semantic document HTML, scoped CSS hooks, A4 rules, page breaks, toolbar behavior, browser print/PDF actions, full screen, accessibility, responsive behavior, idempotent JavaScript, APEX partial-refresh support, safe filenames, emission metadata, and export-process integration points. It must not know a brand, logo, table, column, query, metric, application ID, page ID, real user, or project authorization scheme.
2. **Visual theme** owns logos, licensed assets, typography, primitive and semantic colors, surfaces, gradients, textures, spacing, borders, radii, shadows, icons, cards, indicators, tables, buttons, headers, hero, brand band, footer, density, breakpoints, responsive rules, print tokens, focus states, and reduced motion. It must not query business data.
3. **Document structure** composes optional header, hero, context, applied filters, summaries, indicators, cards, charts, tables, notes, alerts, signatures, footer, no-data state, and safe error state. Reorder or remove blocks without changing the engine.
4. **Business content** owns queries, binds, filters, metrics, labels, scope, permissions, business rules, and the public report function. Keep it in the consumer's confirmed domain package.

## Dependency direction

Business content may call theme and engine APIs. Document composition may call theme and engine APIs. The theme may use stable engine hooks but never business APIs. The engine must depend on neither theme nor business code. Avoid circular package dependencies.

The render path terminates in a native APEX Dynamic Content region calling the consumer's `RETURN CLOB` function. The CLOB contains the essential HTML/CSS/JavaScript runtime. Iframes, external frontend servers, CDNs, and proprietary plug-ins are outside the core dependency graph and must never be required for rendering.

## File ownership

- Mark runtime files as `engine-managed` in the installation manifest.
- Mark generated theme files as `theme-managed`; never update them during a runtime-only upgrade.
- Mark business snippets, configurations, queries, and APEX instructions as `project-owned`.
- Store a SHA-256 checksum for each managed file. Treat a changed checksum as a conflict, not permission to overwrite.

## Versioning

Version the skill, runtime, schemas, and consumer theme separately with semantic versions. A consumer manifest records all four. A runtime update must show the version transition and exact diff before writing.
