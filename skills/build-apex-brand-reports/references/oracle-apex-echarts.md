# Optional Oracle APEX ECharts integration

Use this integration only when the task explicitly requests a chart and the
consumer has installed or approved
[`$oracle-apex-echarts`](https://github.com/andre-simplifica/oracle-apex-echarts).
Pin and verify release
[`v1.0.1`](https://github.com/andre-simplifica/oracle-apex-echarts/releases/tag/v1.0.1)
or a later reviewed compatibility row. The Brand Report Kit remains fully
usable without ECharts.

## Preserve ownership

| Owner | Responsibility |
| --- | --- |
| Brand Report Kit | Document, header, context, filters, KPIs, cards, tables, notes, print/PDF, XLSX/CSV, and CLOB composition |
| Oracle APEX ECharts | ChartSpec, safe serialization, chart rendering, ECharts lifecycle, accessibility, scoped chart CSS, and the offline bundle |
| Consumer domain package | SQL, binds, metrics, filters, authorization, organizational scope, and the data represented by both report and chart |
| Project profile | Locale, timezone, visual tokens, chart preferences, download policy, responsive defaults, and limits |

Do not copy `echarts-*.min.js`, the Oracle APEX ECharts runtime, its plug-in
export, or its skill into this repository. Do not place bundle bytes, a CDN,
`<script src>`, arbitrary callbacks, or a second chart serializer inside the
report CLOB.

## Compose the report

1. Confirm that `PK_APEX_ECHARTS`, plug-in `COM.SIMPLIFICA.APEX.ECHARTS`,
   runtime, ChartSpec, and project profile match one row in the ECharts
   compatibility matrix. Inspection, installation, compilation, import, page
   changes, and publication remain separate authorization boundaries.
2. Keep the existing project-owned report function responsible for server-side
   authorization, SQL, binds, metrics, filters, and document composition.
3. Have that domain package build the authorized ChartSpec and call
   `PK_APEX_ECHARTS.FUNC_CHART_INLINE` or `PK_APEX_ECHARTS.FUNC_CHART_AJAX`.
   Incorporate only the returned chart markup inside the Dynamic Content CLOB.
4. Load ECharts assets exactly once through an approved plug-in region in
   `RUNTIME_ONLY` mode. Never generate a manual `<script src>` tag.
5. Use `.apex-brand-report-kit/brand-profile.json` as the visual source through
   `.oracle-apex-echarts/profile.yaml`; the compiled chart profile contains
   only mapped colors, typography, surfaces, text, border, breakpoints, reduced
   motion, and contrast tokens, never a logo or full document identity.
6. Keep essential values in semantic text, KPI, or table output. Provide an
   accessible textual or tabular fallback when the chart is essential. A chart
   error must not suppress the report or expose an Oracle/APEX error.

Use a standalone ECharts plug-in region instead only when the chart genuinely
has an independent SQL, authorization, refresh, loading, error, drill-down, or
volume lifecycle outside the report document. Inside a Brand Report Kit
document, prefer the `PK_APEX_ECHARTS` Dynamic Content composition above.

## Validate both layers

- Validate the Brand Report Kit document at desktop, tablet, narrow mobile,
  keyboard, reduced motion, print/PDF, empty, and safe-error states.
- Validate the chart's ChartSpec, profile precedence, payload/point limits,
  refresh/disposal, stale AJAX protection, accessibility, and asset deduplication
  with `$oracle-apex-echarts`.
- Disable or remove the optional chart loader and confirm that narrative, KPIs,
  tables, authorization, print, and exports remain usable.
- Confirm that neither the CLOB nor network trace contains a duplicated ECharts
  bundle or remote runtime dependency.
