# Print and PDF

## Visual document

Use the report's own semantic HTML and print CSS for a complete visual document. Do not substitute a tabular export when the requested output includes identity, hierarchy, cards, notes, signatures, or branded composition.

Implement `@page` for A4 portrait or landscape, explicit margins, screen-only toolbar rules, repeated table headers, non-breaking atomic blocks, predictable section breaks, safe long-row behavior, width containment, print colors, optional economy mode, and suppression of empty trailing pages. Treat browser support for counters, repeated fixed headers, and final filenames as variable.

Avoid nested repeated document header/footer groups around a long data table: Chromium can clip a later fragment. Prioritize the data table's own repeated column header and keep the document header/footer as first/last-page content. Treat any repeated document shell as a browser-specific consumer enhancement that requires its own real-PDF validation; it is not part of the safe default runtime.

The Print and Save as PDF actions may both open the browser print dialog. State clearly that the browser or operating system controls the final destination and may override the suggested document name.

## Validation

1. Generate real PDFs for portrait, landscape, and a long table through a supported browser printing path.
2. Record the browser and version.
3. Use `pdfinfo` to confirm page size and page count.
4. Render every page to PNG with `pdftoppm`.
5. Inspect every image for margins, fonts, sizes, colors, contrast, repeated headers/footers, clipped text or images, split atomic blocks, empty pages, overflow, page sequence, legibility, and visual identity.
6. Extract text only as a secondary completeness check; never treat it as layout validation.

Reject a PDF that merely exists. Fix and regenerate until every rendered page is usable.
