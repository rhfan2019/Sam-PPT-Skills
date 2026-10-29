# ppt-master v6.7.2 capability map — slice C: visual styles + images

Root: `P = C:/Users/fanrh/.claude/plugins/cache/ppt-master/ppt-master/cc8b722a24e9-32c1cf49/ppt-master`. All paths below are relative to `P/references/`. Read-only; nothing modified.
Citation form: `file:line`.

---

## 1. Inventory (every file read in full; line counts from `wc -l`)

### visual-styles/ (19 files, 815 lines)
| file | lines |
|---|---|
| _index.md | 119 |
| blueprint.md | 38 |
| brutalist.md | 39 |
| chalkboard.md | 37 |
| dark-tech.md | 38 |
| data-journalism.md | 37 |
| editorial.md | 39 |
| glassmorphism.md | 37 |
| ink-notes.md | 38 |
| ink-wash.md | 37 |
| memphis.md | 38 |
| paper-cut.md | 37 |
| photo-editorial.md | 39 |
| pixel-art.md | 37 |
| sketch-notes.md | 37 |
| soft-rounded.md | 38 |
| swiss-minimal.md | 39 |
| vintage-poster.md | 37 |
| zine.md | 38 |

### image-*.md (5 files, 1003 lines)
| file | lines |
|---|---|
| image-base.md | 53 |
| image-generator.md | 433 |
| image-layout-patterns.md | 256 |
| image-layout-spec.md | 114 |
| image-searcher.md | 147 |

### image-palettes/ (15 files, 418 lines) — LEGACY, not used by current flow
_index 36, cool-corporate 26, dark-cinematic 32, duotone 27, earthy-dusty 26, editorial-classic 25, frost-ice 26, jewel-tone 25, macaron 27, mono-ink 35, nature-organic 26, sunset-gradient 28, tech-neon 25, vivid-launch 26, warm-earth 28.

### image-renderings/ (21 files, 818 lines)
_index 102, 3d-isometric 33, blueprint 33, chalkboard 35, corporate-photo 46, digital-dashboard 33, editorial 32, fantasy-animation 37, flat 33, glassmorphism 37, ink-notes 37, minimalist-swiss 37, nature 37, paper-cut 37, pixel-art 35, screen-print 36, sketch-notes 36, vector-illustration 35, vintage-poster 37, warm-scene 37, watercolor 34.

### image-type-templates/ (12 files, 708 lines)
_index 92, comparison 57, cycle 50, flowchart 67, framework 80, funnel 51, infographic 60, map 51, matrix 52, pyramid 50, scene 46, timeline 52.

### ai-image-comparison/** (56 files)
Text (read in full): README.md 65; palette/_subject.md 51, _manifest.md 248, _manifest.json 126; rendering/_subject.md 37, _manifest.md 351, _manifest.json 178; type/_subject.md 68, _manifest.md 209, _manifest.json 117.
Binary WebP (45): palette/*.webp ×14 (all 1280×720), rendering/*.webp ×20 (1280×720), type/*.webp ×11 (1024×1024 cycle/framework/matrix; 1024×768 infographic/scene; 768×1024 funnel/pyramid; 1280×544 comparison/flowchart/timeline; 1280×720 map). Each image's content is fully specified by the matching `_manifest.json` prompt; 5 rendering images (minimalist-swiss, editorial, blueprint, ink-notes, vector-illustration) were opened visually and match their prompts. `wc -l` counts on .webp are meaningless (binary).

---

## 2. Visual-style presets

### 2.1 What a "visual style" is and how it is selected
- Definition: how the deck **looks** (shape language, decoration density, whitespace, typographic character, texture/elevation). Exactly **one per deck**; Default profile locks it, Quick keeps it only in active context (visual-styles/_index.md:3).
- Hard capability boundary: style governs treatment/weight/density/coherence; it **never** decides carrier eligibility or image source, never narrows primitive / Office-preset / Boolean / freeform vocabulary (_index.md:5-10).
- **Styles carry NO HEX and define no palette.** Colors live in `design_spec.colors` / `spec_lock.colors` (confirmation `e`); fonts chosen at confirmation `g` (_index.md:12; every style file §2/§3 note).
- Style ≠ mode: "style = how it looks; mode = how you argue" (modes/_index.md); resolved independently, any pairing allowed (_index.md:14).
- Value of `visual_style` is only ever a first-column id (`swiss-minimal`, `editorial`…). "Paired rendering" column values are image-rendering ids, never a visual_style (_index.md:22).
- Read discipline: read only the index while choosing; after fixing, read ONE preset file, or every exact `visual_style_references` file for a catalog-based `custom`, or none for a novel custom. **Never glob the directory** (_index.md:20).
- `custom`: each Default Stage-2 direction authors one visible, non-empty `custom` aesthetic per strategist.md §d — executable shape language, composition geometry, decoration density, whitespace, typography character, texture — naming only catalog bases actually used. Quick resolves one preset or custom behavior per quick-generate.md §2 and persists nothing (_index.md:108-111).
- Selection is "reference, not constraint"; topic/industry keyword never selects a row; compare on shape/space, information texture, carrier integration, typography character, delivery/afterlife (_index.md:77-90).
- Default to derive shape language from project fit — test whether source/identity offers a more specific edge/corner/contour before settling on generic lines/rects/circles (_index.md:92-98).
- Each style's §1 "Composition geometry" is generative vocabulary, not a finite layout menu (_index.md:116-119).
- `Illus.` column = illustration centrality only after resource review selects illustration (core/supportive/sparse); never recommends adding illustration; `image_usage: none` writes no illustration rows (_index.md:24).
- Paired rendering is only a coherence candidate; not every rendering has a style twin (nature/warm-scene/fantasy-animation are imagery-only) (_index.md:100-104).
- Every style file has the same 6 sections: Shape & decoration, Typography character, Using the deck's colors, Texture/elevation, Paired image-rendering, Illustration propensity.

### 2.2 Catalog (18 presets)
| id | group | look / when (file:line) | paired rendering | illus |
|---|---|---|---|---|
| swiss-minimal | Corporate | Strict Swiss grid, sharp, aggressive whitespace, near-zero ornament; "high-end consulting, architecture, design firms, type-led" (swiss-minimal.md:3) | minimalist-swiss | sparse |
| soft-rounded | Corporate | Rounded cards, gentle elevation; product/SaaS/training/consumer (soft-rounded.md:3) | flat | supportive |
| glassmorphism | Corporate | Translucent glass panels on dark field, gradient light; SaaS/fintech/AI demos (glassmorphism.md:3) | glassmorphism | sparse |
| dark-tech | Corporate | Dark canvas, glow accents, geometric precision; tech/AI/dev tools (dark-tech.md:3) | digital-dashboard / blueprint | sparse |
| blueprint | Corporate | Schematic line work on dark paper, isometric, annotations; architecture/engineering whitepapers (blueprint.md:3) | blueprint | supportive |
| editorial | Editorial | Magazine hierarchy, rules & columns, serif/sans; finance/journalism/research/long-form analysis (editorial.md:3) | editorial | supportive |
| photo-editorial | Editorial | Full-bleed photography dominates; architecture/fashion/culture (photo-editorial.md:3) | corporate-photo | sparse |
| data-journalism | Editorial | Bloomberg/Economist density: multi-column micro-charts, sidebars, source lines; finance/market reviews/research (data-journalism.md:3) | editorial | sparse |
| brutalist | Editorial | Newsprint density, ruled boxes, thick rules; annual reviews, research digests, manifestos (brutalist.md:3) | screen-print / editorial | supportive |
| memphis | Expressive | Clashing color blocks, confetti, bold outlines; festivals/consumer/youth (memphis.md:3) | flat | core |
| zine | Expressive | Riso misregistration, halftone, print grit; culture/design talks (zine.md:3) | screen-print | core |
| vintage-poster | Expressive | Mid-century flat blocks, halftone; heritage/hospitality/anniversaries (vintage-poster.md:3) | vintage-poster | core |
| paper-cut | Expressive | Layered cut paper with soft inter-layer shadow; education/children/folk (paper-cut.md:3) | paper-cut | core |
| sketch-notes | Hand-drawn | Warm paper, doodle line work, pastel blocks; education/onboarding (sketch-notes.md:3) | sketch-notes | core |
| ink-notes | Hand-drawn | Pale field, black hand-ink, sparse semantic accent; "professional end of hand-drawn", methodology/manifestos (ink-notes.md:3) | ink-notes | supportive |
| chalkboard | Hand-drawn | Dark slate, chalk strokes, pastel accents; teaching (chalkboard.md:3) | chalkboard | core |
| ink-wash | Hand-drawn | Rice paper, brush marks, single seal-red accent; 新中式/culture/philosophy (ink-wash.md:3) | ink-notes / watercolor | supportive |
| pixel-art | Specialty | 8-bit grid, blocky, limited palette; gaming/retro (pixel-art.md:3) | pixel-art | core |

(Catalog table: _index.md:30-71.)

### 2.3 Presets relevant to consulting / MBB whitepaper decks — what they prescribe
**swiss-minimal** (explicitly "high-end consulting", swiss-minimal.md:3)
- Lines vs blocks: sharp exact contours, true circles, **single-weight rules**, "a small number of large geometric planes"; square corners default (:9). Composition: one oversized plane / full-height color column / hero numeral / single diagonal rule as grid break — "Few, large, exact" (:10).
- Decoration: omit any ornament without an information/composition job; no ornamental gradients, decorative blocks, badges (:11). Whitespace vast; layout snaps to modular grid (:12-13).
- Type: single sans family, regular/bold contrast; large headlines, small precise body, left-aligned flush (:17-18).
- Color: near-white field; a dominant color may define a deliberate grid zone; accent localized as punctuation; "Color as conceptual zone… No gradients" (:24-25).
- Texture: strictly flat, no shadows (:31). Illustration sparse (:39).

**editorial** (finance/research/long-form, editorial.md:3)
- Lines over cards: "thin rules and column dividers over repeated cards"; outlined/compound contours allowed when they clarify; rounding minimal (:9).
- Composition: oversized drop cap/numeral, pull quote across columns, full-height vertical rule the content hangs from, asymmetric column split, figure crossing column edge (:10).
- Decoration: hairline rules, kickers/eyebrows, pull quotes — typographic not graphic (:11). Multi-column flow; "comfortable but information-rich" (:12-13).
- Type: serif/sans interplay; kicker → headline → standfirst → body hierarchy (:17-18).
- Color: mostly monochrome text on light field; restrained accent on a rule/figure/kicker (:24-25). Flat; shadow only on genuine floating element (:31).

**data-journalism** (finance, market reviews, research, data reports, data-journalism.md:3)
- Density is the look: dense multi-column grid, inline small charts/tables, sidebars, pull-stats, **hairline dividers**, hero numbers, running source/footnote line (:9).
- Composition: chart as page spine (layout wraps chart, not boxed); hero number at full column scale; spanner rule into stat band; sidebar cut into grid; small-multiple strips (:10).
- Decoration minimal beyond data; tight but structured whitespace (:11-12).
- Type: serif headline/hero number × sans/mono lining figures (:16).
- Color: restrained field (light paper or dark graphite); accent marks risk/key figures; charts use tints of one family, never rainbow; numbers colored to mean up/down/risk/focus (:22-23).
- Texture: flat; "favor hairline rules over heavy cards"; no glow/decorative shadow (:29).

**brutalist** — densest option; thick black borders, `rx="0"`, irregular column widths, one inverted ink cell, near-monochrome + spot accent; no gradients/shadows (brutalist.md:9-31). Less "consulting polish", more manifesto.

**ink-notes** — near-monochrome ink + sparse semantic accent, line defines structure, "repeated filled-card grids are not the default grammar" (ink-notes.md:9, :23-24); hand-drawn character makes it less MBB.

**blueprint** — single line color + one spot accent on dark paper (blueprint.md:23-24); fits technical whitepapers, not standard MBB.

Summary for an MBB "lines-not-blocks, restrained color" whitepaper: the closest presets are **editorial** (rules/columns), **swiss-minimal** (grid, single-weight rules, color-as-zone) and **data-journalism** (dense evidence + hairlines); a catalog-based `custom` can combine them via `visual_style_references` (_index.md:20, :110). soft-rounded is the card-heavy opposite ("cards as the primary container", soft-rounded.md:11).

### 2.4 Construction rules embedded in style files (easy to miss)
- glassmorphism: bloom/glow halo must be `<circle>`/`<ellipse>` + `<radialGradient>`, never `rect rx=w/2` (glassmorphism.md:11); the one style where generous gradients are on-brand (:29).
- Hand-drawn marks (chalkboard, ink-notes, sketch-notes, ink-wash, paper-cut): realize as `<path>`/`<polyline>`/`<polygon>` with non-aligned points, not pristine primitives (chalkboard.md:9; ink-notes.md:9; sketch-notes.md:9; ink-wash.md:9; paper-cut.md:9).
- soft-rounded: prefer native `arc`/`blockArc` presets before custom arc paths (soft-rounded.md:10).
- photo-editorial: deterministic fallback — page with no usable image renders in `editorial` text-led layout, never an empty dashed frame (photo-editorial.md:14).
- paper-cut: layered soft drop shadow is core, not a violation (paper-cut.md:29).
- Exact Light/Black weights require a user-confirmed installed face (swiss-minimal.md:17; glassmorphism.md:16).

---

## 3. Image capabilities

### 3.1 Common framework (image-base.md)
- Trigger: any resource row with `Acquire Via: ai|web|slice`, or a pending prepared derivative; `user`/`placeholder` rows tracked but skipped. Source: Default `design_spec.md §VIII`; Quick active context; or standalone on an existing project (image-base.md:7).
- Resource row columns: Filename | Dimensions | Purpose/Type | Image pattern | Crop Policy (`adaptive`/`no-crop`) | Acquire Via | Status | Reference (image-base.md:13-15).
- Dispatch table (image-base.md:19-26):
  - Prepared derivative (`Reference: Derived from <parent>; treatment=<op>`) → `image_treat.py` to a distinct `.png`, parent preserved; status inherits parent.
  - Registered-layer derivative → image-generator §4.4.
  - `ai` → `image_gen.py` → `Generated`.
  - `web` → `image_search.py` → `Sourced` (`Needs-Selection` intermediate).
  - `slice` → `slice_images.py` after parent sheet `Generated`.
  - all-web deck never reads image-generator.md and vice versa (:28).
- Treatment paths: `none` / `native` (SVG crop/clip/opacity/frame/shadow/scrim/vignette — no file) / `prepared derivative` (only pixel blur, desaturate/grayscale, duotone, brightness/contrast, downscale `image_treat.py --fit WxH` never upscale, cutout/registered-layer). Never bake a native treatment into a derivative (image-base.md:30).
- Pattern→preparation map: A1-02/A1-03 → `image_treat.py` blur/duotone; A1-01/A1-04 need existing composite or AI (`image_treat.py` does not blend); A2-01 RGBA/keyed asset; A2-02/A2-03 §4.4; A2-04 transparent device frame; A3-01..03 registered derivatives (image-base.md:32).
- `Reference` is intent, not query (image-base.md:34).
- Procedure: run `analyze_images.py` once before SVG; verify every row terminal; agent writes Status back (tools only update own manifests) (image-base.md:38-41).
- Failure: automatic exhaustion of all permitted strategies before blocking; `Needs-Manual` handoff lists filename, prompt location `images/image_prompts.md` (refresh `image_gen.py --render-md`), target path, slice parent/names (image-base.md:47).
- Credits only in `project/images/image_sources.json` — never notes (TTS would speak them), total.md, or SVG `<title>/<desc>`; user assets with licence terms registered there too; per-slide credit required, closing sources page doesn't replace it (image-base.md:51).
- Default Executor never runs image_gen/image_search/slice_images/image_treat (image-base.md:53).

### 3.2 AI generation (image-generator.md)
- Inputs per image: `page_role` = `local` | `hero_page`; `text_policy` = `none` | `embedded` (image-generator.md:15-23).
- Hard rules: one `deck_rendering` + same core deck colors for every image; HEX is guidance not text; long copy/data/bullets stay SVG; one coherent prose paragraph, no tag soup (:27-33).
- Dimensions: Rendering (once per deck), Deck colors (from `spec_lock.md colors`), Type (optional per image, 11 types) (:39-43). On-demand loading: read renderings + type indices once, then only selected files; never glob (:47).
- Prompt assembly template: rendering paragraph (80–120 w) + deck color behavior + composition (type or §4.1) + subject + container note ("composed as WxH px for page_role") + hard rules; budget 150–300 words (:81-90).
- Missing `image_rendering` in lock → infer from design_spec d. Style, print notice (:65).
- No-type primitives §4.1: A single dominant subject; B portrait; C typographic hero (`embedded`); D atmospheric backdrop (`hero_page` only); E custom prose (2–5 sentences) incl. structural infographics with no template; fewshots for A–D (:94-110).
- §4.2 Subject-domain depth: scientific/medical/engineering/legal figures expand to 500–1000+ words; no pre-emptive shortening; name field conventions (:113-114).
- §4.3 **Illustration sheets**: one generation → many transparent illustration / illustrated-icon / decorative-lettering elements; sheet is never placed, only slices (:117-122). Grid derived from target shape; each element ~65% of cell, ≥10% key margin; flat chroma key `#00FF00`/`#0000FF`/`#FF0000` stated first and last (:128-129). Lettering sheet: one literal string per cell; lone mark on wide sheet → use ~4:1 band to avoid ghost copy (:132). Grid table by element shape (:137-143). `slice_images.py <sheet> --grid RxC --names a,b,… --trim --alpha --bg "#00FF00" --strict-alpha` (:155-158); `--tolerance`, `--inset H,V` (e.g. `0.01,0.03`) for model-drawn grid lines (:168). Source pixels ≥1.5–2× display size (1K/2K/4K) (:170). Placement: slices are accessories, unboxed, may bleed/rotate; no quota (:172). Several opaque photos for a multi-cell layout may share one sheet sliced by `--grid --inset` without key/trim/alpha (:120).
- Resource contract: sheet row `Acquire Via: ai`, `Type: Illustration Sheet`, manifest carries `slice_grid` + `slice_names`; element rows `Acquire Via: slice`, `crop=no-crop`, `Type: Illustrated icon` (never an SVG library entry) (:149-152).
- §4.4 **Registered reconstruction groups / shared plates**: clean base (inpainted) + subject/foreground RGBA layers + optional midground + shared non-overlapping plate; preserve registration, never trim registered outputs (:176-198). Uses `image_gen.py "<instruction>" --reference-image <src> -o … -f <name>` then `slice_images.py --grid 1x1 --alpha` (:204-210). Image-to-PPTX profile requires Codex native reference-image capability; other hosts unsupported (:187).
- §5 global hard rules: HEX-not-text sentence (:221); likeness authorization for real people (:225); two-layer text ownership (Layer 1 image-owned stable art/figure labels; Layer 2 SVG editable) (:229-234); decide by editability, never by script/length; non-Latin embedded text gets one verification look, 3 regen max, then native-text fallback (:241-243); font-echo table for in-image lettering (:249-255); no brands/trademarks unless user-owned (:261).
- §6 Manifest `project/images/image_prompts.json`: `deck_rendering`, `color_scheme` {background, secondary_bg, primary, accent, secondary_accent, body_text}, items[] {filename, purpose, type?, page_role, text_policy, aspect_ratio, image_size 512px/1K/2K/4K, prompt, model?, alt_text?, slice_grid/slice_names, status} (:269-319). Backends accept subsets of aspect ratios (gemini no 3:1); `--manifest` fails item pre-request (:313). Legacy spellings in scripts/docs/image.md (:321).
- §7 Execution paths (:329-345):
  - **Path A** `python3 scripts/image_gen.py --manifest project/images/image_prompts.json --output project/images` — concurrent, atomic status, interrupt-safe; backend/.env/provider keys in scripts/docs/image.md; single-image form `image_gen.py "prompt" --filename …` for re-rolls (:351-355).
  - **Path B** host-native image tool (Codex, Antigravity, Claude Code…), batch ~3–4; still run `image_gen.py --render-md` for sidecar (:359).
  - **Offline Manual** only on explicit `manual`; dashed placeholders; export blocked until files validated (:363-368).
  - `auto`: A if `IMAGE_BACKEND` set (2 consecutive failures → B), else B (:342). Confirmed path never switches provider (:347).
  - Default exhausted decision: Repair-and-retry / Generate manually / Cancel affected AI images (:372-378). Quick: silent no-AI replan (:382).
  - `scripts/gemini_watermark_remover.py` exists for watermarked web outputs (:384).
- §8 Blank-Reference inference table (cover→hero_page A/D; framework→type framework; process→flowchart; before/after→comparison; team→scene; headshot→B; big number→C) (:394-404); symptom→adjustment troubleshooting (:408-419); variant workflow: set status Pending, edit prompt, rerun; or append `_v2` items (:421).
- §9 Forbidden list (:427-433).

### 3.3 Web sourcing (image-searcher.md)
- License tiers: `no-attribution` (CC0, PD, Pexels, Pixabay), `attribution-required` (CC BY, CC BY-SA), `manual` (direct URL/adopted page); auto-reject NC/ND/ARR/unknown (image-searcher.md:15-21).
- Quality first across tiers; `--strict-no-attribution` opt-in (:27).
- Providers & chain: pexels (`PEXELS_API_KEY`) → pixabay (`PIXABAY_API_KEY`, max 1280px) → openverse (zero-config) → wikimedia (zero-config; pin `provider: wikimedia` for artworks/museum objects) (:41-48).
- Query translation: concise entity keywords; `query_variants` for translations/aliases/Chinese names; `required_terms` groups with `|` aliases for exact entities; no negative words (:56-61).
- Commands: single `python3 scripts/image_search.py "<query>" --filename x.jpg --slide id --orientation landscape --purpose background -o <proj>/images` (:74-75); batch `--batch images/image_queries.json --save-candidates` (:83); item fields filename/query/status + optional query_variants, candidate_page, slide, purpose, orientation, provider, strict_no_attribution, min_width, min_height, required_terms (:97).
- Review: with vision → first 8 ranked previews under `candidates/<stem>/review/` + `review_sheet.jpg`, run workflows/stages/web-image-review.md (isolated reviewer); `--candidate-page 2` before changing query; without vision → metadata-ranked best-only (:101-102).
- Replacement ladder: promote → next page → new variants → adopted-page package (topic-research hand-off, license `manual`) → `--from-url` manual replace → `Needs-Manual` (:104).
- Standalone thumbnail selection commands incl. `--promote candidate_03.jpg` (:108-113).
- Manifest `image_sources.json` keyed by filename: license_tier, attribution_text, width/height, selection_method (:121).
- On-slide attribution contract with compression examples; `svg_quality_checker.py` verifies each attribution-required image has its own visible credit (:127, :143).

### 3.4 Layout patterns (image-layout-patterns.md) — 90 catalogued ids
- Groups: P (Primary structures, 47) = P1 single visual / P2 image-as-canvas with native overlay / P3 multi-visual; M (Modifiers, 28) = M1 reveal/crop/registration, M2 tone/focus, M3 framing/depth; A (asset-dependent, 11) = A1 composites, A2 subject layers, A3 registered derivatives; C (cross-page continuity, 4) (image-layout-patterns.md:18-23). Note: body enumerates P1×13, P2×10, P3×24, M1×12, M2×9, M3×7, A1×4, A2×4, A3×3, C×4.
- "Reference — not a constraint"; inventing uncatalogued forms equally valid; IDs like `#P1-01` (:11-12).
- Mechanism owners: geometry → image-layout-spec; treatments → svg-effects §6.1; Boolean holes/text subtraction → native-shape-authoring; per-pixel mask → prepared asset (:25-35).
- Situation router (:41-52) and high-yield combinations playbook (:232-250), e.g. cover = `#P1-01 + #M2-01`; bento = `#P3-12 + #P3-14 + #P2-05`; curved photo wall `#P3-24`; folded strips `#M1-11 + #M2-03`.
- Notable: P2 overlays live inside the picture root group, cost no page area (:76); `#P2-03` vs `#P2-04` not interchangeable (:89); `#M1-10/#M1-11/#P3-21` topology table (:139-143); `#M1-12` glyph-shaped picture defaults to editable native text picture fill (svg-effects §6.3) (:135); registration boundary list (:252).
- Combination procedure: Skeleton → Job → Apply → Prepared asset → Continuity → Integrate → Stop (:220-228).

### 3.5 Layout geometry (image-layout-spec.md)
- Ownership: Strategist chooses resource/role/crop; Image_Generator composes inside bitmap; Executor owns final SVG geometry (image-layout-spec.md:11).
- Contain / Fill formulas with anchors `ax, ay` (:21-38); mode selection by narrative intent — page / backdrop / coequal block / accent; don't default to side-by-side; portrait canvases and 4:3 favor stacked (:42-44).
- Single image weighted split `q_item/q_other` (:50-55); equal grid & weighted tracks (:63-78); free multi-item composition with centers, sizes, z-rank and direction generators `vector` / `shared-baseline` / `curve-spine` / `panel` (:82-91); angle mechanisms; **no shear/skew/perspective** (:93).
- 12-row composition check table (:99-112).

### 3.6 Renderings (image-renderings/) — 20 presets, one per deck
- Lock one rendering per deck; HEX not in renderings; core deck identity has precedence, sample HEX in files is illustrative (image-renderings/_index.md:3-7).
- Catalog: modern/commercial — vector-illustration, flat, minimalist-swiss, glassmorphism, 3d-isometric, digital-dashboard, corporate-photo, blueprint, editorial; hand-drawn — sketch-notes, ink-notes, chalkboard, paper-cut; narrative — watercolor, warm-scene, screen-print, vintage-poster; specialty — fantasy-animation, pixel-art, nature (_index.md:15-53).
- `custom` rendering: every Stage-2 direction carries one complete `rendering: custom` candidate even when AI not recommended; UI hides rendering controls until AI source selected; `image_rendering_behavior` 2–5 sentences covering line/texture/depth/material/mood; `image_rendering_references` owned by strategist-image.md §2 (_index.md:57-72).
- Each file: paste-ready style paragraph (90–110 w), line/texture/depth table, deck-HEX role mapping, fewshot snippet. Consulting-relevant: vector-illustration "default safe rendering" (vector-illustration.md:3), minimalist-swiss for high-end consulting (minimalist-swiss.md:3; accent ≤2–3%, :29), editorial default for finance/explainers (editorial.md:3), blueprint near-monochrome 1–1.5px lines (blueprint.md:7). ink-notes/chalkboard use exact deck roles (body_text as ink) and should only be offered when roles support the contrast (ink-notes.md:23-29; chalkboard.md:23-27). corporate-photo maps HEX to color grading (corporate-photo.md:33-38).

### 3.7 Palettes (image-palettes/) — LEGACY tombstone
- Current generation **never** presents/selects/consumes `image_palette`; legacy rows ignored; do not load sibling presets (image-palettes/_index.md:7-20). Files kept only for diagnosing historical locks and the palette comparison gallery (:26). 14 archived behaviors (cool-corporate "default for consulting/finance/B2B", cool-corporate.md:3; mono-ink overrides deck primary/secondary, mono-ink.md:9-15; dark-cinematic overrides background, dark-cinematic.md:9; sunset-gradient forces background gradient, sunset-gradient.md:21).

### 3.8 Type templates (image-type-templates/) — 11 internal skeletons for `local` AI infographics
- Type = geometric skeleton inside the painted rectangle, per image; not page_role, not subject (_index.md:3-13). hero_page and single-subject/portrait skip type (:15).
- infographic, flowchart, framework (hub/matrix/layered stack), matrix 2×2, cycle, funnel, pyramid, comparison, timeline, map, scene (_index.md:23-35); Purpose→type auto-table (:43-57); default containers (flowchart 1200×400, timeline 1200×350, funnel/pyramid 600×800, etc.) (:67-79); most decks use 2–4 types (:89).
- Each file: skeleton ASCII + LAYOUT/ELEMENTS/NEGATIVE SPACE table, `none`/`embedded` variants, fewshot (vector-illustration + cool-corporate baseline). Matrix: `none` is lower-risk because models render axis labels inconsistently (matrix.md:36); scene diegetic text "often fails" (scene.md:38).
- Note: these are AI-bitmap diagrams; editable native diagrams are a different subsystem (executor/native-shape refs, outside this slice).

### 3.9 Comparison gallery (ai-image-comparison/)
- Controlled-variable sets: rendering ×20 (baseline Primitive A + cool-corporate), palette ×14 (legacy), type ×11 (vector-illustration + cool-corporate) (README.md:10-14). Generated with OpenAI gpt-image-2; other backends differ (:34).
- Confirm UI displays **rendering only**, serving `rendering/<id>.webp` (README.md:3, :55); palette set must not reintroduce a color decision (:65).
- Regenerate: `python3 skills/ppt-master/scripts/image_gen.py --manifest .../rendering/_manifest.json -o .../rendering/ --backend openai` (README.md:38-53); re-encode PNG→WebP q85.
- `_manifest.md` files are `image_gen.py --render-md` sidecars (rendering/_manifest.md:3). Type set uses aspect ratios 4:3, 21:9, 1:1, 3:4, 16:9 (type/_subject.md:43-55).

---

## 4. Opt-in / easy-to-miss features
1. `visual_style: custom` with `visual_style_references` — combine several catalog styles (e.g. editorial + swiss-minimal + data-journalism) instead of one preset (visual-styles/_index.md:20, :110).
2. Styles never set colors/fonts — those are confirmations `e`/`g`; a wrapper that wants fixed HEX must lock them in design_spec/spec_lock, not in a style (visual-styles/_index.md:12).
3. photo-editorial auto-fallback to editorial when no image (photo-editorial.md:14).
4. Illustration sheets + `slice_images.py` → transparent icon/illustration/lettering sets from one generation (image-generator.md:117-172).
5. Registered reconstruction groups / shared plates for subjects crossing native frames (image-generator.md:176-210; patterns #A2-03).
6. `image_treat.py` prepared derivatives (blur, duotone, desaturate, `--fit WxH` downscale) (image-base.md:21, :30).
7. `analyze_images.py` must run once before SVG; backfills Dimensions (image-base.md:40; image-generator.md:152).
8. `image_gen.py --render-md` writes paste-ready `images/image_prompts.md` for manual generation (image-generator.md:359, :363).
9. `--reference-image` edit mode on image_gen.py (image-generator.md:205-208).
10. `IMAGE_BACKEND` env selects Path A; otherwise host-native image tool (Claude Code counts) (image-generator.md:331-342, :359).
11. Per-item `model` override and `image_size` 512px–4K (image-generator.md:315-316).
12. Subject-domain long prompts (500–1000+ words) for technical figures (image-generator.md:114).
13. Non-Latin (CJK) embedded lettering: one check look, 3 regenerations, then native-text fallback (image-generator.md:243).
14. `scripts/gemini_watermark_remover.py` (image-generator.md:384).
15. Web: `--strict-no-attribution`, `required_terms`, `query_variants`, `--save-candidates`, `--candidate-page`, `--promote`, `--from-url`, `provider: wikimedia` pinning, `min_width/min_height` (image-searcher.md:27, :61, :97-113).
16. Isolated vision reviewer workflow `workflows/stages/web-image-review.md` (image-searcher.md:101).
17. Attribution enforced by `svg_quality_checker.py`; credits never in notes (TTS) or `<title>` (image-searcher.md:143; image-base.md:51).
18. Cross-page continuity patterns C1/C2/C3 (persistent overlay, pan, push-in, matched framing) (image-layout-patterns.md:197-210).
19. Image-as-canvas P2 overlays inside the picture root group (no page area cost) (image-layout-patterns.md:76).
20. Direction generators and the ban on shear/skew/perspective for multi-image layouts (image-layout-spec.md:84-93).
21. Image palettes are dead code — do not wire them into a wrapper (image-palettes/_index.md:7-20).
22. Rendering `custom` candidate is always authored per direction even without AI (image-renderings/_index.md:57).
23. Comparison gallery `rendering/*.webp` doubles as the Confirm UI's rendering picker assets (ai-image-comparison/README.md:55).
