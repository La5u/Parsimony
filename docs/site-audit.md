# Site experience, accessibility and importer security audit

## Scope and result

Audited the current working-tree site after the existing fixes; this is not a review of a pristine release. The follow-up UI fixes touch `parsimony/site.py`, `site/template.html`, the six generated pages, relevant site tests and this note. No importer, measurement or ranking changes, and no commits.

**Result:** local custom imports passed the tested injection, validation and lifecycle checks. Keyboard sort focus is retained, Escape dismisses chart tooltips, metadata is inside the document head, all six boards have distinct titles, leaderboard navigation is labelled, and a no-JavaScript explanation links to published data. The site is not yet ready for an accessibility-conformance claim: tooltip hover/persistence, narrow scatter discoverability and assistive-technology verification remain open. Graph geometry, ranking and the owner-required offscale extrapolation/mobile scatter policy are unchanged.

## Evidence and reproducibility

Real headless Firefox **157.0.1**, cached geckodriver **0.37.1**, Selenium from the existing `/tmp/parsimony-site-browser` environment. The default Python has no Selenium. No dependencies were added to the repository.

```sh
PARSIMONY_BROWSER_TESTS=1 /tmp/parsimony-site-browser/bin/python -m unittest tests.test_site_browser -v
python -m unittest tests.test_site -q
node tests/custom_benchmark.cjs
python -m unittest tests.test_site_browser -v
```

Follow-up results: **6 real-browser tests passed** on two consecutive final runs, **21 site tests passed** (**27 total** with `tests.test_site_self_run` and `tests.test_live_publication`), all six generated-page Node sorting/interaction checks passed, and Node importer tests passed. All six browser tests correctly skip without the opt-in variable. The Escape regression settles scroll before focusing because scroll dismissal is intentional; this avoids conflating a pending focus-induced scroll with Escape behavior. `tests.test_site` also runs the Node sorting/interaction harness with its required generated-page argument.

Rebuilt all six pages offline using the commands in `HANDOFF.md`. Compared each embedded application/json payload to a saved copy of the working-tree page before this follow-up: **all six are byte-identical**, including models, tasks, ranks/metrics, external data and self-run data. No remeasurement or publication-data edits.

New browser coverage includes Enter/Space repeated sorting and Tab progression in aggregate/task views, sort focus on all six published boards, Escape dismissal without moving chart focus in scatter/bar views, suppression of pointer-move reopening until exit/blur, valid head placement and unique titles, labelled six-link navigation, and actual visible fallback paragraphs/links with Firefox scripting disabled. WebDriver's `is_displayed()` special-cases the `noscript` container as hidden even when its children render; the test checks the visible paragraph and link instead. Source parsing verifies that all title/meta/style elements are in the head and fragment output remains wrapper-free. This is targeted structure verification, not a full HTML-validator or accessibility-conformance audit.

Browser tests cover synthetic rendered fixtures and all six published pages (`index`, `verified`, `live`, `javascript`, `typescript`, `go`) loaded from local files. Headless Firefox clamps top-level windows to at least 500 CSS pixels here. Narrow tests therefore use real iframe browsing contexts and assert `innerWidth` is exactly **320 or 390**; simply requesting a 320px outer window is not valid mobile evidence. This exercises CSS layout, not mobile hardware or touch emulation.

## Security: custom JSON importer

Reviewed `site/custom-benchmark.js`, its existing Node tests, and the UI with actual file-picker uploads.

### Verified strengths

- Imports use `JSON.parse`, not evaluation, and all user-visible benchmark/unit/model strings are inserted with `textContent` into created nodes. An HTML payload containing an external image URL and an `onerror` handler remained literal text; no image, script, iframe or link was created in imported results, and no payload execution was observed.
- Model names `__proto__` and `constructor` rendered normally. Summaries use `Map`, duplicate tracking uses `Set`, and field checks use own-property checks: no object-key assignment pollution path was found in this importer.
- Strict top-level and record field allowlists; nonempty required strings; finite numeric amounts or explicit null; boolean/null correctness; negatives only for net measurements; unique model/task/attempt tuples.
- Browser checks rejected malformed JSON, unsupported fields, duplicate tuples, a nonfinite amount, string correctness, more than 10,000 records, and files over 5 MiB. Errors clear old imported results rather than leaving a stale successful display.
- The same pathname can be selected again after editing or errors. Clear removes imported output/status, and imports leave the official leaderboard unchanged.
- Source and existing Node tests cover stale completion/rejection and clearing during an outstanding read. The generation counter prevents an older read from overwriting a newer selection. These races were not reproduced through the real OS file picker.
- No importer network or persistence operations were found in source. During browser imports, instrumented page-level `fetch`, XHR, beacon and Web Storage write calls remained unused. This is not packet capture or proof about browser telemetry, extensions, every network API, or deployment behavior.
- Download uses a local JSON Blob/object URL with revocation; the Node test checks the payload and revocation. Real-browser download completion was not checked.

### Residual risks / limits

- The byte and record caps are useful but do not bound per-field length, nesting depth, model count or rendering time tightly. Parsing, validation and table creation run on the main thread. A valid near-limit file with thousands of distinct models can still cause a long pause and large DOM; no maximum-load latency/memory budget was established.
- Strings are rendered safely but can contain misleading Unicode/bidirectional controls, exceptionally long labels or deceptive benchmark names. Imported results are explicitly marked unverified, which helps; this is not content authenticity validation.
- Empty result arrays are accepted and create an empty summary table. This is not a security flaw but could benefit from an explicit empty-state message.
- This importer has no URL field. Other page-data paths assign benchmark/navigation/task/external URLs; they are trusted publication inputs, not the importer attack surface. End-to-end URL allowlisting across the generator and deployment was not audited here.
- Live hosting headers (CSP, MIME sniffing protection, referrer policy, transport security), request logs and third-party infrastructure were not inspected. Local-file tests cannot certify those controls.

## Accessibility and professional experience

### Working in this audit

- Generated documents expose `lang="en"` and viewport metadata. Main content, heading structure, explanatory caveats and unit definitions are present.
- Task search, chart/axis selects and file input have labels. Task/import messages use polite live status regions. Invalid task text preserves the previous valid selection and explains it.
- Keyboard Tab from search reaches All tasks; Enter resets the selection. Native sorting buttons expose `aria-sort` state. Existing tests verify missing-value handling and hidden self-run controls.
- Chart circles and bars are focusable with descriptive labels. Focus shows a tooltip; blur/scroll/resize dismiss it. The narrow fixture tooltip stays within the viewport. Failed attempts and self-run limitations are described rather than conveyed only by color.
- File privacy, unverified status, missing-value denominators and separation from published rankings are clearly explained.

### Concrete remaining findings

1. **Keyboard sort focus — fixed and regression-tested.** `renderBoard()` restores only the sort key whose button actually held focus, using `preventScroll`; it does not steal focus from task search or All tasks. Firefox tests cover repeated Enter/Space sorting, updated `aria-sort`, normal Tab progression, both table views, and the six published boards.
2. **Escape tooltip dismissal — fixed; other popup requirements remain open.** Escape hides and clears scatter/bar tooltips without moving focus. Pointer movement on the dismissed target does not reopen the popup until exit/blur or redraw. Existing blur/scroll/resize/redraw dismissal remains. Pointer events are still disabled on the tooltip, so hoverability, persistence and possible content obscuration need a separate WCAG 1.4.13 assessment; this fix does not establish compliance.
3. **Screen-reader chart semantics need verification (medium priority).** Scatter uses `svg role="img"` around individually focusable circles, potentially flattening descendants in some accessibility trees. Bars have useful `aria-label`s but no `aria-describedby` relationship to the tooltip. No NVDA/JAWS/VoiceOver or Firefox accessibility-tree audit was performed; DOM attributes alone do not establish that all values are announced. The table is a useful fallback, but not every selectable chart metric is present in it.
4. **Head structure, board titles and navigation — fixed; table naming remains open.** The generator now separates template metadata/style from body content before adding the standalone wrappers. Board-specific titles include benchmark and language and are HTML-escaped. Navigation uses `nav aria-label="Leaderboards"`. Source and Firefox tests verify head placement and all six distinct titles. Tables still lack captions and two leaderboard headings frame the chart/table; descriptive captions, clearer heading grouping and full HTML validation remain future work.
5. **Contrast, targets and magnification remain unverified.** Focus outlines are defined, but faded older/self-run text and tiny labels require contrast assessment. Scatter circles have a 12px diameter before responsive scaling; evaluate target-size requirements/exceptions rather than assuming a label makes tapping easy. No comprehensive color-contrast computation, 200%/400% zoom/reflow, forced-colors or reduced-motion audit was performed.
6. **No-JavaScript fallback — added and browser-tested.** A static `noscript` paragraph explains the JavaScript requirement and links to the repository benchmark directory containing cohort reports and downloadable JSON/JSONL data. It renders with scripting disabled on all six pages. This is an explanation/data-access fallback, not a server-rendered leaderboard. Runtime script failures with JavaScript enabled still need separate error recovery.

## Mobile findings

All six pages populated their official tables and bar charts at verified 320px and 390px CSS viewports. Bar containers fit horizontally, labels truncate, and numeric values remain alongside the tracks. Tables use their own horizontal scroll wrappers; this is preferable to widening the whole page, although discoverability and keyboard scrolling of those wrappers need a manual check.

The scatter view is **not fully contained**. Diagnostic measurements at `innerWidth = 320`:

| Board | Labels crossing horizontal viewport | Points crossing horizontal viewport | Root scroll width |
| --- | ---: | --- | ---: |
| index | 2 | none | 339px |
| verified | 9 | none | 349px |
| live | 1 | none | 385px |
| javascript | 3 | Gemini 3.1 Pro Preview (high) | 339px |
| typescript | 2 | none | 339px |
| go | 1 | none | 339px |

These are bounding-box measurements, not a claim that every overflowing pixel is visible. `body { overflow-x: clip; }` hides horizontal overflow rather than making out-of-viewport content reachable. In particular, the JavaScript point remains mathematically plotted to scale outside the fitted axes but is not fully visible on the narrow screen. The table and bar view provide alternative access, yet users may never discover the clipped scatter item. The owner requires true-coordinate offscale extrapolation and fixed 10 CSS-pixel label offsets. This follow-up deliberately does **not** change mobile scatter defaults, label placement, axis fitting, clipping or extrapolation. Offscale values remain disclosed in labels/tooltips and accessible through the table/bar alternatives; any further discoverability treatment needs owner review and must preserve these constraints.

At 320px the official table wrapper had 276px client width versus 824–1025px scroll width, depending on board. This is substantial horizontal travel; test on touch hardware and with keyboard/screen readers before declaring the mobile experience complete. Labels also overlap densely at small chart sizes; readability was not quantified by screenshot comparison.

## Recommended next owner tasks

1. Assess tooltip hoverability/persistence and obscuration, plus screen-reader chart semantics.
2. Manually test touch, zoom and offscale discoverability without changing the owner-required scatter positioning/extrapolation policy.
3. Run full HTML validation and consider descriptive table captions/heading grouping.
4. Run contrast/target-size checks plus a hosted security-header audit.
5. Stress-test a valid near-limit import and define an acceptable responsiveness budget; consider runtime script-error recovery.

The browser tests assert the fixed and verified behaviors; residual findings remain recorded rather than silently treated as passing accessibility assertions. No WCAG conformance or comprehensive security certification is implied.
