# Brand extraction

## Separate identity from experience

Treat identity and product experience as different inputs:

- The **identity source** owns logos, licensed assets, typography, color, gradients, texture, radius, shadow, and voice.
- An approved **experience reference** may contribute component anatomy, information hierarchy, density, responsive composition, interaction feedback, and chart or tooltip grammar.
- A legacy APEX page is implementation evidence, not automatically the source of either system.

When both sources exist, inspect and cite them separately. Apply the experience grammar through the consumer's identity tokens. Do not copy the reference application's logo, palette, names, data, distinctive copy, or business rules. If the current markup encodes a weaker layout, explicitly decide whether the DOM must change; a CSS-only reskin is not modernization when the hierarchy or grouping remains wrong.

## Inspect the source

1. Identify the official source and authorization to access and reuse it.
2. Open every accessible page, slide, menu, section, component state, and document page. Inspect desktop, tablet, mobile, and narrow widths.
3. Capture evidence for typography, spacing, palette, backgrounds, gradients, textures, borders, radii, shadows, icon language, cards, indicators, tables, buttons, headers, hero, bands, footers, density, motion, and print behavior. Label each observation as identity, experience grammar, business-specific content, or unresolved inference.
4. Inspect original CSS, SVG, images, fonts, and asset metadata when authorized. Prefer original assets over approximation. Never redraw an existing logo by eye.
5. If the source behaves like a presentation, extract its visual language without importing autoplay, camera effects, timelines, or decorative operational-screen animation unless requested.

## Record provenance

For each important token or asset, record the exact source location, extraction date, license or authorization basis, and decision. Record inferred tokens as inferences. Record experience-grammar decisions separately from brand tokens, including the source component/state and how it was adapted to the consumer identity. List unresolved conflicts and source limitations.

## License assets

- Confirm font, icon, image, logo, and texture rights before copying.
- Use system fallbacks when a font cannot be redistributed.
- Keep real company assets in the authorized consumer project, never in this public skill repository.
- Do not store authenticated screenshots, cookies, session values, private URLs, or embedded credentials.

## Validate the profile

Create a `brand-profile` with schema version `1.0`. Validate it with `validate_theme.py`. Check WCAG contrast, focus visibility, keyboard affordances, disabled states, readable print colors, and `prefers-reduced-motion`. Do not mix Universal Theme or legacy styles into the extracted identity without an explicit decision recorded in provenance.
