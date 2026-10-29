# D. ppt-master v6.7.2 — `templates/` capability map

Root: `P = .../ppt-master/cc8b722a24e9-32c1cf49/ppt-master`; all paths below relative to `P/templates/` unless prefixed. Read-only survey 2026-10-26. Citations are `file:line`.

---

## 1. Inventory

### 1.1 Markdown read in full (line counts)

| File | Lines |
|---|---:|
| README.md | 56 |
| VISUALIZATION_TEMPLATE_AUTHORING.md (Chinese, maintainer guide) | 463 |
| design_spec_reference.md | 196 |
| spec_lock_reference.md | 107 |
| scaffolds/design_spec.md / scaffolds/spec_lock.md | 116 / 46 |
| brands/README.md | 25 |
| brands/*/templates/design_spec.md — accenture, alibaba, aws, bain, bcg, deloitte, huawei, ibm, jpmorgan, mckinsey, nvidia, tencent, xiaomi | 63 each |
| brands/anthropic 70, google 68, microsoft 65, pwc 66, zcare-rescue 80, 中国电信 72, 中国电建 76, 中汽研 72 | — |
| styles/README.md | 32 |
| styles/*/templates/design_spec.md — academic-research 81, consulting-decision 77, creative-pitch 80, duty-manual 109, incident-postmortem 91, investor-pitch 81, **mbb-consulting 103**, narrative-keynote 78, operating-review 91, product-launch 76, science-explainer 79, solution-proposal 80, technical-deepdive 88, workshop-teaching 76 | — |
| layouts/README.md | 53 |
| layouts/*/templates/design_spec.md — editorial_bleed 72, moments_square 64, presentation_core 103, presentation_core_43 90, report_core 82, story_vertical 70, xiaohongshu_post 72 | — |
| decks/README.md 57; decks/中国电信 81; decks/中汽研 77 | — |
| charts/README.md 63; charts/chart-vocabulary.md 75 | — |
| tables/README.md 65; tables/table-vocabulary.md 21 | — |
| icons/README.md 46; icons/THIRD_PARTY_NOTICES.md 100 | — |
| sounds/README.md 63; sounds/THIRD_PARTY_NOTICES.md 71; sounds/sound-vocabulary.md 252 (section headings + first 60 rows read; rest is an id/label/duration list) | — |
| Total md | 5,196 |

Also read (outside slice, for install mechanics): `P/workflows/stages/apply-template-workspace.md` (114 lines).

### 1.2 Non-md assets

| Folder | Contents | Count |
|---|---|---:|
| (root) | brands_index.json, styles_index.json, layouts_index.json, decks_index.json (inside each kind dir) | 4 indexes |
| schemas/ | design_spec.schema.json, spec_lock.schema.json | 2 |
| charts/ | `<key>.svg` + charts_index.json | 33 SVG |
| tables/ | `<key>.svg` + tables_index.json | 6 SVG |
| layouts/ | prototype SVGs: editorial_bleed 10, moments_square 8, presentation_core 20, presentation_core_43 16, report_core 13, story_vertical 9, xiaohongshu_post 10 | 86 SVG |
| decks/ | 中国电信 5 SVG + 6 PNG; 中汽研 5 SVG + 2 PNG | 10 SVG, 8 PNG |
| brands/ images | anthropic 3 SVG, google 2 SVG, zcare-rescue 9 PNG, 中国电信 1 PNG, 中国电建 4 PNG, 中汽研 2 PNG; **all 15 other brands: no images, no SVG** | 5 SVG, 16 PNG |
| styles/ | spec only, no assets (by contract, styles/README.md:32) | 0 |
| scaffolds/ | 2 md | — |
| icons/ | chunk-filled 641, tabler-filled 1,055, tabler-outline 5,138, phosphor-duotone 1,518, simple-icons 3,675 | 12,027 SVG |
| sounds/ | kenney-interface 100, kenney-ui 51, bigsoundbank 35 WAV + sounds_index.json + CC0-1.0.txt | 186 WAV |
| All files under templates/ | — | 12,450 |

---

## 2. Template kinds

Four independent kinds, **not** an inheritance chain; each owns one segment (README.md:5-12).

| Kind | Owns | Never owns | Files | Index |
|---|---|---|---|---|
| **Brand** | identity: colour, type, logo, voice, icon style (README.md:9) | page structure, SVG roster | `templates/design_spec.md` (frontmatter `kind: brand`, 6 required sections I Overview / II Color / III Typography / IV Logo / V Voice & Tone / VI Icon Style) + optional `images/`, `icons/` (brands/README.md:13-21) | brands_index.json `brand_id → {summary, primary_color}` (brands/README.md:25) |
| **Style** | communication method + visual-language defaults: argument flow, page-role vocabulary, evidence/data discipline, composition, density, decoration, colour behaviour, image/icon direction, review focus (styles/README.md:3) | identity, geometry, SVGs, current-project contract (styles/README.md:28) | one file only, frontmatter `style_id, kind, summary, keywords` (3–5); sections I–VII; optional `Fallback Color Scheme` / `Fallback Typography` = lower-priority defaults, never identity; §VII must contain exactly one `<!-- visual-review-trigger: explicit-user-only -->` (styles/README.md:26) | styles_index.json `style_id → {summary, keywords}` |
| **Layout** | brand-neutral structure: canvas, Master/Layout graph, page types, slot geometry, semantic text roles, capacity, SVG roster (layouts/README.md:3) | colour, typeface identity, final type scale, logo, voice, narrative | spec frontmatter `layout_id, kind, category, summary, canvas_*, replication_mode, native_structure_mode: structured, page_count, page_types, placeholders:` + §IV Signature Design Elements, §V Page Roster, §VII Placeholder Overrides (layouts/README.md:22-45); SVGs are complete Slide previews (layouts/README.md:49) | layouts_index.json `{summary, canvas_format, page_count, page_types}` |
| **Deck** | recurring presentation family: application context + integrated identity + structure (decks/README.md:3) | — | frontmatter `deck_id, kind, category, summary, primary_color, canvas_*, replication_mode, native_structure_mode, page_count`; §I Template Overview, II Color, III Typography, IV Signature, V Page Roster, VI Assets, VII Placeholder Overrides (decks/README.md:22-47) | decks_index.json `{summary, canvas_format, page_count, primary_color}` |

Orthogonal axes, never synonyms (README.md:20-28): kind; selection source `library`/`explicit`; internal creation strategy `standard`/`fidelity`/`mirror` (tool provenance, never user choice); internal application plan `template_reuse_scope` (+ optional `template_adherence` strict/adaptive) decided by Strategist; PPTX structure `flat`/`structured`.

**Workspace contract** (README.md:32-40): `<root>/templates/` (spec + SVGs + optional `native_payloads.json.gz`), `images/` (referenced `../images/<name>`), `icons/imported/` (`data-icon="imported/<name>"`), `exports/` (review evidence, never input). Library root keeps `templates/design_spec.md`; project root keeps one flat `templates/` with `design_spec.<kind>.<id>.md` per kind. One `templates/` holds one active roster — Layout if present else Deck.

**Creation**: `workflows/create-template.md` dispatches one of create-brand / create-style / create-layout / create-deck (README.md:16). Validate with `svg_quality_checker.py --template-mode`; library scope registers with `register_template.py <id> --kind <kind>` (styles/README.md:32, layouts/README.md:53, decks/README.md:57). `template_preview_pptx.py` renders a review PPTX (on request; always for multiple Masters). Project scope = initialized `projects/<name>/` root, no registration.

**Install** (`P/workflows/stages/apply-template-workspace.md`): only after Stage 1 confirms an exact root (never for bare names or style descriptions, :7); one root per kind, all four may coexist (:27). Command `python3 scripts/apply_template.py <project> --root <ws> [--root ...]` (`--dry-run`) (:74). Library `templates/design_spec.md` installs as `design_spec.<kind>.<id>.md` with one `> **Installed from**: ...` line added under H1 (:56-60). Only the structural owner's SVGs are copied (Layout beats Deck) (:56,62). After install every role reads only `<project>/templates/`, `images/`, `icons/` (:79). Raw PPTX is not a workspace (:29).

**Consumption / combination** (apply-template-workspace.md:64-69, 87-96; styles/README.md:13-22):
- Identity: Brand > Deck > (Style fallbacks are candidates only).
- Structure: Layout > Deck > free design. Style never supplies structure.
- Application context: Deck only.
- Method/direction: Style.
- Style-only and Style+Brand → flat PPTX; Style+Layout/Deck → follows that owner (styles/README.md:7).
- Owned segment governs visual *weight*, not only values (a Style's whitespace tendency cannot demote a Brand's dominant colour, apply-template-workspace.md:96).
- Layout + Deck valid: Layout owns structure, Deck keeps the rest (:100). Duplicate kinds rejected.
- Strategist writes `- **Template Application**: <natural-language plan>` after design_spec §I (design_spec_reference.md:59).
- Page titling: authored §IX titles and Style titling rule beat a mode's title tendency (styles/README.md:20).

Chart/Table catalogs are **not** kinds; they are page-local Visualization references (README.md:48). "Structure" (qualitative diagrams) is a runtime Executor method with no catalog (VISUALIZATION_TEMPLATE_AUTHORING.md:14).

---

## 3. Every shipped template

### 3.1 Brands (21) — identity only, no page SVGs

All global-company brands: every colour `approx` from third-party compilations reviewed 2026-08-07 (except noted `fact`); typography `Arial, "Microsoft YaHei", sans-serif` title 600–700 / body 400 (proprietary faces deliberately not named/bundled); Logo `none / never`; Voice formal/neutral, emoji forbidden, spell-out-first-use; Icon Style stroke, `tabler-outline` suggested. Palette pattern = primary, accent, bg #FFFFFF, surface, border, muted-text.

| id | primary | look / intended use |
|---|---|---|
| accenture | #A100FF violet, accent #000000 | violet on black; tech transformation, delivery (accenture:4,25-26) |
| alibaba | #FF6A00 orange + black | commerce/cloud; simple-icons alibabacloud/alibabadotcom symbols available (alibaba:48) |
| anthropic | #D97757 coral (fact) + #191919 | Claude lockup/mark/wordmark SVGs bundled; tabler/lucide stroke |
| aws | #FF9900 orange + navy #252F3E | cloud architecture; simple-icons per-service symbols |
| bain | #EE3224 scarlet | see 3.1.1 |
| bcg | #147B58 forest green | see 3.1.1 |
| deloitte | #86BC25 green + black | see 3.1.1 |
| google | #4285F4 + #34A853/#FBBC05/#EA4335 (fact) | Segoe UI stack; wordmark + G logo SVG; emoji allowed |
| huawei | #CF0A2C red + near-black #232527 | restrained-accent principle; ICT/gov-enterprise |
| ibm | #0F62FE Carbon Blue 60 (fact), accent #002D9C | enterprise/hybrid cloud |
| jpmorgan | #117ACA + navy #004B87 | finance research; prefer tabular figures (jpmorgan:41) |
| mckinsey | #051C2C navy + #2251FF electric blue | see 3.1.1 |
| microsoft | #00A4EF + #F25022/#7FBA00/#FFB900 quadrants | M365/Azure; pick one quadrant per product |
| nvidia | #76B900 (fact) + #1A1A1A | AI/GPU decks; logo needs written approval (nvidia:48) |
| pwc | #DB4E18 + 4-tone warm spectrum | see 3.1.1 |
| tencent | #3458B0 + #1F3A78 | platform/cloud; no simple-icons symbol |
| xiaomi | #FF6900 + #1F1F1F | consumer launch; generous white |
| zcare-rescue | #081830 navy, #8890A0, #D8F04A fluoro, #E85D2B | 9 PNG lockups; YaHei/Arial Black/Arial; Chinese spec; rescue-team courseware (zcare-rescue:25-80) |
| 中国电信 | #004EA2 | logo.png; YaHei stacks + Arial data role (中国电信:25-40) |
| 中国电建 | #004EA1 + #C90A4F | 4 logos (group + 3 subsidiaries); filled/sturdy icons |
| 中汽研 | #004098 + #003B82 | large + header logo PNG; faint-watermark allowed (中汽研:56) |

#### 3.1.1 Consulting brands — detail (no SVG/images exist for any of them; look is fully described by the spec)

- **bain** (brands/bain/templates/design_spec.md): primary #EE3224 scarlet, accent #8C1B12 deep red "for chapter grounds and depth", bg #FFFFFF, surface #F5F5F5, border #DCDCDC, muted #5C5C5C (:25-30). Rule: red only for identity + decisive emphasis, never large fills behind body text, never reads as risk (:32). Voice: lead with the result, tie recommendation to effect (:57). Use cases: strategy, PE/diligence, performance improvement (:17).
- **mckinsey**: primary #051C2C deep navy, accent #2251FF electric blue, surface #F2F4F6, border #D9DEE3, muted #5A6872 (:25-30). Accent "genuinely rare: marks the answer, the decisive figure, or the recommendation" (:32). Voice answer-first (:57).
- **bcg**: primary #147B58 forest green (PMS 341 C), accent #0A3D2C deeper green, warm surface #F4F6F4, border #D8DED9, muted #5B6660 (:25-30). Green as grounding colour, not highlighter; beware green-primary vs green "positive" status (:32).
- **accenture**: primary #A100FF violet (PMS 2592 C), accent #000000, surface #F5F3F7 (:25-30). Violet off large fills/body text; black carries type weight; violet marks single decisive element (:32). simple-icons/accenture symbol exists, never fabricate a lockup (:48).
- **deloitte**: primary #86BC25 (PMS 368), accent #000000, surface #F5F6F5, muted #63666A (:25-30). Never body text in green; never green dot beside wordmark (:32,48).
- **pwc**: primary #DB4E18, accent #E88D14, accent-warm #F3BE26, accent-rose #E669A2, accent-deep #AD1B02, surface #F6F5F4 (:25-33). Pick one tone per deck, never all five rainbow; overlaps warning range (:35).
- Shared: every value approx, may not be represented to a client as the firm's spec; never imply affiliation (bain:32,48 etc.).

### 3.2 Styles (14) — method + visual defaults, one file each

| id | Preferred mode | Visual style | Image rendering | Use |
|---|---|---|---|---|
| academic-research | custom (instructional+pyramid) | swiss-minimal | flat | thesis/conference |
| consulting-decision | pyramid | swiss-minimal | minimalist-swiss | decision docs, see below |
| creative-pitch | showcase | photo-editorial | editorial | agency/campaign pitch |
| duty-manual | custom (instructional+pyramid) | custom: swiss-minimal+blueprint+dark-tech, dark field, left-edge section indicator bar; fallback palette #0E1B2E/#4A9FD8/#D8F04A/#E85D2B (duty-manual:56-85) | custom line drawing | technical manuals/training (Chinese origin, Z-CARE) |
| incident-postmortem | briefing | swiss-minimal; severity palette Normal/Degraded/Critical/Recovered (:61-71) | digital-dashboard | outage reviews |
| investor-pitch | narrative | dark-tech | corporate-photo | fundraising |
| **mbb-consulting** | pyramid | custom (swiss-minimal ref) | minimalist-swiss | see below |
| narrative-keynote | narrative | editorial | editorial | keynotes |
| operating-review | custom (briefing+pyramid) | data-journalism; status palette On plan/Watch/Off plan/Focus (:62-72) | digital-dashboard | QBR/MBR |
| product-launch | showcase | photo-editorial | corporate-photo | launches |
| science-explainer | instructional | paper-cut | vector-illustration | public lectures |
| solution-proposal | pyramid | soft-rounded | corporate-photo | presales/bids |
| technical-deepdive | instructional | blueprint; dark palette #0F1C2B/#4A7BA7/#4FC9E8/#E8A54F (:60-69) | 3d-isometric | architecture reviews |
| workshop-teaching | instructional | sketch-notes | sketch-notes | training |

**mbb-consulting** (styles/mbb-consulting/templates/design_spec.md) — the most relevant shipped asset for a consulting whitepaper Skill:
- Summary: "answer-first argument at document density with numbered exhibits, a key-message column, footnotes, and action titles on every page" (:4). Derived from consulting-decision, conventions from example `ppt169_ev_market_priorities` (:19).
- Method: trace `overall answer → key support → page message → evidence`; one governing question per page, assertion title; facts/assumptions/implications/recommendations distinct (:24-26).
- 11 page roles with composition tendencies (:32-42): Executive synthesis (numbered findings + inference panel + basis-numbers strip + **dark decision-ask column at right**), Recommendation (priority table with tier + evidence-page column, totals strip, tier-meaning block), SCR, Driver decomposition, Current-state diagnosis (**two numbered exhibits side by side + third panel beneath + key-message column ending in implication panel**), Comparison, Process, Roadmap (stage chevrons, outputs row, tier lanes, decision-gate box with dated thresholds), Risk (register table + monitoring column + implication panel + reference strip), Decision request (ask/action/owner/consequence columns over milestone strip + review-date line), Appendix.
- Charts: exhibits A/B/C with solid badge, bold title, unit line; direct labels; deltas at bar ends; **no gridlines or value axes**; accent marks the point; footnote calculations (:47).
- Sources: numbered footnotes bottom-left + source line (:49).
- Fixed chrome (:56): two-line action title top-left + hairline, unit/exhibit-index line, section tracker + draft marker top-right, footnotes bottom-left, page number bottom-right; cover is the only dark full-bleed; all else white, hairlines, **no cards, no shadows**.
- Composition: 5–7 modules per content page (:57). Density at 1280 px: action title ~24, body/key messages ~14, exhibit titles ~13, labels 11–12, footnotes 10; exhibits ~1/3 page height; table rows 18–22 px (:58).
- Decoration: hairlines + solid badges only; implication panels light grey with thin left accent bar (:59).
- Colour behaviour + Fallback scheme (:60-76): Field #FFFFFF, Dominant #051C2C, Accent #2251FF, Accent tint #8FB8FF, Body #333333, Muted #7F7F7F, Hairline #B7B7B7, Grid #E3E3E3, Surface #F7F7F7, Negative #B3261E. (= McKinsey navy/blue.) Any Brand/Deck replaces it.
- Fallback type: Microsoft YaHei / Arial titles+body; Arial numerals (:80-83).
- Review focus includes "five to seven modules" check (:101).

**consulting-decision**: same method, but looser visuals — 1–3 primary regions, synthesis pages breathe, flat planes + hairlines, no fallback palette (styles/consulting-decision/templates/design_spec.md:53-58).

### 3.3 Layouts (7) — structure only, neutral preview paint

| id | canvas | pages | notes |
|---|---|---:|---|
| presentation_core | 16:9 1280×720 | 20 | general; fidelity; 64 px safe frame; typed picture/chart/table slots; incl. kpi_dashboard, process_timeline, data_story, chart_insight, table_summary (presentation_core:72-103) |
| presentation_core_43 | 4:3 1024×768 | 16 | projector/classroom; stacked_split, 2×2 kpi_grid |
| **report_core** | 16:9 | 13 | **2 Masters** (content light plane with header hairline y64 / footer hairline y664; divider inverted plane); real `slide-number`/`footer`/`date` placeholders; 48 px margins, 28 px title; body density ladder 20/19/18/15, chrome 12; agenda with Layout-owned 01–05 indices; matrix_2x2 with axis slots; appendix no container; "rules before containers" (report_core:57-86) |
| editorial_bleed | 16:9 | 10 | full-bleed images, gradient scrims (must be Slide-local, never solid rect) (editorial_bleed:50-57) |
| moments_square | 1:1 1080 | 8 | social square |
| story_vertical | 9:16 1080×1920 | 9 | phone story safe zones y120–1740 |
| xiaohongshu_post | 3:4 1242×1660 | 10 | single column, never split |

Report_core's prototype SVG carries `data-pptx-master`, `-layout`, `-layer="master"`, `-placeholder="title|body|footer|slide-number"`, `-idx`, `-bounds`, `-carrier`, `-editable` (layouts/report_core/templates/04_title_content.svg).

### 3.4 Decks (2)

- **中国电信** (decks/中国电信): fidelity, 5 pages (cover/toc/chapter/content/ending), 2 Masters (Brand / Content); white ground, telecom red #C00000 capsule + silver band header, grey rounded panels, skyline line art, bottom ribbon; 6 PNG assets (:31-81).
- **中汽研**: fidelity, 5 pages, Masters CATARC Dark / Light; deep blue #004098, square chapter-number header, grid + faint circles on dark pages (:31-77).
These are the only examples of a "purchased-template-like" Deck workspace; Create Deck with `mirror`/`fidelity` produces the same shape.

---

## 4. design_spec_reference.md and spec_lock_reference.md

### 4.1 design_spec.md (project-level, human-readable)

- First line exactly `<!-- ppt-master-schema: design-spec/v1 -->`, then `# <Project> - Design Spec` (:9). Written once, complete; never scaffold-patched (:9). Linted by `schemas/design_spec.schema.json` (:3).
- Depth `brief` (default) vs `complete` (:7); `complete` forced by split mode, `refine_spec: true`, preservation profiles.
- **§I Project Information** table (:23-46): Project Name, Canvas Format, Page Count, Primary Language (BCP-47), Target Audience, Communication Intent, Desired Audience Outcome, Core Message/Ask/Action, Delivery Context, Artifact Afterlife, Reading Mode, Content Strategy, Design Style, AI Image Acquisition Path, Generation Mode, Spec Refinement, Speaker Notes, Custom Animations, Narration Audio (each with provenance), Created Date. + optional `- **Template Application**:` line (:59).
- **§II Canvas**: Format, Dimensions, viewBox, Margins, Content Area (:48-56).
- **§III Visual Theme**: Theme Style (Mode, Visual style, Theme, Tone; + Mode/Visual Style References/Behavior when custom) and Color Scheme rows Background, Secondary background, Primary, Accent, Secondary accent, Body text, Secondary text, Divider (:64-84). Conditional `### AI Image Strategy` (Image Rendering, Visual, Mood) when any §VIII row is `ai` (:129-139).
- **§IV Typography**: Font Plan table (Role, Character, Primary, English-if-non-English, Fallback tail) for Title/Body + extra recurring roles (Display, Annotation, Footer, Footnote, Data, Emphasis, Quote, Code, Index …); `Typography upgrade (Reference)`; Title/Body/<Role> stacks; Font Size Hierarchy anchors Body/Title/Subtitle/Annotation (:86-127).
- **§V Layout Principles**: Hierarchy direction, Composition tendency, Cross-page continuity, Spacing posture, **Spacing anchors** (5 px values: page margin, block gap, column gutter, corner radius, body leading) (:108-116).
- **§VI Icon Usage**: Primary bundled library (one of 4 or none), Brand-logo library (simple-icons), table Icon Path / Suitable Scenarios; Stroke Width only for stroke lib (:118-127).
- **§VII Visualization Reference List** (conditional): Page | Family | Template | Usage; ≤1 chart|table per page (:144-155).
- **§VIII Image Resource List**: Filename, Dimensions, Ratio, Purpose, Type (`Source`, `Illustration Sheet`…), Image pattern, Crop Policy (adaptive/no-crop), Acquire Via (ai/web/user/placeholder/slice), Status (Pending/Needs-Manual…), Reference, text_policy, page_role (:149-157).
- **§IX Content Outline**: per slide `#### Slide NN - name`: Audience move, **Relationships** (semantic units + order/link/parent/contrast; no shapes), Composition (Reference), Title, Core message, Content, Mathematical content (:163-176). Optional lines: Visualization (kebab keys) + `Native-ready` map `<key>=yes|no`, Images, Motion suggestion (incl. Morph candidate), Hyperlinks (`#slide-N` / URI), Fact IDs, `Data class: scenario`, Cover impact, Closing impact (:155,190). Any field can be suffixed **`(binding)`** so Executor follows it literally (:190).
- **§X Speaker Notes**: Generation, Filename, Content, Total duration, Notes style, Presentation purpose; "preserve verbatim" for given scripts → `notes/total.md` (:179-188).
- Validation: `python3 scripts/project_manager.py validate <project>` (:196).

### 4.2 spec_lock.md (execution lock)

- First line `<!-- ppt-master-schema: spec-lock/v1 -->`, `# Execution Lock`; only `##` sections and `- key: value` lines (:7-9).
- Base sections (:15-26): `canvas` (viewBox, format), `communication` (primary_language, audience, objective, core_message, optional consumption_mode), `mode`, `visual_style`, `colors` (semantic roles incl. secondary_text, divider; image_rendering only for AI images), `typography` (font_family, title_family, body_family, body, title + `<role>_family`, `<role>` sizes), `icons` (library, inventory, stroke_width), `page_rhythm` (`P01: anchor|dense|breathing`), `pptx_structure` (mode flat|structured), `forbidden`.
- `forbidden`: two baseline rows (no mask/`<style>`/class/foreignObject/textPath/@font-face/animate/script/iframe; no HTML entities) + only verbatim user prohibitions tagged `(user)` (:26-37).
- Conditional (:43-52): custom mode → `mode_behavior`(+refs); custom visual_style → `visual_style_behavior`; custom image_rendering → behavior; tabler-outline → stroke_width 1.5/2/3; structured → `template_reuse_scope: layout|mirror`, `template_adherence`, `pptx_masters`, `pptx_layouts` (`key: master | name | template:<svg>`), `page_pptx_layouts`, `page_layouts`; mirror → structured+strict; `style` scope → flat.
- Optional data: `images` (`- p04: images/a.png | source=user | crop=no-crop`), `page_visualizations` (`P03: chart/line_chart`); legacy `page_charts` read-only (:28,85-89).
- Anchor semantics: page-local tints/gradients need no row; a value becomes a lock role when recurring or a display size hits 3rd occurrence (:107).
- Schema `schemas/spec_lock.schema.json` properties: canvas, communication, mode, visual_style, colors, typography, icons, images, page_rhythm, pptx_structure, pptx_masters, pptx_layouts, page_pptx_layouts, page_layouts, page_visualizations, page_charts, forbidden.

### 4.3 Scaffolds
`scaffolds/design_spec.md`, `scaffolds/spec_lock.md` = `{{PLACEHOLDER}}` + `[fill]` skeletons used only by `project_manager.py scaffold-spec` / `scaffold-lock` troubleshooting (design_spec_reference.md:9; spec_lock_reference.md:7). Note they lag the reference: scaffold has only 4 colour rows, no Primary Language, no Relationships line, no Spacing anchors, no §VII (scaffolds/design_spec.md:8-110).

---

## 5. Charts, tables, icons, sounds

### 5.1 Charts (33) — `chart/<key>`
By relationship (chart-vocabulary.md:14-75): time — line, area, stacked_area, dual_axis_line, stock, waterfall; category — column, horizontal_bar, grouped_bar, stacked_bar, butterfly, dumbbell, pareto; target — bullet, progress_bar, gauge; distribution — histogram, box_plot, scatter, bubble, heatmap, radar, matrix_2x2; part-whole — pie, donut, pie_of_pie, bar_of_pie, treemap, sunburst; flow — funnel, sankey, gantt, word_cloud.
- charts_index.json gives each a `Pick for … Skip if …` rule (e.g. column 3–8 categories; horizontal_bar 5–12 long labels; bullet 3–7 KPIs with target).
- 23 of 33 SVGs carry `data-pptx-replace-with="chart"` + JSON metadata → native editable PowerPoint charts when exporting with `--native-charts-and-tables`; not native-ready: bullet, butterfly, dumbbell, gantt, gauge, heatmap, matrix_2x2, progress_bar, sankey, word_cloud (always shapes).
- `<!-- chart-plot-area: x1,y1,x2,y2 -->` comment is a tool input; never delete (VISUALIZATION_TEMPLATE_AUTHORING.md:265-271).
- Use: Strategist lists in design_spec §VII, lock `page_visualizations`; resolve with `scripts/visualization_recall.py validate chart/<key>`; Executor reads only the selected SVG and re-skins it (charts/README.md:24-32,57-63). Native output is a separate opt-in: §IX `Native-ready` + `--native-charts-and-tables` flag.
- matrix_2x2 is a value chart (bubble positions); a qualitative 2×2 of text boxes is a runtime Structure (charts/README.md:49-53).

### 5.2 Tables (6) — `table/<key>`
record_table, metric_table, comparison_matrix, feature_matrix, rating_matrix (Harvey balls), hierarchical_table (tables/README.md:47-54). Native marker on record_table and hierarchical_table only; graphical cells stay shapes (:41-45). Legacy aliases: basic_table, consulting_table→metric_table, comparison_table, feature_matrix_table, harvey_balls_table, financial_statement_table, project_schedule_table→gantt (VISUALIZATION_TEMPLATE_AUTHORING.md:385-393).

### 5.3 Icons (12,027)
Five libraries (icons/README.md:5-11): chunk-filled (heavy 16px), tabler-filled, tabler-outline (stroke 2, best on screen), phosphor-duotone, simple-icons (3,675 real brand logos). One primary stylistic library per deck; simple-icons extra for real brands only. Copy to project with `python3 scripts/icon_sync.py <project> tabler-outline/home ...` (mixing stylistic libs in one batch fails) (:17-21). Use `<use data-icon="lib/name" x y width height fill/>`; `finalize_svg.py` embeds (:25-31). Search by drawable object (`bulb` not `idea`); names differ across libs (:42). Custom icons: drop SVG in `<project>/icons/<lib>/`.

### 5.4 Sounds (186 CC0 WAV)
Only for post-motion pass (animations.md §2.2), never a template resource (README.md:56). Namespaces kenney-interface 100, kenney-ui 51, bigsoundbank 35; 11 cue groups (transition 28, reveal 17, notification 9, confirmation 7, error 8, question 4, navigation 30, selection 8, interaction 18, state change 49, draw/gesture 8) (sound-vocabulary.md). Copy with `scripts/sound_sync.py <project> bigsoundbank/1797 ...`; `sound_sync.py list --query transition` (sounds/README.md:24,51).

### 5.5 Maintainer authoring contract
VISUALIZATION_TEMPLATE_AUTHORING.md: neutral palette (#0F172A, #475569, #64748B, #CBD5E1, accent #2563EB, pos #059669, neg #E11D48, warn #D97706) is preview-only (:115-124); font ≥ 12 (:200); every direct root `<g>` needs `data-pptx-bounds` (:224); Shape-first ladder rect/line → bentConnector/curvedConnector → `shape_boolean_svg.py` Merge Shapes → path (:248-255); no Master/Layout markers in catalog SVGs (:20).

---

## 6. Easy-to-miss features

1. **Bain, McKinsey, BCG, Accenture, Deloitte, PwC brand workspaces exist** (plus 15 others) — but colour/type/voice only; no logos, no page SVGs; fonts default Arial/YaHei (brands/*/templates/design_spec.md).
2. **`styles/mbb-consulting`** already encodes an MBB document-density page system (exhibit badges, key-message column, implication panel, footnotes, 5–7 modules, no cards/shadows, density px values) — directly comparable to a hand-built consulting whitepaper rule set (styles/mbb-consulting:32-83).
3. Styles carry **fallback palettes/typography** that are overridden wholesale by any Brand/Deck; Style + Brand = flat PPTX, no Masters (styles/README.md:7,13-22).
4. **report_core** layout gives real PowerPoint page-number/footer/date placeholders, two Masters and header/footer hairlines — a ready report chrome that can combine with a Brand or Style (report_core:57-63).
5. Layout + Deck can be combined: Layout replaces only Deck's structure (README.md:40; apply-template-workspace.md:100).
6. **Native editable charts/tables** require two opt-ins: `Native-ready` in §IX and export flag `--native-charts-and-tables`; typed chart/table slots in layouts force that flag (layouts/README.md:49; charts/README.md:57-63).
7. Template-owned chart JSON with `data-pptx-native-authority="json"` is authoritative; never re-derive from preview (apply-template-workspace.md:81).
8. **`(binding)`** suffix on any §IX field makes Executor follow it literally (design_spec_reference.md:190).
9. `forbidden` in spec_lock accepts only verbatim user sentences tagged `(user)`; Strategist-drafted rules go to `visual_style_behavior` (spec_lock_reference.md:26,37).
10. §V `Spacing anchors` (5 deck-wide px values) and per-role font families (`Display`, `Data`, `Footnote`…) are first-class lock anchors (design_spec_reference.md:116,127; spec_lock_reference.md:74).
11. Hyperlinks, Fact IDs, `Data class: scenario`, Motion/Morph candidates, LaTeX `Mathematical content` are §IX slide fields (design_spec_reference.md:190).
12. `simple-icons` has 3,675 real brand logos (incl. accenture, ibm, nvidia, aws services) usable for partner/tech-stack listings (icons/README.md:11).
13. Project-scope templates (no library registration) are supported: `design_spec.<kind>.<id>.md` in project `templates/` (README.md:40; layouts/README.md:53).
14. `template_preview_pptx.py` renders a workspace preview PPTX into `exports/` for review (layouts/README.md:53).
15. A Style may not contain any identity or structure field; `register_template.py` rejects violations (styles/README.md:28; brands/README.md:25).
16. Chart index summaries give quantitative selection thresholds (charts_index.json); gauge was re-scoped to a single KPI 2026-08-10 (VISUALIZATION_TEMPLATE_AUTHORING.md:365).
17. Selecting a brand/style by description never activates it; only an exact index id/root does (styles/README.md:11; apply-template-workspace.md:7).
18. Scaffold files are stale relative to the references; do not use them as authoring models (§4.3).
