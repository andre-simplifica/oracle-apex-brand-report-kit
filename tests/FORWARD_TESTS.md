# Forward-test record for v0.1.0

Two independent clean-context evaluations exercised the packaged skill without modifying the repository, a database, or an APEX application.

## HTML/URL source

The evaluator started from the synthetic local HTML reference and original SVG, navigated desktop, tablet, mobile, narrow, and alternate feature states, derived fresh brand/report profiles, ran a write-free scaffold dry-run, created a temporary consumer, and validated the result. It also tested an all-enabled and an all-disabled feature configuration, the native Dynamic Content `RETURN CLOB` contract, export request hooks, focus contrast, sensitive-data scanning, and the ZIP-installed skill.

The first pass identified inert configuration fields, incomplete brand-token mapping, weak focus contrast, missing XLSX/CSV actions, an invalid disabled-export example, incomplete skill-local dependency declaration, and a print-shell conflict. Those defects were fixed and covered by regression tests. The final pass confirmed 22/22 repository tests, official skill validation, a 12-file dry-run with no writes, a valid 12-file scaffold, contained table overflow at 390 and 320 CSS pixels, zero browser console errors in the tested state, operational feature toggles, distinct page/soft-background mapping, semantic `header/main/footer` order in the opt-in repeat demo, and no iframe or external runtime dependency.

## PDF/image source

The second evaluator started only from the synthetic portrait PDF and its rendered pages. It inspected both source pages, derived a fresh visual profile with documented inferences, validated enabled and disabled configurations, exercised dry-run and actual scaffolds, inspected generated tokens and runtime source, and checked the native APEX contract. It independently rendered and inspected the portrait, landscape, and four-page long-table outputs.

The final pass confirmed official skill validation, 22/22 repository tests, sensitive-data scanning, the 12-file no-write dry-run, valid temporary scaffolds, mapped visual tokens, 3:1-or-better focus contrast, enabled and disabled export semantics, pinned skill-local dependencies, intact long-table rows and repeated column headers, and no blank trailing PDF page.

## Deliberate limits

- No Oracle package was compiled and no `USER_ERRORS` evidence is claimed.
- No authenticated APEX Page Designer or application runtime was changed or tested.
- Server-side XLSX/CSV templates remain guidance and integration hooks until a consumer confirms its installed APEX APIs, query types, authorization, locale, and timezone.
- Browser PDF pagination and the final download filename remain browser/operating-system behaviors.
