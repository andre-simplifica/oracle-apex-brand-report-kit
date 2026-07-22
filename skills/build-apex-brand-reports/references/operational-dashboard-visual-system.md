# Operational dashboard visual system

Use this reference for dashboards, scorecards, home pages, and compact operational summaries. It defines a brand-neutral component grammar. The consumer's approved brand profile remains the source of colors, typography, assets, radii, shadows, and voice.

## Start with two contracts

Write these contracts before changing code:

1. **Identity contract:** official brand source, tokens, assets, licenses, contrast, typography, and voice.
2. **Experience contract:** approved reference states, component anatomy, hierarchy, density, interaction, responsive behavior, and the legacy patterns that must be removed.

Do not collapse the two contracts into a mood board. A successful result should visibly belong to the consumer while behaving and composing as well as the approved experience reference.

## Compose a compact dashboard shell

A dedicated dashboard may provide its own compact internal shell when the
consumer project authorizes it. Keep that shell separate from the global APEX
navigation and from print/PDF document headers. Its header has three stable
zones:

1. **Identity:** the authorized tenant or project mark with a safe fallback;
2. **Context:** a short category, the dashboard title, and one concise sentence;
3. **Actions:** business actions followed by technical controls in one toolbar.

Keep the identity subordinate to the dashboard title and keep the toolbar on
one line while space permits. Use one project-owned gap token between the shell
and each major section instead of accumulating unrelated margins. The content
width and exact breakpoint belong to the consumer profile; do not hard-code a
reference application's dimensions into the shared system.

A dedicated dashboard may omit the page breadcrumb only when the internal
header supplies a meaningful accessible name, the surrounding application
still provides a clear way back, and the consumer's APEX conventions explicitly
allow it. The CLOB must not resize or restyle the global application header or
navigation drawer.

## Standardize the action toolbar

- Use one toolbar container and stable hooks such as
  `data-dashboard-action`, `data-dashboard-refresh`, and
  `data-dashboard-fullscreen`; a consumer may namespace those hooks.
- Put at most one visible primary business action before the technical actions.
  Move secondary business actions to an overflow menu when space is limited.
- Treat refresh and fullscreen as optional capabilities. Their absence must not
  cause a JavaScript error or leave an empty toolbar.
- Every action needs an icon, an accessible name, visible focus, an explicit
  destination or request, and server-side authorization when it changes or
  exposes business state.
- Refresh only the owning APEX region through its confirmed Static ID. Bind the
  runtime idempotently so repeated `apexafterrefresh` events do not duplicate
  handlers, observers, or requests.
- Fullscreen only the dashboard root, synchronize icon, title, and accessible
  label on `fullscreenchange`, and tolerate the browser leaving fullscreen
  outside the button.
- Hide the toolbar in print. At narrow widths, labels may collapse to icons only
  when `aria-label` and `title` remain meaningful.

## Prefer surfaces over card mosaics

Related measures should normally read as one analytical sentence:

- Use one continuous surface for a tightly related KPI group.
- Put the primary measure first and make it visually dominant.
- Place secondary measures in an integrated supporting band or row with light dividers.
- Use nested cards only when each child has an independent action, state, or comparison that justifies a separate boundary.
- Do not place every label/value pair inside its own pastel rectangle. Excessive nested boxes weaken hierarchy and consume space.

For four peer business modules, prefer a `4 -> 2 -> 1` responsive grid when the available width supports it. This avoids an orphan fourth card on wide screens. Use `3 -> 2 -> 1` only when three modules are truly primary or the fourth has a deliberately different role.

## Card anatomy

A compact operational card should normally contain:

1. **Header:** semantic icon, business title, and optional concise state.
2. **Primary line:** dominant tabular value, unit/context, and optional monetary or comparison value aligned as one row.
3. **Supporting context:** small segmentation such as lead/client, period, or source when it helps interpret the primary value.
4. **Supporting band:** two to four peer results separated by lines, not independent decorative boxes.
5. **Detail affordance:** tooltip or drill-through only when it exposes information not already readable on the surface.

Keep the complete card clickable only when the whole card has one destination. Nested interactive tooltip triggers must remain keyboard reachable and must not create invalid nested links or buttons.

## Typography and section language

- Use the consumer display family for headings and the body family for reading.
- Use tabular numerals for KPIs, money, percentages, and aligned comparisons.
- A kicker locates the section, the title names it, and the summary explains its purpose. Never repeat the same word in all three levels.
- Prefer business language such as `Priorities / Focus for today` and `Productivity / Daily overview` over duplicated labels such as `Focus / Focus for today`.
- Labels should be quiet; numbers and exceptions should carry emphasis.
- Do not use uppercase, letter spacing, and bold weight on every level. Reserve those treatments for short locating labels.

## Semantic accents

Define card-level properties from the consumer palette, for example:

```css
[data-dashboard-root] .metric-card {
  --metric-accent: var(--theme-primary);
  --metric-soft: var(--theme-soft);
}
```

Use one restrained accent per business domain and keep success, warning, and danger states semantically stable across cards. An accent may color the icon surface, a narrow edge, a small status, or a subtle radial wash. It should not recolor all text or turn a neutral zero into an alert.

Use decorative gradients only as low-contrast surface depth. Preserve text contrast and a useful monochrome/reduced-color state.

## Interaction and accessibility

- Keep hover and focus feedback between roughly 120 and 220 milliseconds.
- Prefer border, shadow, opacity, and small transforms. Do not animate layout dimensions.
- Use `:focus-visible` with a clear outline that is not clipped by the card.
- Tooltips are hidden by default, anchored to the hovered or focused trigger, stable near viewport edges, non-blocking, and readable by keyboard users.
- Respect `prefers-reduced-motion` and keep the dashboard fully usable without animation.
- Do not use color as the only signal for success, cancellation, delay, or completion.

## APEX implementation shape

- Keep a stable root selector and scope every rule below it.
- Return semantic HTML, scoped CSS, and only necessary idempotent JavaScript in the `CLOB`.
- Use CSS custom properties or semantic modifier classes for domain tones; map them to the consumer theme in the consumer package.
- Preserve `apexafterrefresh` behavior and prevent duplicate handlers or observers.
- Use content-driven height. Do not force equal heights when text can vary; align peer cards through grid stretch and internal layout instead.
- Test initial load and repeated region refresh before accepting the component.
- Scope shell, refresh, and fullscreen behavior to the dashboard root; never
  attach them to the whole APEX page by accident.

## Modernization workflow

1. Capture the current stable desktop and mobile states.
2. Inspect the real DOM and emitting PL/SQL. List which structures are semantic and which are legacy presentation artifacts.
3. Capture the approved experience reference at equivalent widths and identify reusable grammar rather than brand details.
4. Write the new section hierarchy, card anatomy, semantic tones, and breakpoints.
5. Decide explicitly whether the DOM must change. Do not rely on replacements and CSS overrides when the old grouping is the problem.
6. Implement the static hierarchy first, then hover, focus, tooltip, and refresh behavior.
7. Validate real data, all-zero data, long labels, missing optional values, empty state, and safe error state.
8. Compare desktop, tablet, mobile, and narrow screenshots. Check console health, overflow, focus, reduced motion, and repeated refresh.

## Rejection checklist

Reject the result when any of these remain:

- the new palette is applied to the old component anatomy without a hierarchy change;
- a section kicker repeats its title;
- four peer modules produce an accidental `3 + 1` layout;
- supporting measures appear as a mosaic of nested boxes without independent meaning;
- all KPIs, labels, and statuses have equal emphasis;
- colors come from the experience reference instead of the consumer identity;
- fixed heights clip text or create large empty areas;
- tooltips work only with a pointer;
- the dashboard header duplicates the breadcrumb without an explicit reason;
- the toolbar wraps into an accidental second header row or loses accessible names;
- refresh duplicates events or fullscreen captures the whole application shell;
- the dashboard breaks after an APEX region refresh.
