# Reusable APEX application layout patterns

Use these patterns for branded Oracle APEX application screens rendered by
project-owned PL/SQL `RETURN CLOB` functions. They define product behavior and
composition, not a customer's identity or business rules.

## Ownership boundary

Keep three inputs separate:

1. **Brand identity:** approved logo, colors, typography, radii, spacing, and
   asset provenance from the consumer's `brand-profile`.
2. **Experience contract:** the layout and responsive behaviors in this
   reference.
3. **Business content:** titles, metrics, actions, permissions, filters, links,
   page items, and package names owned by the consumer.

Never copy a reference application's logo, palette, CSS namespace, page IDs,
package names, labels, data, or authorization rules. A layout may be reusable
even when every visible token and every business action is different.

## Structured internal page header

Use one semantic `header` inside the Dynamic Content root. Compose it from five
stable zones:

1. **Brand surface:** a fixed-size surface containing the authorized mark.
2. **Divider:** an optional vertical separator between identity and context.
3. **Context:** eyebrow, page title, and one short summary.
4. **Primary action:** at most one business action.
5. **Utility actions:** secondary navigation, overflow, help, refresh, and
   fullscreen when those capabilities exist.

Keep this order in the DOM even when CSS changes the visual rows. The primary
action is the task the page exists to advance; utilities support the page but
must not compete with it.

### Brand surface

- Give the surface a fixed inline size and block size per responsive mode.
- Render the image with `object-fit: contain`, centered, and with internal
  padding.
- Constrain both wide and tall marks so customer uploads cannot change header
  height or push actions.
- Preserve alternative text and a neutral fallback when the asset is missing
  or invalid.
- Resolve the asset with the consumer's authorized server-side rule. Do not
  expose private storage details in the CLOB.
- Use the tenant mark only when the page represents that tenant. Use the
  product/help-provider mark for product-owned help and support experiences.

### Context

- Keep the eyebrow short and categorical.
- Let the title carry the page meaning in business language.
- Limit the summary to one useful sentence.
- Avoid a decorative dash before the eyebrow when the brand surface and divider
  already establish hierarchy.
- Allow the title to wrap naturally without colliding with action zones.

### Action behavior

On wide screens, keep the primary action and utilities on the header row.
When the row no longer fits:

1. collapse utility text labels to icons while preserving accessible names and
   tooltips;
2. keep the utilities together after the context;
3. move the primary action to a dedicated row below the other zones;
4. make that primary action full width.

On narrow phones, stack brand/context first, utilities next, and the full-width
primary action last. Do not squeeze the primary action between utility icons,
wrap each button label independently, or let the toolbar overflow
horizontally.

Use server-side authorization for every action. Hidden CSS is not
authorization. Emit only the actions that the current user may execute.

Use stable capability hooks such as `data-layout-action="primary"`,
`data-layout-action="refresh"`, and `data-layout-action="fullscreen"`. Scope
refresh to the owning APEX region and fullscreen to the nearest layout root.
Bind behavior idempotently on initial load and `apexafterrefresh`. Listen for
`fullscreenchange` so icon, label, and accessible name remain correct.

### Breadcrumb decision

An internal header may replace the native breadcrumb title and breadcrumb
actions only when all are true:

- the application shell still provides orientation and navigation;
- the internal header owns page identity;
- every authorized breadcrumb action has an equivalent internal action;
- narrow-screen behavior is tested.

Do not render the same title or action in both locations.

## Compact header variant

Use a compact variant for dense dashboards or dialogs without a primary
business action. Keep brand, divider, context, and utilities on one line when
possible. Utility labels may collapse to icons before the context wraps.

Compact does not mean fragile: retain the fixed brand surface, accessible
actions, safe title wrapping, and the same capability hooks.

## Immersive Home or landing hero

The first authenticated Home view may use a more editorial hero than an
operational page. It should answer “where am I?”, “what matters now?”, and
“what should I do next?” in one first read.

Compose it with:

- a short eyebrow;
- a large, concise headline with at most one emphasized phrase;
- one short orientation sentence;
- a fixed brand surface;
- an adjacent attention panel with greeting/context and a small set of
  actionable indicators.

The attention panel is one subordinate surface, not a loose mosaic of cards.
Its indicators must have labels, values, destinations, and contextual
explanations where a term is not self-evident.

At smaller widths, stack the narrative, brand surface, and attention panel
without changing their reading order. Keep the Home hero reserved for first
read or landing experiences; routine operational screens use the structured
internal header instead.

## Simple filter surface

For a short filter set, use one rounded surface with:

1. start input;
2. end input;
3. one primary search/apply button;
4. optional selected-period context at the far side.

On wide screens, keep all four zones on one row. The context may contain a
compact label, the formatted interval, and one short explanation.

The selected-period context is progressive enhancement. Hide it before it
would wrap below the controls. Never move it to a second row on tablet or
mobile.

When the controls no longer fit:

- keep start and end side by side while each remains usable;
- move the search button to a full-width row beneath them;
- stack start, end, and search on very narrow screens;
- omit the selected-period context.

Keep labels visible, calendar triggers aligned, touch targets usable, dates
localized, and the submit/refresh contract explicit. Do not create horizontal
scroll, rely on placeholder-only labels, or duplicate the period summary below
the filter.

Use this pattern only for a small filter set. For many filters, choose an
explicit expanded-filter or Smart Filters contract rather than forcing every
control into this surface.

## Package-rendered help canvas

Render contextual help as one cohesive canvas inside the native APEX drawer,
dialog, or page host. Let the APEX host own close behavior, focus trapping, and
footer actions. Let the project-owned help function own the inner header and
content.

### Help header

Use a compact branded hero with:

- a short help eyebrow;
- a task-oriented title;
- one concise lead;
- the product/help-provider logo in a fixed surface at the far side.

Use a small brand-token accent only when it belongs to the consumer theme.
Decorative topic chips are not part of the default help header. Put topics,
steps, or states in the content hierarchy where they provide real guidance.

### Help content

Organize the canvas as a continuous reading path:

1. the decision or first choice;
2. ordered steps or checks;
3. practical signals, warnings, or examples;
4. the expected outcome.

Use larger grouped surfaces, restrained internal dividers, semantic accents,
and compact cards only where they aid scanning. Avoid a collection of unrelated
equal-weight cards.

Stack split sections on narrow screens. Keep type readable, preserve focus
order, avoid nested scroll areas, and verify the last content remains reachable
above the native host footer.

For a full-page help hub, place its authorized navigation actions in the same
structured header contract. Collapse secondary actions to icons and move the
primary action to a full-width lower row when space is constrained. Do not
duplicate those actions in a breadcrumb.

## Implementation contract

- Scope CSS and JavaScript to one stable root.
- Use semantic `header`, `main`, `section`, and navigation/action elements.
- Escape dynamic text and attributes; validate URLs and asset sources.
- Keep business queries, authorization, and page-item contracts in the
  consumer.
- Prefer a small project-owned renderer/helper for repeated header, toolbar,
  filter, and help anatomy. A helper may standardize markup and behavior, but it
  must not absorb domain queries or authorization.
- Make optional zones truly optional. Missing logo, primary action, help,
  refresh, fullscreen, or period context must not leave empty gaps or broken
  JavaScript.
- Keep generated class names neutral and consumer-scoped. Do not publish a
  customer's namespace as the shared contract.

## Responsive validation matrix

Test at the consumer's wide, medium, tablet, mobile, and narrow breakpoints.
Use actual content, then repeat with:

- wide, square, tall, missing, and invalid logos;
- a long translated title and summary;
- primary action present, absent, allowed, and denied;
- utility labels visible and collapsed;
- one utility missing from the middle of the toolbar;
- repeated partial refresh;
- fullscreen enter and exit;
- filter context visible inline and hidden before wrap;
- help with short and long content;
- keyboard-only navigation and reduced motion.

Reject the implementation if the primary action remains squeezed among utility
icons, utility labels wrap independently, a customer logo changes header
height, filter context moves to a second row, a help hero depends on decorative
chips, business actions bypass server authorization, or identity from the
reference application leaks into the consumer.
