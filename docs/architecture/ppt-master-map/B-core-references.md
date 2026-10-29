# B — ppt-master v6.7.2 core references: capability map (authoring roles)

Root P = `C:/Users/fanrh/.claude/plugins/cache/ppt-master/ppt-master/cc8b722a24e9-32c1cf49/ppt-master/references/`.
Cites are `file:line` relative to P. Read-only; nothing modified. "Ref" = Reference (non-binding sketch); "HR" = Hard rule.

---

## 1. Inventory (every file read in full)

| File | Lines | One-line role |
|---|---:|---|
| strategist.md | 282 | Strategist role: 2-stage confirmation, 3 directions, design_spec/spec_lock authoring, Gates 1–2 |
| strategist-template.md | 79 | Applying an installed Brand/Style/Layout/Deck; reuse scope/adherence; structured lock rows |
| strategist-image.md | 45 | Rendering candidates, §VIII image rows, illustration sheets, lettering, crop policy |
| plan-core.md | 199 | Shared planning craft (Default+Quick): contract, reading mode, content, rhythm, resources, color/type/icons |
| executor-base.md | 364 | Always-loaded Executor core: routing table, device menu, layout structures, 9-step per-page chain, carrier receipt |
| executor-chart.md | 76 | Value-driven geometry, plot-area markers, verify-charts handoff |
| executor-image.md | 47 | Image status, crop policy, per-page image composition, direction generators |
| executor-notes.md | 38 | Speaker notes `notes/total.md` grounded in final SVG |
| executor-structure.md | 91 | Relationship atoms → topology grammar (order/link/parent/membership/contrast/overlap) |
| executor-structured.md | 88 | mirror/layout template reuse, Master/Layout/slot mapping |
| executor-table.md | 37 | Semantic cell-grid tables |
| executor-visualization.md | 50 | Resolving one chart/table catalog reference per page |
| executor-web-image.md | 19 | Inline attribution for web-sourced images |
| shared-standards.md | 3 | Pointer only |
| shared-standards-core.md | 259 | SVG technical contract, grouping/bounds, text frames, shared aesthetic baseline §6 |
| semantic-svg.md | 75 | `data-pptx-*` marker vocabulary |
| native-data-interface.md | 79 | Pattern fills; native chart/table replacement markers + JSON schemas |
| native-formula.md | 70 | Native Office Math from LaTeX (inline/block) |
| native-hyperlinks.md | 51 | Native click hyperlinks (external / #slide-N) |
| native-shape-authoring.md | 182 | Contour selection gate, preset/Boolean helpers, composition lenses, geometry signature, modelling techniques |
| preset-shape-vocabulary.md | 133 | All 187 DrawingML presets by Office category |
| topology-assembly.md | 56 | Generative assembly material per relationship atom |
| svg-effects.md | 610 | Gradients, alpha, shadows/glow, image overlays, lines, text treatments, transforms, freeform, radial, constructed styles, page recipes |
| svg-image-embedding.md | 53 | Image status enum, resource list format, `<image>` form |
| visual-review.md | 121 | Opt-in visual review rubric H1–H9, S1–S10, STYLE, brand escalation |
| animations.md | 261 | Transitions, object animations, Morph pairing, sounds |
| canvas-formats.md | 57 | Canvas registry, keep-clear, body-size start table |
| confirm-surface.md | 108 | Confirm UI vs chat; stage1/stage2/result JSON shapes |
| artifact-ownership.md | 92 | Who owns which artifact; regeneration commands |
| pptx-structure-interface.md | 85 | flat vs structured routing; Master/Layout/placeholder metadata |
| template-designer.md | 295 | Create Layout/Deck role: standard/fidelity/mirror, template design_spec format, placeholders |
| video-design.md | 107 | Recorded/self-running/video delivery planning |
| modes/_index.md | 58 | 5 modes + custom; decision distinctions |
| modes/briefing.md | 41 | Neutral, topic titles |
| modes/instructional.md | 45 | Teaching sequence |
| modes/narrative.md | 43 | Story arc |
| modes/pyramid.md | 58 | Conclusion-first, SCQA, assertion titles |
| modes/showcase.md | 43 | Visual-led impact |

Not in slice but referenced as owners: `templates/design_spec_reference.md`, `templates/spec_lock_reference.md` (exact §-grammar), `workflows/generate-pptx.md` (gates/commands), `visual-styles/_index.md`, `image-renderings/_index.md`, `image-layout-patterns.md`, `image-layout-spec.md`, `scripts/docs/*`.

---

## 2. Strategist

### 2.1 What it decides
- Owns: sufficiency, gap-filling, selection — roster & content, `Relationships`, resources/paths, structured-template routing, fonts, palette anchors, icon library/stroke + curated pool, crop bans, optional Chart/Table refs (strategist.md:56).
- Sketches only as Reference: macro composition, focus, continuity — "never a carrier mix, element geometry, or authoring method" (strategist.md:56; plan-core.md:87-89).
- HR "native construction stays downstream": never inventory/bind a preset, primitive, Connector, Boolean, coordinates (plan-core.md:89).
- Missing material returns upstream, never invented (strategist.md:65).

### 2.2 Confirmation stages (BLOCKING, strategist.md:21-26)
- **Stage 1** — communication contract + template choice: `primary_language` (BCP-47), audience, open-ended communication intent, audience outcome, core message, delivery context, artifact afterlife, `content_divergence`, canvas, explicit `free_design` vs `templates` + selected roots (strategist.md:25). Candidates never influence the contract recommendation (strategist.md:25,38).
- **Stage 2** — reading mode (`delivery_purpose`: text/balanced/presentation), mode + visual style, page count, color, icons, typography, image source + rendering, template application, AI-image path, generation mode, refine-spec toggle, `design_spec_depth` (brief|complete), proactive notes/animations/narration (strategist.md:26). Defaults: notes true, animations false, narration false; depth `brief` unless split/refine/preservation (strategist.md:34).
- Exactly three directions, plainly different designs; `design_directions.selected` = zero-based strongest fit (strategist.md:32,93-97). Each serializes `mode: custom`, `visual_style: custom`, `image_strategy.rendering: custom` with behavior prose unless a preset is fixed (strategist.md:95).
- Visual style carries no color; forbidden: non-catalog name as `visual_style`; generic words (flat/modern/clean/minimal) are not behavior (strategist.md:117,126).
- Continuity-aware default: plan adjacent pages as visible states of one scene when it lowers switching; recommend custom animations then (strategist.md:36).
- Confirmed-value semantic types: Literal / Semantic / Identity anchor / Reference / Permission (strategist.md:44-54). `must/only/exactly/verbatim` strengthens only the named property (strategist.md:54).
- Surface: Confirm UI page by default; chat if user asks; delegated if user delegates (confirm-surface.md:9-13). JSON shapes: stage1 (confirm-surface.md:25-41), stage2 incl. 6-role palette, typography `body_size`, three candidates (confirm-surface.md:45-104), result.json fields (confirm-surface.md:108).

### 2.3 Field-level rules
- (a) Canvas from scenario (strategist.md:69-71; canvas-formats.md:7-16).
- (b) Page count: Stage-1 narrow range → exact count after Stage 1; roster ids/count/order invariant after Gate 1 (plan-core.md:56).
- (c) Contract: six open-prose fields; blank = no constraint, never repopulated (strategist.md:79-81). Intent → outline obligations table: Inform/Explain/Persuade/Decide/Align/Teach/Report/Mobilize/Record (plan-core.md:24-36).
- Reading mode table: carrier, §IX page grammar, granularity, notes per mode (plan-core.md:44-50).
- `content_divergence`: free text; HR facts stay sourced however free (plan-core.md:58; strategist.md:85).
- (d) Mode layer (strategist.md:99-111) — user outline is a Reference unless presented as final page plan (strategist.md:107; modes/_index.md:23). Beautify = verbatim 1:1 (strategist.md:108).
- (e) Color: user colors are truth; six roles `background, secondary_bg, primary, accent, secondary_accent, body_text`; derive `secondary_text`, `divider` in §III; §V fixes five spacing anchors (strategist.md:136). Optional neutral tiers `surface, grid, scrim, overlay, block-shade` (plan-core.md:154-160). Positive/warning/negative roles owned by plan (plan-core.md:152).
- (f) Icons: A emoji / B built-in library / C custom / D none (plan-core.md:190-195); one primary library, `stroke_width` ∈ {1.5,2,3} for tabler-outline; curated pool synced via `icon_sync.py` before Executor; GATE re-pick on missing (strategist.md:144-150).
- (g) Typography: user/template authoritative; ≤4 families; one Latin + one CJK face per stack; avoid near-equivalent splits; directions include both concord and contrast pairing (plan-core.md:164-166; strategist.md:156). Role ratio table (cover 2.5–5×, chapter 2–2.5×, page title 1.5–2×, subtitle 1.2–1.5×, lead 1.1–1.4×, annotation 0.7–0.85×, footnote 0.5–0.65×) (plan-core.md:172-182). Example anchors body 24 → title 42, subtitle 32, lead 30, annotation 18, footnote 16 (plan-core.md:184). Role extension (annotation/footer/footnote/data/emphasis/quote/code/display) with one `Role rationale` line in §IV (plan-core.md:168; strategist.md:158). OPPO Sans = non-preinstalled; safe substitute Trebuchet MS/Verdana (plan-core.md:166).
- (h) Image source ids none/provided/ai/web/placeholder; credentials never decide need; visual grounding before `none`; per-image source decision (plan-core.md:113-125; strategist.md:181-189).
- Math & links: recorded in §IX only (`Mathematical content` LaTeX, `Hyperlinks` line) (plan-core.md:66; strategist.md:162-164).
- Chart/Table refs: at most one `family/key` per page, validated with `visualization_recall.py validate`; `Native-ready` map `<key>=yes|no` (plan-core.md:135-142; strategist.md:179).
- Motion: §IX `Motion suggestion` naming Morph candidates whenever a unit visibly continues (strategist.md:175).
- Notes: §X records policy or `Generation: disabled` (strategist.md:195-202).

### 2.4 design_spec.md sections (as named in slice; full grammar in templates/design_spec_reference.md)
- **§I** — communication contract (full), `content_divergence`, Reading Mode, confirmed canvas + exact count, mode/style identity, Template Application prose, AI-image path, generation mode, refine toggle, production mechanics (notes/animations/narration outcome + provenance), outline-promotion note (strategist.md:85,107,232,239,246-254; strategist-template.md:22).
- **§II** — not described in this slice.
- **§III** — color/identity anchors incl. derived `secondary_text`, `divider`; `Theme` (cross-page motif + continuity job + reuse mode) (strategist.md:136,220,248; plan-core.md:81).
- **§IV** — typography: Character/upgrade References, heading/body stacks, recurring role stacks, exact `body/title/subtitle/annotation` anchors, `Role rationale` (strategist.md:249,158).
- **§V** — five deck-wide spacing anchors: page margin, block gap, column gutter, corner radius, body leading (strategist.md:136; executor-base.md:205); page descriptions used for mirror selection (executor-structured.md:31). Reference only (executor-base.md:187).
- **§VI** — icons: synced paths + broad scenarios, base library (strategist.md:148,250).
- **§VII** — `Page | Family | Template | Usage` for chart/table refs (strategist.md:179).
- **§VIII** — image rows: filename, dimensions/ratio, purpose/type, `Image pattern`, crop policy, `Acquire Via` (ai/web/user/placeholder/slice), status, Reference, AI fields (strategist-image.md:9,35-45; svg-image-embedding.md:13-17).
- **§IX** — complete ordered page roster; per page: title, core message, **Audience move**, **Relationships** (units + source-stated relationship or `none`), content at depth, optional **Composition** Reference, `Mathematical content`, `Hyperlinks`, capability recommendations, `Visualization` (keys + `Native-ready` map), `Images`, `Fact IDs`, `Data class: scenario`, `Motion suggestion` (strategist.md:239,175,179; plan-core.md:60-66).
- **§X** — speaker notes requirements or `Generation: disabled` (strategist.md:197-202).
- Gate 1 active-decision fidelity; Gate 2 lock context fidelity (strategist.md:257-259).

### 2.5 spec_lock.md contents
- communication: `audience`, `objective`, `core_message`, `consumption_mode` (strategist.md:267).
- `mode` (+`mode_behavior`, `mode_references`); `visual_style` (+`visual_style_behavior`, `visual_style_references`) (strategist.md:111,128).
- colors (6 roles + `secondary_text`, `divider`, optional neutral tiers) (strategist.md:136).
- typography: `title_family`, `body_family`, every `<role>_family`, size anchors (strategist.md:261).
- icons: library, inventory pool, `stroke_width` (strategist.md:148).
- images: `<path> | source=<Acquire Via> | crop=<adaptive|no-crop>` (strategist-image.md:9).
- `image_rendering_behavior` / `_references` only for confirmed ai (strategist-image.md:31).
- `page_rhythm` per page: anchor|dense|breathing — mandatory (strategist.md:269).
- `page_visualizations` `P<NN>: chart|table/<key>` (strategist.md:272).
- `pptx_structure` (mode flat|structured, `template_reuse_scope`, `template_adherence`, `pptx_masters`, `pptx_layouts`, `page_pptx_layouts`, `page_layouts`) (strategist-template.md:63-77).
- `forbidden`: technical baseline + user prohibitions quoted verbatim tagged `(user)`; direction behavior never projected to prohibitions (strategist.md:265).
- Never page-local values; Executor never reverse-projects local choices (strategist.md:242,263).

### 2.6 How installed templates feed in (strategist-template.md)
- Load only after Stage 1 confirms and installs into `<project>/templates/` (strategist-template.md:7).
- Reads every installed `design_spec.<kind>.<id>.md`; `design_spec.style.*.md` = active Direction/method segment (strategist-template.md:13).
- Outputs: stage2 `template_application.value` prose; §I `Template Application`; internal lock values only (strategist-template.md:19-23).
- Scopes: `mirror` (literal), `layout` (Master/Layout reused, content open), `style` (direction only, flat pages); adherence `strict|adaptive` (strategist-template.md:25-31,49-53).
- Precedence: user/final confirmation > ...; Brand overrides Deck identity; Layout overrides Deck structure; **Style owns Direction/method only — its visual values are candidate defaults yielding to Brand/Deck identity; its preferred Mode/Visual Style seed the final locks** (strategist-template.md:57).
- All three directions obey the same template context; repeat fixed palette/fonts with `typography.fixed: true` (strategist-template.md:59; strategist.md:156).
- **Style Review Focus never activates visual-review; only explicit user request does** (strategist-template.md:59).
- Style-only or Style+Brand → `pptx_structure.mode: flat`, `template_reuse_scope: style` (strategist-template.md:67).
- Slot fit: `text_measure.py`, baseline-in-frame rule `top + 0.85×size ≤ baseline ≤ bottom − 0.35×size` (strategist-template.md:75).

### 2.7 Image planning (strategist-image.md)
- Three rendering candidates always authored (name, `rendering: custom`, visual, mood with real-world analogy, behavior) (strategist-image.md:31).
- Illustration Sheets → slice rows; illustrated icons as slices (`Crop Policy: no-crop`) (strategist-image.md:21-23).
- Decorative lettering candidates; native title kept separately (strategist-image.md:25; plan-core.md:131).
- Treatment path none/native/prepared derivative; subject crossing native content → cutout `#A2-03` (strategist-image.md:27).
- Crop policy `no-crop` for screenshots/charts/certificates/diagrams/logos; else `adaptive` (strategist-image.md:45).
- Hero pages proposed in `image_notes`, `page_role: hero_page` (strategist-image.md:33).

---

## 3. Executor toolkit

### 3.1 Module routing table (evaluated once over whole roster before P01; executor-base.md:5-21)
| Trigger | Module |
|---|---|
| `pptx_structure.mode: structured` | executor-structured.md |
| Chart/Table `family/key` ref | executor-visualization.md → branch |
| Any value-driven geometry (incl. mini charts, sparklines) | executor-chart.md |
| Any semantic cell grid | executor-table.md |
| Preset pattern fill or `<key>=yes` native object | native-data-interface.md |
| First page with topology decision `yes` | executor-structure.md + topology-assembly.md |
| Contour beyond rect/roundRect/circle/ellipse/line, or Boolean/freeform | native-shape-authoring.md (read completely) |
| Visual job beyond everyday block (glass, constructed styles, gradient stroke, text picture fill, gauge/sunburst/arc, freeform, transforms beyond rotate, unsupported effect) | svg-effects.md |
| Any image | executor-image.md + image-layout-spec.md + image-layout-patterns.md + svg-image-embedding.md |
| Structural math notation | native-formula.md |
| Any hyperlink | native-hyperlinks.md |
| Sourced image / image_sources.json record | executor-web-image.md |
| Notes enabled, after all pages pass | executor-notes.md |
- `preset-shape-vocabulary.md` is resident with the core, read completely before first page (native-shape-authoring.md:27; executor-base.md:15,309).
- Mode/style files: preset → its one file; custom → only `*_references`; none → behavior prose only (executor-base.md:25).

### 3.2 Binding vs realization (executor-base.md:179-213)
- Binds: content & `Relationships`, roster & `page_rhythm`, resource paths, routing keys, core fonts, palette & spacing anchors, icon library/stroke, crop boundaries, `(binding)` fields (executor-base.md:181-183).
- Executor owns: carrier mix, geometry, composition, which icon (executor-base.md:183,187).
- Content vs expression: may paraphrase/condense/regroup/switch prose↔bullets; never add claims, move content across pages, drop info (executor-base.md:191-197).
- Sizes: every structural text maps to a declared role ±2 px; sparse display exception ≤2 occurrences deck-wide, 3rd → return to Strategist (executor-base.md:207-209).
- Spacing anchors deck-wide; depart only for a page job, never to fit content (executor-base.md:205).

### 3.3 Per-page decision chain (9 steps, executor-base.md:215-257)
1. Communication trace — objective, core message, §IX `Core message` + `Audience move`; else `warning: P<NN> has no communication move` (:219).
2. Reading-mode check text/balanced/presentation (:221-231).
3. **Topology decision (Mandatory)** from §IX `Relationships` only; yes → structure grammar (:233).
4. Layout rhythm anchor/dense/breathing; missing → warnings, default dense (:235-243).
5. **Carrier mix (Mandatory)** — background field, text/lettering, native geometry, prepared assets, visualizations, weights, z-order (:245).
6. **Module line (Mandatory)** `P<NN> modules: core[, structure][, native-shape][, effects][, image][, native-data][, chart|table|formula|link|web-image]` (:247).
7. Composition — style §1 `Composition geometry`; motif adoption; image composition (:249-253).
8. **Geometry move (Mandatory)** via native-shape-authoring §2.1 incl. running geometry signature (:255).
9. Coordinates/bounds — sentence first, then zone (:257).

### 3.4 Page Expression Core (executor-base.md:37-150)
- Typographic feature elements: lead-in, inline emphasis run, pull quote, kicker, hero number, takeaway line (:41).
- Inline emphasis = nested `<tspan>` in one editable frame (:43-47).
- Native contour families: snipped/one-sided rounded rects, plaque, bevel, polygons, trapezoid/parallelogram, pie/arc/donut, frames, corners, stripes, folded corners, block arrows, chevrons, flowchart, callouts, brackets/braces, stars/banners, connectors, equation shapes (:49).
- **Everyday device menu** (:51-72): gradient block/band; rounded card; icon with label (32–48 px); numbered circle/badge; color swatch; KPI card; takeaway box (tint 0.06–0.10, lead size); divider/rule (hairline or 2 px accent bar); full-bleed image + scrim; framed/shaped picture; quote block; timeline/step strip; process/decision diagram; callout/annotation; display text with gradient/glow; accent gradient rule; elevated primary object (softShadow); duotone/brand-wash image.
- **Layout structures** (:74-86): 16:9 safe area 1200×640, 40 px margins, title band ≈100, content ≈500, footer ≈40; 4:3 and A4 values. Relationship → structure: one focal claim (column 800–1000, 40–60% empty), equal comparison (1:1, quadrants ≈560×250), dominant evidence + takeaway (3:7/2:8), parallel sequence (3 cols, 30–40 gaps), core + forces (hub 200–300, 4–6 satellites), wide visual + explanation (visual ≥55%), page-field organization.
- **Page-level recipes** cover/divider/text-led/process/evidence/comparison/closing/motif (:88-99; svg-effects.md:599-608).
- Image composition families P1/P2/P3 + M1/M2/M3 + A + C (:101).
- Visual job router (:103-114).
- Everyday effects & aesthetic defaults: 60-30-10, contrast ≥4.5:1, accent on key number/word, depth through restraint (≤2–3 shadowed objects), shadow values, overlay stops, dash conventions, inline emphasis rules (:116-125); sample `<defs>` (:127-150).

### 3.5 Motion endpoints at authoring time (executor-base.md:156-167)
- Continuous actions authored as consecutive pages with compatible direct-root `<g id>`; partner id recorded via `workflow_log.py` (:160-167).

### 3.6 Native shapes (native-shape-authoring.md, preset-shape-vocabulary.md)
- HR contour before encoding; rect/roundRect/circle/ellipse are not an earlier tier (executor-base.md:309; native-shape-authoring.md:31).
- Materialization tiers: primitive → helper preset → `<line>` → connector preset → independent siblings → Boolean → freeform last (executor-base.md:311-325; native-shape-authoring.md:37-47).
- Default "exact page-fit geometry before generic neutrality": a plain primitive/uniform grid wins only after naming the strongest native alternative and why it adds nothing; "Quick speed, restrained style, readability, equal importance, precedent, and shorter syntax alone never qualify" (native-shape-authoring.md:33).
- HR style does not narrow capability (native-shape-authoring.md:35).
- Helpers: `preset_shape_svg.py render|render-batch|describe|list`, `shape_boolean_svg.py render` (union/combine/intersect/subtract/fragment) (native-shape-authoring.md:7-25).
- 5-pass selection Job → Browse → Inspect → Select → Encode (native-shape-authoring.md:55-61).
- Semantic fit, not name association (scroll ≠ playbook, flowchart only in flowcharts, chartX not chart) (native-shape-authoring.md:63; preset-shape-vocabulary.md:14-20).
- §2.1 compound page geometry passes: topology/page job → decompose → select → compose → materialize (native-shape-authoring.md:69-77).
- **Composition lenses**: page field, outline carrier (`fill="none"` frame/arc/bracket/band), nested fields, continuity, depth & contrast, deck language (native-shape-authoring.md:79-88).
- **Running geometry signature**: `page job → composition move → contour / edge language` (+ `relationship → topology`); compare with previous pages; repeat only for same job or deliberate continuity — "section, equal weight, style, and precedent are insufficient" (native-shape-authoring.md:92).
- Boolean decision gate (native-shape-authoring.md:94-105).
- Modelling techniques: alternating light/dark gradient for dimensional form; built reflection; fragment for pyramid tiers/quadrant wheels/ring segments; soft edges via alpha gradients; ground plane/staging (native-shape-authoring.md:151-182).
- Vocabulary: 187 presets in Lines, Rectangles, Basic Shapes, Block Arrows, Equation, Flowchart, Stars & Banners, Callouts, Action Buttons (preset-shape-vocabulary.md:3,28-133); `describe --frame` gives text rectangle (preset-shape-vocabulary.md:22-25).

### 3.7 Topology / structure (executor-structure.md, topology-assembly.md)
- HR no Structure catalog; compose from §IX relationships (executor-structure.md:7).
- Atoms: order, link, parent, membership, contrast, overlap with topology generators (executor-structure.md:19-26).
- Combined-atom spatial relation; orthogonal overlay (executor-structure.md:30).
- **HR no topology from balance alone** — node count never justifies equal shapes/mirroring/radial symmetry (executor-structure.md:32).
- Roles field/node/spine/edge/label/garnish; ops repeat/arrange/transform/connect/region/attach (executor-structure.md:38-54).
- Construction order spine → nodes → connectors → labels → garnish; relationship before styling (executor-structure.md:62-72).
- Validation table: coverage, reading path, roles, attachment, removal, fidelity, construction, composition (executor-structure.md:80-89).
- Assembly material: chevron stages, wrap/reverse paths, blockArc recurrence, split/merge, two-way exchange, nested bubbles, brace decomposition, lanes, opposing fields, tapered trapezoid stack (→ fragment pyramid), overlap ellipses, order×membership swimlanes, 2×2 with non-central thresholds, radial parent (topology-assembly.md:19-56). HR two-step assembly test + registration closure (topology-assembly.md:9-11).

### 3.8 Charts (executor-chart.md)
- HR data owns marks; construction order domain → frame → marks → labels → styling (executor-chart.md:19-21).
- Perceptual reading: zero baseline for magnitude bars, direct labels, shared scales, dual-axis restrictions (executor-chart.md:23).
- Ref color conventions: monochrome depth (primary full, comparison ~60% alpha), gray dashed baselines, accent only on key points, annotate inflection points, source note (executor-chart.md:25).
- Mandatory plot-area marker per verified chart object `<!-- chart-plot-area: object=<key> | x_min,y_min,x_max,y_max -->` (pie/donut/radar forms) (executor-chart.md:35-62); rg check (:66); `verify-charts` stage after all pages (:76). ChartEx types (:72).

### 3.9 Tables (executor-table.md)
- Boundary: row header × column header addresses each fact; metric-card rows are not tables (executor-table.md:13-19).
- Catalog keys record_table, metric_table, comparison_matrix, feature_matrix, rating_matrix, hierarchical_table (executor-table.md:21).
- HR grid before decoration; widths from semantic weight, not equal (executor-table.md:27).
- Ref defaults: header by weight + rule, zebra 0.05, numbers right, one highlight row accent 0.1, **horizontal rules only — avoid full grid** (executor-table.md:31).

### 3.10 Visualization reference (executor-visualization.md)
- One primary catalog SVG per page; resolve via `visualization_recall.py validate` (executor-visualization.md:23-30).
- Preserve content; adapt dimensions/styling freely; forbidden preview substitution (sample data) (executor-visualization.md:42-48).

### 3.11 Native data (native-data-interface.md)
- Pattern fills: closed enum of DrawingML presets (grids, diagonals, percent, checks, decorative) (native-data-interface.md:9-18).
- Native chart/table: SVG-first default; marker + JSON written atomically; stamp `stamp_native_fallbacks.py`; export flag `--native-charts-and-tables` is the opt-in (native-data-interface.md:22-37).
- Table schema `ppt-master.semantic-table.v2` (cells, borders, spans) (native-data-interface.md:67-71); chart types list (column…stock), fail-fast on map/heatmap/bullet/gantt (native-data-interface.md:75).

### 3.12 Formula / hyperlinks
- Formula: plain text vs inline `data-pptx-inline-formula` vs block `data-pptx-replace-with="formula"`; reserve native height; never PNG (native-formula.md:16-68).
- Hyperlinks: `<a href>` whole-object or inline; `#slide-N`; checker compares with §IX `Hyperlinks` (native-hyperlinks.md:22-51).

### 3.13 Effects (svg-effects.md; must be read completely once triggered, :11)
- §6.1 job-first selection (skeleton/diagnose → surface/select → integrate/stop) (:35-39); one dominant composition scaffold (:46-51); Visual Job Router (:62-73); Image-Treatment Implementation Map (:81-92).
- §6.2 color/alpha channels (:104-115).
- §6.3 gradients (objectBoundingBox, no gradientTransform; linear Native-normalized, radial Approximate); gradient stroke; native text picture/texture fill `data-pptx-text-image-fill` (:119-170).
- §6.4 shadows/glow: elevation table Floor/Resting/Raised/Glow (:211-216); one light source (:218-224); one weight tool per container; peer cards stay on floor (:226-237).
- §6.5 image treatments: cover/contain/stretch/fade/shaped; overlays directional scrim, bottom fade, vignette, brand wash, grid scrim, faux glass (:243-276).
- §6.6 lines: 5 dash presets, caps/joins, markers, multi-subpath grids (:282-322).
- §6.7 text treatments: underline/strike, mixed runs, super/sub, tracking, transparency, gradient fill, outline, shadow/glow, native bullets; CJK tracking ≤2% (:328-388).
- §6.8 transforms (no skew) and layering (:394-410).
- §6.9 freeform curves (last tier) (:416-447).
- §6.10 radial geometry, donuts, gauges, sunburst, diagonal arrowheads (:453-511).
- §6.11 constructed recipes: faux glass, paper cut, hand-drawn mark, ink wash, riso offset, pixel grid, **halftone** (calculated circles, sparse), faceted/folded form, gradient ribbon, line+area (:525-536).
- §6.12 unsupported → alternatives: blur, inner shadow, soft edge, reflection, mask/blend, custom tile, skew = Bake-required (:578-588).
- §6.13 page-level composition recipes (:599-608).

### 3.14 Images (executor-image.md, svg-image-embedding.md, executor-web-image.md)
- Status handling Existing/Generated/Sourced/Needs-Manual/Placeholder (executor-image.md:11-17); full enum incl. Pending/Failed/Needs-Selection (svg-image-embedding.md:21-30).
- Crop policy: `no-crop` → one complete `meet` instance, no clip/mask (executor-image.md:21).
- **Mandatory per-page image composition decision**: `role → direction generator → parent contour → slots/rhythm → crop → image-shape action → labels/overlays → depth/continuity`, compare with plain placement (executor-image.md:31).
- Preserve image job at final size (executor-image.md:35); direction generators vector/shared-baseline/curve-spine/panel/none-grid (executor-image.md:37-45).
- Web attribution per `license_tier` (executor-web-image.md:13-19).

### 3.15 Icons, fonts, grouping, text frames
- Icons: `<use data-icon="lib/name">`, always `fill="#HEX"`, stroke-width only tabler-outline; missing → back to Strategist (executor-base.md:337-348).
- Fonts: role → `title_family`/`body_family`; common stack on root `<svg>`; delivery-target faces only (executor-base.md:354-358; shared-standards-core.md:168).
- One paragraph = one `<text>` with positioned `<tspan>` (executor-base.md:199; shared-standards-core.md:178).
- Leading starts: titles 1.2–1.3×, dense body 1.4–1.5×, body 1.5–1.6×, breathing 1.6–2.0× (shared-standards-core.md:184).
- **Mandatory grouping**: each logical unit one top-level `<g id>` with `data-pptx-bounds`; page title its own group; forbidden giant group / ungrouped atoms / per-line groups / anonymous groups (shared-standards-core.md:188-228; executor-base.md:272-274).
- Width estimation via per-role chars-per-100px calibration; keep ~5% under bounds; never trim wording (executor-base.md:275).
- Main agent hand-writes every SVG — never a sub-agent or generator (executor-base.md:278).
- Native background promotion: first full-canvas `<rect>` → `p:bg` (shared-standards-core.md:180).
- Static `<use>`/`<symbol>` reuse (shared-standards-core.md:85-103); markers (5 line-end types) (:73-75); image clip-path only on `<image>` (:79-81).
- Flat page: root `data-pptx-page-role` cover/toc/section/content/ending; `data-pptx-role` background/decoration/header/footer/logo/watermark/chrome/page-number (semantic-svg.md:9-13,60-69).
- Fact provenance on page: source footnote; `Scenario data`/`情景数据` label; "our reading"/`整理` label for frameworks the source doesn't state (executor-base.md:268).

### 3.16 Structured templates (executor-structured.md, pptx-structure-interface.md)
- mirror: copy, edit text in place, topology frozen; misfit → warning + return to Strategist (executor-structured.md:27-39).
- layout: re-skin paint from lock; **font size is skin — template hardcoded sizes never inherited** (executor-structured.md:23-25).
- Required per-page output: `📝 Template mapping` + `🎯 Adherence rules / application plan` (executor-structured.md:41-46).
- Slot coverage, layer coverage (master/layout atoms), Layout identity rules (executor-structured.md:54-57); metadata table & placeholder types (pptx-structure-interface.md:34-57); slot capacity: mostly-empty slot → raise type to top of band / add source detail / smaller prototype (pptx-structure-interface.md:67).

### 3.17 Notes (executor-notes.md)
- `notes/total.md`, `# <n>_<title>` + `---`; prose only, TTS-safe (executor-notes.md:11).
- Grounded in final SVG; cover every information-bearing group; proposition → evidence → implication (executor-notes.md:19-28); per-reading-mode emphasis (:32-36).

### 3.18 Animations (animations.md)
- Capability menu (animations.md:9-19); defaults fade 0.4 s, per-element off, sound off (:29-33); `animations.json` sidecar (:41-88); Morph pairs (:90-115); 48 transitions mapped to page relationships (:136-160); 203 object presets; lifecycle static/enter/emphasize/move/exit (:207-213); ambient motion, carousel/odometer/parallax/flip recipes (:219-228). "auto-firing builds on every page are an unsolicited 'AI deck' tell" (:23).

---

## 4. Quality gates

### 4.1 Mandatory
- Strategist Gate 1 (active-decision fidelity) and Gate 2 (lock context fidelity) (strategist.md:257-259); `project_manager.py validate` owns grammar (strategist.md:19).
- Icon sync GATE (strategist.md:150); `visualization_recall.py validate` for every ref (plan-core.md:137-140).
- `svg_quality_checker.py` (unfiltered; fix all errors + selected warnings in one pass; never defer past `finalize_svg.py`; warnings advisory) (executor-base.md:284). Final: `--canonical-authoring --stage final --json` → `validation/svg_quality_report.json` (artifact-ownership.md:50,89).
- Checker-enforced items seen in slice: fail-closed property allowlist (shared-standards-core.md:31,63); XML entity rules (:41-46); structural blacklist mask/style/class/foreignObject/textPath/@font-face/animate/script/iframe (:48-61); root-group overlap >1px fail, text overflow >5% fail (warn ≤5%) (:190); sibling-`<text>` paragraph warning (:178); preset helper metadata drift (executor-base.md:327; native-shape-authoring.md:24); font-size anchor drift 2px, id uniqueness, spec-lock comparison, animation_config (visual-review.md:7); web credit missing → error (executor-web-image.md:19); hyperlinks vs §IX (native-hyperlinks.md:51); formula compile + native-height envelope (native-formula.md:70); native chart/table parity "blocks --native-charts-and-tables" (native-data-interface.md:77); `--template-mode` placeholder warning (template-designer.md:236); `--canonical-authoring` compact-form advisory (shared-standards-core.md:67).
- Per-page `rg` checks for plot-area markers and native markers (executor-chart.md:66; native-data-interface.md:65).
- `verify-charts` stage when any value-driven chart exists (executor-chart.md:76).
- **Final carrier-receipt review (Mandatory)**: compare checker `[CARRIERS]` / `files[].info.carrier_receipt` with page jobs, resource roles, geometry signatures. Contradictions: adopted preset absent; direction/step/flow drawn as hand path; primary image reduced; unrelated jobs collapsing into one neutral construction. **Absence needs a written reason** for: deck-wide `Presets: (none)`; `inline emphasis 0`, `gradients 0`, `filters 0`; fewer preset/connector pages than order/link/parent/membership pages; no carrier-and-field contour; `icons: 0` with a registered pool. Families: carrier & field / direction & sequence / grouping & ownership / emphasis & annotation. "The style, speed, restraint, 'text was enough', or 'it is editable anyway' are not reasons" (executor-base.md:287-305).
- Export: no silent downgrade (animations.md:169); package postflight `[POSTFLIGHT]` (artifact-ownership.md:51).

### 4.2 Opt-in: visual review (visual-review.md)
- Only on explicit user request; Style Review Focus never activates it (strategist-template.md:59).
- Prereq: checker passed → `visual_review.py` render (visual-review.md:7).
- **Hard H1–H9**: out-of-bounds; text overflow; text overlap; readability (contrast <4.5 / <3.0 at ≥24px, text on complex image without scrim); (H5 retired); element collision; declared chrome displaced; image broken; missing key element (visual-review.md:15-29).
- **§1.1 brand-token escalation**: H4 on a brand token → don't edit, `needs_human`, append `.review/brand_review.json` (visual-review.md:31-33).
- **Soft S1–S10**: rhythm tight (<1.05×); rhythm hollow (>150 px, breathing exempt); intended anchor missed; alignment drift >4 px; grid non-uniform >5%; CJK letter-spacing >5%; decorative accents compete; **emphasis mismatch** (most prominent ≠ §IX primary); image-text relationship; **breathing violation** (≥3 rounded-card grid on breathing page) (visual-review.md:35-50). Deck-wide recurrences → `untouched_concerns` (:37).
- **STYLE**: Style Review Focus supplement; unmet → `rule: "STYLE"` (visual-review.md:13).
- §3 don't-touch: brand tokens, layout restructure, content, other files (visual-review.md:52-54). Budget 1 iteration; soft ≤2 fixes/iter; backups; batches K=5 subagents (visual-review.md:58-117).

---

## 5. Modes (references/modes)
- One mode per deck; mode = how you argue, independent of visual style; `custom` = blend as one behavior (modes/_index.md:3-5,56-58).
- **pyramid**: conclusion-first; title is the conclusion; SCQA opening; assertion titles; contextualize data without inventing comparisons; MECE only when source supports; title → takeaway → evidence; decomposition pages (driver tree, MECE, 2×2); source attribution on every data page; notes open with takeaway (modes/pyramid.md:9-58).
- **narrative**: situation → tension → resolution; suspense/payoff; human framing; beat titles; vary dense/breathing by tension (modes/narrative.md:9-43).
- **instructional**: decompose & sequence; parallel exposition; ground abstraction; signpost; "what it teaches" titles (modes/instructional.md:9-45).
- **showcase**: image/number leads; emotional rhythm; short evocative titles; full-bleed + hero number; "keynote-style" = showcase pacing (modes/showcase.md:9-43; modes/_index.md:46).
- **briefing**: no thesis; topic titles; `core_message` states coverage; complete, parallel, even; tables/status cards (modes/briefing.md:9-41). Least skeleton (modes/_index.md:23).
- Decision distinctions pyramid/briefing, narrative/pyramid, narrative/showcase, instructional/briefing (modes/_index.md:39-44).

---

## 6. Rules on density, hierarchy, focus, emphasis, color, anti-template

- Reading mode governs carriage: "`presentation` and `text` deck ... must differ in page grammar, count, text volume, visual burden, density, rhythm, and notes — not only in font size" (plan-core.md:50).
- Page rhythm: "the tag is what breaks the uniform card-grid feel" (plan-core.md:72); whole-roster rhythm check mandatory; "Same section, equal density, one style, and precedent establish no sub-arc"; breathing page "must stand alone" (plan-core.md:74).
- Cover impact mandatory; P01 "defaulting away from generic content-page templates" (plan-core.md:75). Closing: never "Thank you"/contact-only/cover reprise (plan-core.md:77).
- "Repeating symmetric card grids without a page job is the failure mode these structures exist to avoid" (executor-base.md:86).
- "Mechanical repetition comes from reusing one carrier and topology without a page job, not from cards themselves" (executor-base.md:243).
- Geometry signature repeat only for same job/deliberate continuity (native-shape-authoring.md:92); before stacked cards/equal columns compare page-field/outline/nesting/continuity (native-shape-authoring.md:69).
- HR no topology from balance alone (executor-structure.md:32); topology counts never imply equal size/spacing (topology-assembly.md:13).
- Carrier receipt: unrelated jobs collapsing into one neutral construction → vary (executor-base.md:294).
- Content field: "Unorganized residual space ... is leftover blank, not negative space"; unequal weight when information differs (shared-standards-core.md:250).
- Containers: "An unplanned repeated web-card grid is a carrier / topology problem" (shared-standards-core.md:254). Boundary strength ladder spacing → rule/bracket → tint → outline → panel → floating (shared-standards-core.md:253).
- Titles & chrome: title part of composition, not automatic header band; chrome only with a job (shared-standards-core.md:255).
- Typography roles: fewest roles; legible differences at thumbnail scale (shared-standards-core.md:245). Viewing distance: restructure/shorten/split/reflow, never silent miniaturization (shared-standards-core.md:246).
- Color: 60-30-10; "the accent color goes on the key number or word to create focus, not everywhere" (executor-base.md:118-119); color never carries a required distinction alone (shared-standards-core.md:247); sparse page-local accents never become a competing palette (executor-base.md:204); S7 accents compete (visual-review.md:47).
- Depth through restraint: ≤2–3 shadowed objects, peers flat, one weight tool per container (executor-base.md:121; svg-effects.md:226-232).
- Inline emphasis: 1–2 load-bearing nouns/numbers per sentence; never connectives/structural text; green/red only for real polarity (executor-base.md:125).
- Prose vs bullets: bullets only for genuinely parallel/ordered items; "A list that is merely easier to lay out ... is not a reason" (executor-base.md:231; plan-core.md:62).
- Never trim wording to fit; expand zone, reflow, switch texture before dropping a qualifier (executor-base.md:275).
- Effects: "'Advanced' means capability depth, not an effect quota" (svg-effects.md:18); one dominant composition scaffold (svg-effects.md:46).
- Animation restraint (animations.md:23).
- Table: horizontal rules only (executor-table.md:31).

---

## 7. Especially relevant to consulting-style (MBB) whitepaper decks

- Mode `pyramid` is the native MBB skeleton: assertion titles, SCQA, takeaway line, MECE/driver tree/2×2, source on every data page (modes/pyramid.md:9-41). A Style workspace's preferred mode seeds the lock (strategist-template.md:57).
- Reading mode `text` = read-close whitepaper: complete assertions, short prose, tables, fewer fuller pages, leans dense; body start 20 px (18–21) on ppt169 (plan-core.md:46; canvas-formats.md:35). `balanced` 24 px.
- Takeaway box / takeaway band under title; muted source note at bottom (executor-base.md:61,120); `{{KEY_MESSAGE}}` consulting placeholder (template-designer.md:243).
- Line-led construction is first-class: outline carrier lens (`fill="none"` frame/arc/bracket/band) (native-shape-authoring.md:84); boundary ladder starting from spacing/rule/bracket (shared-standards-core.md:253); hairline dividers 0.2–0.3 alpha, 2 px accent bar (executor-base.md:62,124); brackets/braces presets (preset-shape-vocabulary.md:60-61); light grouping brace (topology-assembly.md:38); 2×2 with non-central thresholds (topology-assembly.md:55); swimlanes (topology-assembly.md:54); tapered stack/pyramid tiers (topology-assembly.md:43).
- Neutral tiers `surface`, `grid` for chart/panel-layering styles (plan-core.md:158).
- Charts: monochrome depth, gray dashed benchmark baselines, accent only on key point, inflection annotations, source note (executor-chart.md:25); native editable charts/tables via `Native-ready=yes` + `--native-charts-and-tables` (native-data-interface.md:29-37).
- Tables: horizontal rules only, numbers right-aligned, one highlighted row (executor-table.md:31).
- Fact provenance: `Fact IDs`, compact source footnote, `Scenario data` label, "our reading" label on non-source frameworks (executor-base.md:268; plan-core.md:60).
- Decide-intent obligations: decision ask + options + criteria + trade-offs + consequence of delay (plan-core.md:31); Report: baseline + progress + variance + evidence + risk + ownership (plan-core.md:34).
- Installed Style = Direction/method only, flat route; visual values yield to Brand/Deck; no prototypes (strategist-template.md:29,57,67; executor-base.md:31). Template hardcoded font sizes never inherited (executor-structured.md:25).
- Recall aid: finance/business navy `#003366` (plan-core.md:152). OPPO Sans not preinstalled → needs target install or stays reference (plan-core.md:166).
- Carrier receipt "absence needs a reason" applies even to restrained styles — "restraint" is explicitly not a reason (executor-base.md:296-305). A thin wrapper should not add its own anti-template lint: rhythm check, geometry signature, carrier receipt, S5/S8/S10 already cover it.
- Per-page "module line" + geometry signature are in-context only — no artifact (executor-base.md:247; native-shape-authoring.md:92).
