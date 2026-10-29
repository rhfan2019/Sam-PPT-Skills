# ppt-master v6.7.2 — Capability Map, Slice A: SKILL.md + workflows/

P = `C:/Users/fanrh/.claude/plugins/cache/ppt-master/ppt-master/cc8b722a24e9-32c1cf49/ppt-master`. All paths below relative to P. Citations `file:line`. Abbrev: GP = workflows/generate-pptx.md, QG = workflows/profiles/quick-generate.md, CT = workflows/create-template.md, EN = workflows/edit-native-pptx.md, RT = workflows/routing.md, BP = profiles/beautify-pptx.md, IP = profiles/image-to-pptx.md, ATW = stages/apply-template-workspace.md, FR = governance/failure-recovery.md.

---

## 1. Inventory (24 files, 3017 lines, every file read start to end)

| File | Lines |
|---|---|
| SKILL.md | 143 |
| workflows/routing.md | 116 |
| workflows/index.md | 46 |
| workflows/generate-pptx.md | 378 |
| workflows/create-template.md | 384 |
| workflows/edit-native-pptx.md | 175 |
| workflows/profiles/quick-generate.md | 250 |
| workflows/profiles/beautify-pptx.md | 162 |
| workflows/profiles/image-to-pptx.md | 129 |
| workflows/stages/apply-template-workspace.md | 114 |
| workflows/stages/customize-animations.md | 123 |
| workflows/stages/generate-audio.md | 125 |
| workflows/stages/live-preview.md | 41 |
| workflows/stages/refine-spec.md | 54 |
| workflows/stages/resume-execute.md | 55 |
| workflows/stages/topic-research.md | 105 |
| workflows/stages/verify-charts.md | 87 |
| workflows/stages/visual-review.md | 78 |
| workflows/stages/web-image-review.md | 53 |
| workflows/governance/failure-recovery.md | 88 |
| workflows/create-template/create-brand.md | 94 |
| workflows/create-template/create-style.md | 97 |
| workflows/create-template/create-layout.md | 57 |
| workflows/create-template/create-deck.md | 63 |

---

## 2. Routes and profiles

### 2.0 Entry (SKILL.md)
- Mandatory load order: read SKILL.md → run `python3 "${SKILL_DIR}/scripts/attribution_guard.py"` (non-zero = stop, never bypass; Windows: retry with `python` on 9009) → read routing.md → select exactly ONE route + profile → read only that authority (SKILL.md:32-42).
- Route→authority table (SKILL.md:44-51). Never load another route's procedure; Image-to-PPTX and Beautify mutually exclusive (SKILL.md:53-57).
- Global discipline: serial; ⛔ BLOCKING = wait for user; no cross-gate bundling; no speculative later-phase artifacts; deterministic routing (no route menus); repair at owning layer, never silently downgrade (SKILL.md:112-120).
- Role-switch banner required before each role change (SKILL.md:127-133). design_spec.md headings stay English (SKILL.md:126).
- Phase frame (Plan vs Do·Check·Act) per route: Default Plan=Steps1-5, Quick §2, Edit Native §1-4, Create Template Steps 1-3 (SKILL.md:100-110).
- "Authored Expression Range" — what a page CAN carry: inline emphasis, lead-in, kicker, pull quote, hero number, takeaway line; 187 Office presets, Boolean merge, connectors, freeform; full-bleed/shaped images, scrim, spotlight, cross-page continuity; gradients, alpha, native shadow/glow, halftone; one cross-page motif (SKILL.md:61-70).
- Vocabulary (Relationships, Topology decision, pptx_structure.mode flat/structured, Composition, Device, Carrier, Page job, Page field, Geometry signature, Module line, mode senses) (SKILL.md:74-98).
- Sponsors only on explicit request (SKILL.md:143).

### 2.1 Routing (routing.md)
Three top-level routes: Generate PPTX, Create Template, Edit Native PPTX (RT:29-33). Profiles/stages are not routes (RT:18, 61-63).

| Condition | Effect | Source |
|---|---|---|
| Raster page frames → reconstruct | image-to-pptx (always Quick, Codex) | RT:41 |
| Existing PPTX, keep wording/count/order 1:1 | beautify-pptx (Quick only on explicit Quick intent) | RT:42 |
| Recorded/self-running/video delivery | load references/video-design.md (not a profile) | RT:43 |
| Explicit quick/fast/skip-strategy/direct SVG→PPTX | quick-generate directly, never loads GP | RT:44 |
| Topic only or factual gaps | topic-research | RT:45 |
| PPTX redesign (split/merge/re-outline) | Generate with PPTX as source; Default unless explicit Quick | RT:46 |
| PPTX pages drop/reorder/repeat w/o redesign | Edit Native (page_plan.json) | RT:47 |
| Default reaches planning | Step3 candidates → Stage1 confirms contract + template choice → apply-template-workspace only for non-free | RT:48 |
| Explicit workspace root | Default: Stage-1 candidate; Quick: validate+install directly; `library` label only if exact index match else `explicit`; consume root, never only `templates/` | RT:49 |
| Split-mode fresh chat | resume-execute | RT:50 |
| Deck-wide `colors.*` / `typography.font_family` change | `scripts/docs/update_spec.md` (update_spec.py) then final gate + Step 7 | RT:51 |
| Deck revision | GP Revision Round / QG §4 / EN §7 | RT:52 |
| Explicit spec refinement | refine-spec between Gate 1 and Gate 2 | RT:53 |
| Data charts exist | verify-charts before export | RT:54 |
| Explicit visual review request | visual-review | RT:55 |
| Preview/annotation request | live-preview; explicit Quick+preview FALLS BACK TO DEFAULT | RT:56 |
| Deck-wide transitions/auto-advance only | references/animations.md exporter flags | RT:57 |
| animations.json exists / per-object request / §I Custom Animations on | customize-animations | RT:58 |
| Narration explicit or §I Narration Audio on | generate-audio (implies notes) | RT:59 |

- Quick may consume up to one Brand/Style/Layout/Deck each; Layout > Deck for structure; Brand/Style-only & free design stay flat; Layout/Deck → structured (RT:63).
- No in-place Master/Layout upgrade of an existing PPTX/SVG; use Create Template then Generate (RT:69, 78).
- Raw PPTX called "template" + new content → Edit Native unless reusable workspace explicitly requested (RT:74).
- Template discovery reads ONLY `templates/brands/brands_index.json`, `styles/styles_index.json`, `layouts/layouts_index.json`, `decks/decks_index.json`; never scans dirs; bare names never resolved to paths (RT:111-116).

### 2.2 Generate PPTX — Default (generate-pptx.md)
Pipeline: Materials → [Research] → Create Project → Template Candidates → Stage-1 (communication + template) → [Template Install] → Stage-2 Solution → [Images] → Executor + Live Preview → Quality Check → Post-processing → Export (GP:11).

**Step 1 Source processing** (GP:32-49)
- `python3 ${SKILL_DIR}/scripts/source_to_md.py <file_or_URL_or_dir> [...]` for PDF/DOCX/XLSX/XLSM/PPTX/EPUB/HTML/LaTeX/RST/URL; `-t <type>`, `-o` only when needed (GP:38, 43). CSV/TSV read directly; wide datasets sliced via Python snippet (GP:39). Topic only → topic-research (GP:41). Sufficiency test (GP:45). EMF/WMF stay vector (GP:47). Image orientation review (GP:43).

**Step 2 Project init** (GP:53-68)
- `python3 ${SKILL_DIR}/scripts/project_manager.py init <project_name>` [+ `--format <registered>` only if fact-established] (GP:58, 62)
- `python3 ${SKILL_DIR}/scripts/project_manager.py import-sources <project_path> <sources...>` (`--move` optional) (GP:59)
- Artifacts: `validation/workflow.log` (+ `workflow_log.py <project_path> "<detail>"` for notes) (GP:64); PPTX intake `analysis/<stem>.identity.json`, `<stem>.slide_library.json`, `source_profile.json` (GP:66).

**Step 3 Template candidate preparation** (internal, no user stop; Quick skips) (GP:72-87)
- UI branch: embed `template_options` in `recommendations.stage1.json` (`schema_version:1`, `phase:"template"`, `lang`, `explicit_workspace_roots`, `default_mode` templates|free_design) (GP:82).

**Step 4 Strategist (MANDATORY in Default)** (GP:91-179)
- Load: `references/strategist.md`, `plan-core.md`, `canvas-formats.md` (GP:100-102); + `strategist-template.md` if template installed; + `video-design.md` if video delivery (GP:105-108).
- After Stage 1: planning-capability block: `strategist-image.md`, `modes/_index.md`, `visual-styles/_index.md`, `image-renderings/_index.md`, `templates/icons/README.md`, `templates/charts/chart-vocabulary.md`, `templates/tables/table-vocabulary.md` (GP:112-120).
- User images: `python3 ${SKILL_DIR}/scripts/analyze_images.py <project_path>/images` → `analysis/image_analysis.csv` (GP:126).
- ⛔ BLOCKING two-stage confirmation (GP:128): Stage 1 = communication contract + `free_design`|`templates` (four kind selectors). Stage 2 = complete deck solution (THREE candidate solutions, GP:142) + production mechanics. `refine_spec: true` adds a gate.
- UI commands: `python3 ${SKILL_DIR}/scripts/confirm_ui/server.py <project_path> --daemon`; `... --wait-only --wait-stage stage1`; `... --wait-only`; `... --shutdown` (always) (GP:135-150). Receipts: `template_selection.json`, `result.json` (server-written), `template_install.json` (installer) (GP:132). Stage-1 exit 0 is intermediate — continue (GP:139).
- Chat branch alternative (GP:154); delegation lets agent decide but never fabricate receipts (GP:130).
- ⛔ GATE Design Spec → review → lock (GP:156-162): read `templates/design_spec_reference.md`, write complete I–X `design_spec.md` at `design_spec_depth`; Gate 1 audit vs confirmation; optional refine-spec; read `templates/spec_lock_reference.md`, write `spec_lock.md`; `python3 ${SKILL_DIR}/scripts/project_manager.py validate <project_path>` (Gate 2).
- Confirmation notes: split-mode note (heavy runs), spec-refinement offer (always shown, default OFF) (GP:164-169).
- Production fields: Speaker Notes default true, Custom Animations false, Narration Audio false; stored in design_spec §I with provenance, never in lock (GP:171).
- Formulas (LaTeX) and hyperlinks are §IX content (GP:173). Prepared final narration → `notes/total.md` (GP:175).
- Output: `design_spec.md`, `spec_lock.md`, `notes/total.md` (narration branch) (GP:177). Every §IX needs `Audience move` (GP:179).

**Step 5 Image acquisition (conditional)** (GP:183-216)
- Trigger: §VIII row `Acquire Via: ai|web|slice` or derived row (GP:187). Read `references/image-base.md` always (GP:190).
- Derivatives: `scripts/image_treat.py` (blur, grayscale, duotone, brightness, contrast, `--fit WxH`) (GP:195).
- ai: `images/image_prompts.json` → `image_gen.py --render-md images/image_prompts.json`; Path A `image_gen.py --manifest`; Path B host-native; `manual` stops (GP:196).
- web: `scripts/image_search.py`, ≥2 rows → `images/image_queries.json` + `--batch`; with vision `--save-candidates` + web-image-review + `--promote` (GP:197, 203).
- slice: `slice_images.py <sheet>.png --grid RxC --names ... --trim --alpha --bg KEY_HEX --strict-alpha` (GP:198).
- 🚧 Exhausted-automation GATE (AI): ask repair/manual/cancel (GP:205). Rerun analyze_images.py after (GP:207).
- Split mode: prints "Planning Session Complete" and stops (GP:209-216).

**Step 6 Executor** (GP:220-316)
- Load core: `executor-base.md`, `shared-standards-core.md`, `semantic-svg.md`, `preset-shape-vocabulary.md`, `modes/<id>.md`, `visual-styles/<id>.md` + triggered modules from executor-base routing table (GP:225-233).
- Context rules incl. **Five-page lock re-read** after P05/P10/P15… (GP:243).
- Exact roster = §IX; no add/drop/merge/split while drawing (GP:247).
- **Design Parameter Confirmation (Mandatory)** output before P01 incl. calibration: `python3 ${SKILL_DIR}/scripts/text_measure.py calibrate <project_path> --outline` → `validation/text_calibration.json` (GP:251).
- **Live preview auto-start (Mandatory)**: `python3 ${SKILL_DIR}/scripts/svg_editor/server.py <project_path> --live --daemon` (port 6060+, `--port N`), URL in `live_preview/lock.json` (GP:253-259).
- Cadence: P01–P05 → early gate (skip if ≤6 pages) → rest → final gate (GP:261).
- Structure: `mirror`/`layout` start from `page_layouts` SVG and preserve slots; `style`/free/brand-only flat (GP:265-268).
- Early gate: `python3 ${SKILL_DIR}/scripts/svg_quality_checker.py <project_path> --canonical-authoring --stage early --json` → `validation/svg_quality_early_report.json`; emit `gate-signal:` line; method-level bias rules (GP:272-291).
- Final gate (Mandatory): `... --canonical-authoring --stage final --json` → `validation/svg_quality_report.json` (export refuses without it) (GP:293-304).
- Mandatory final carrier-receipt review (GP:306).
- Notes (if enabled): `references/executor-notes.md` → `notes/total.md` (GP:308).
- Conditional: verify-charts; visual-review (opt-in only); customize-animations (GP:312-316).

**Step 7 Export** (GP:320-364) — strict serial.
- 🚧 Image readiness gate for Needs-Manual (GP:324).
- 7.1 `python3 ${SKILL_DIR}/scripts/total_md_split.py <project_path>` (notes on) (GP:331).
- 7.2 `python3 ${SKILL_DIR}/scripts/finalize_svg.py <project_path>` → `svg_final/` (GP:339).
- 7.3 `python3 ${SKILL_DIR}/scripts/svg_to_pptx.py <project_path>` [`--no-notes`] (GP:348-349). Flags: `--native-charts-and-tables` (explicit editable chart/table decision or structured chart/table slot), `--image-sizing display`, animations.md deck flags, `-a none`, `--no-animations`, `--conversion-trace <path>` (GP:351-360).
- Artifacts: `exports/<name>_<timestamp>.pptx`, `validation/<name>_<timestamp>.report.json` (passed / passed-with-warnings), optional `.trace.json`; read `[POSTFLIGHT]` receipt (GP:364).
- Revision Round (GP:366-368): edit SVG + §IX + notes; renumber everything on insert/drop; deck-wide colour/font via update_spec.py; rerun final gate, `animation_config.py validate`, 7.1/7.2/7.3.
- Completion checklist (GP:370-378).

### 2.3 Generate PPTX — Quick (quick-generate.md)
- Trigger: explicit quick/fast, skip strategy/confirmation, or "go to SVG and export"; page count never decides (QG:9).
- Removes: Strategist, Confirm UI, design_spec.md, spec_lock.md, confirmation payload, finalize_svg.py, resumability (QG:17-27). Keeps all capabilities (QG:31).
- Notes/animations/narration default OFF but agent may enable without asking (QG:33).
- Mandatory motion discovery table pre-P01 (QG:35-43); video delivery forces Custom Animations (QG:45).
- Sources same as Default (QG:51-59); topic-research (QG:53).
- Template branch: exact roots only, ≤1 per kind, run apply-template-workspace; canvas = user > Layout > Deck (QG:67-72).
- `python3 ${SKILL_DIR}/scripts/project_manager.py init <name> --quick-generate`; `import-sources` (QG:74-79).
- Installed templates: read every installed spec + every Layout/Deck SVG prototype before P01; apply §5 segment precedence (QG:91).
- **Template Application paragraph** frozen in context (which prototypes used/skipped/repeated/adapted; for `replication_mode: mirror` must state literal reuse vs redesign — Quick has no `template_reuse_scope`) (QG:93).
- Planning-capability batch (no strategist.md, no strategist-template.md) (QG:97-106).
- ONE whole solution, not three (QG:108).
- Pre-P01 resolution: beats/states, production outcomes, roster, reading mode (`presentation`/`balanced`/`text`), `lang` on root svg, typography, color roles, density (`anchor`/`dense`/`breathing`), Relationships, shape language + motif, resources (QG:110-120).
- Mandatory whole-roster rhythm check, cover/closing impact (plan-core §4) (QG:122).
- Chart/Table refs: `visualization_recall.py validate` (QG:130).
- Resource prep table; strict slice closure; no-AI replan on exhausted AI (QG:132-156).
- §3 authoring: same core as Default; topology decision per page; native formulas/hyperlinks; structure flat vs structured (QG:170-191).
- Typography calibration: `python3 ${SKILL_DIR}/scripts/text_measure.py calibrate <project_path> --role <name>:<family>:<size>` (repeatable, `--sample` for other scripts) (QG:193).
- Cadence: early gate after P05 if ≥7 pages (QG:197).
- §4 final: `python3 ${SKILL_DIR}/scripts/svg_quality_checker.py <project_path> --quick-generate --canonical-authoring --stage final --json` (QG:208). Carrier-receipt review (QG:214). Notes → `total_md_split.py` (QG:219).
- Export: `svg_to_pptx.py <project_path> --quick-generate --with-notes|--no-notes` [+ `--native-charts-and-tables`, `-o`] (QG:227-231).
- Revision after delivery: edit SVGs directly; colour swap by hand (update_spec.py needs a lock) (QG:235).

### 2.4 Beautify (beautify-pptx.md) — profile under Default or Quick
- Trigger: supplied .pptx + explicit beautify/re-layout, content kept (BP:9, 17). Text frozen verbatim, no added page numbers/footers, no Morph staging copies (BP:19). 1:1 page count; re-pagination → ordinary Generate (BP:23).
- `beautify_identity.py <source.pptx>` → canvas (BP:35); init (Default or `--quick-generate`) + import-sources (BP:38-40).
- Reads `analysis/<stem>.identity.json` (theme vs observed palette/fonts/sizes) (BP:49).
- Optional source-SVG reference: `pptx_to_svg.py ... -o analysis/source_svg_import`; `extract_svg_assets.py ... --icon-namespace imported ...`; optional reuse gate for logos/motifs into `icons/imported/` (BP:53-60).
- `beautify_inventory.py <slide_library.json> --images <image_manifest.json> -o analysis/beautify_inventory.json`; bounded reads `--summary`, `--page N`, `--with-geometry` (BP:62-70).
- Default: ⛔ BLOCKING recommend & confirm (identity source, preserve scope, ignored, needs_confirmation, verification level) + visual re-confirm via Confirm UI with seeded JSON; source-replica preselected, ≥3 candidates; body_size pt×4/3 rule (BP:88-133).
- Validate: `beautify_inventory.py <inventory> --verify <exports/output.pptx>` (BP:147).

### 2.5 Image to PPTX (image-to-pptx.md) — Quick only, Codex only
- Trigger: raster pages + explicit restore-as-PPTX (IP:9); Codex required (IP:11); never applies templates; flat output (IP:15, 31).
- 🚧 Normalized frame roster gate; contact sheets `slice_images.py --grid` (IP:37-49). Inspect every page (IP:51).
- Content families → native_text/source_graphic/native_chart/native_shape/image_layer/manual_required (IP:57-66). Minimum layer stack, registered groups, layer plates (IP:76-82).
- Artifact `analysis/reconstruction_inventory.json` (IP:88). Forbidden screenshot skin (IP:104). Final checks table (IP:106-117).

### 2.6 Create Template (create-template.md + 4 children)
Scope: `library` (default, `templates/<kind_dir>/<id>/`, `templates/design_spec.md`, registered) or `project` (`design_spec.<kind>.<id>.md`, unregistered) (CT:11-14).
Process (CT:43): Intake → Brief → ⛔ Confirmation (`[TEMPLATE_BRIEF_CONFIRMED]`) → Preflight + child → Validate → [Prototype Review: Layout/Deck] → [Review PPTX] → [Register] → Output.
- Step 1 intake types A (.pptx: `pptx_template_import.py "<ref.pptx>" -o "<import_ws>"`), B (SVG), C (images), D (text/doc/URL via source_to_md.py), E (nothing) (CT:54-60, 74, 123). Strategies `standard` / `fidelity` (A/B) / `mirror` (A only) derived by AI, never asked (CT:62-68).
- Optional `extract_svg_pictures.py ... --select "<group_id>" ...` complex-picture normalization (CT:76). `import-sources --no-image-propagation` (CT:85).
- Basic norm extraction (mandatory with reference) — canvas, identity, layout grammar, image system, density rhythm, roster semantics, asset policy, native structure (CT:89-104).
- Step 2 brief with labels `[fact]/[suggested]/[decision]/[derived]` (CT:140-188).
- Step 3 ⛔ MANDATORY gate; no template file written before marker (CT:46, 192-206).
- Step 4: Template_Designer for Layout/Deck; read `native-shape-authoring.md` + `preset-shape-vocabulary.md` for standard/fidelity (CT:228-230). Multi-Master rules (CT:250). Sprite-sheet preservation (CT:259). Mirror publication (CT:261-268). Placeholder frames are executable defaults (CT:272).
- Step 5 hard gate: `python3 skills/ppt-master/scripts/svg_quality_checker.py "<template_source>" --template-mode --canonical-authoring --format <canvas_format>` (CT:283); Brand/Style same without format + `register_template.py <id> --kind brand|style --dry-run` (CT:278).
- Step 5.1 Prototype Review Round (Layout/Deck; user reacts to roster) (CT:303-305).
- Step 6 review PPTX (requested, or required for multi-Master): `template_preview_pptx.py "<ws>"` [`--native-charts-and-tables -o ...`] [`--force`] → `exports/<id>_template_preview.pptx` (CT:309-331).
- Step 7 `register_template.py <id> --kind brand|style|deck|layout` (library); `--rebuild-all` (CT:339, 342).
- Step 8 output block; handoff root → Generate Step 3 (CT:346-373).
- Children: Brand = identity only, spec I–VII, no SVG (create-brand.md:11, 38-86); Style = method + defaults, spec I–VII incl. `## VII. Review Focus` with `<!-- visual-review-trigger: explicit-user-only -->`, no assets (create-style.md:11-13, 32-85); Layout = brand-neutral structure, no primary_color, `page_types` (create-layout.md:11, 23-47); Deck = application context + identity + structure, sections I–VII, `category`, `primary_color`, `page_count` (create-deck.md:11, 25-51).

### 2.7 Edit Native PPTX (edit-native-pptx.md)
- Use: fill raw PPTX template, rewrite some pages, drop/reorder/repeat, add notes/narration/transitions (EN:11-16). Never runs init/finalize/pptx_template_import (EN:18).
- 🚧 Inputs gate (EN:30). Import: `python3 skills/ppt-master/scripts/pptx_to_svg.py "<source.pptx>" -o "projects/<slug>_<YYYYMMDD>" --inheritance-mode both --roundtrip` (EN:39). Workspace layout `authoring-svg-flat/`, `authoring_summary.json`, notes, native-payloads (EN:42-50). Source proxies atomic (EN:52).
- Plan: `page_plan.json` (schema `ppt-master.roundtrip-page-plan.v1`) only when roster differs (EN:62-76); merge via `svg_authoring_view.py ... --adopt-object slide_05.svg:<id> --into <svg>` (EN:81).
- ⛔ BLOCKING plan confirmation (EN:99).
- After edit: `svg_authoring_view.py ... --refresh-summary`; `svg_quality_checker.py "<ws>" --roundtrip --json` (gate) (EN:125-129).
- Export: `svg_to_pptx.py "<ws>" --roundtrip` [+ `-t`, `--transition-duration`, `--recorded-narration audio --use-narration-timings`, `--animation-config`, `-a`, `--no-notes`, `--native-charts-and-tables`, `--primary-language`] → receipt passthrough/cloned_passthrough/patched/rebuilt (EN:148-157).
- Validate: `pptx_delivery_check.py`, `ppt_to_md.py` read-back (EN:161).

---

## 3. Capability table

| Capability | What it does | Trigger / opt-in | In → Out | Source |
|---|---|---|---|---|
| Attribution guard | Integrity gate | Always, first | — → exit code | SKILL.md:33 |
| Source conversion | Office/PDF/EPUB/HTML/LaTeX/URL → Markdown + profile | Auto when files supplied | files → `<stem>.md`, `*.conversion_profile.json` | GP:38-43 |
| Topic research | Fills factual gaps; isolated worker | Topic-only or gaps | brief → `projects/<slug>.md` + `.facts.json` (`ppt-master.fact-provenance.v1`) | topic-research.md:11-81 |
| Project init/import | Workspace + intake bundle | Always (not Edit Native) | sources → project, `analysis/*` | GP:58-66 |
| Workflow log | Cold audit | Auto; manual note via workflow_log.py | — → `validation/workflow.log` | GP:64 |
| Template candidates/indexes | Lists four kinds from indexes | Default Step 3 | indexes → `template_options` | GP:72-87, RT:114 |
| Confirm UI (2-stage) | Browser confirmation of contract + template + solution | Default (chat fallback) | recommendations.stage1/2.json → result.json, template_selection.json | GP:128-152 |
| Strategist planning | 3 candidate solutions, mode/visual style/rendering, §IX roster with Relationships/Composition/Audience move | Default only | sources → design_spec.md I–X | GP:91-179 |
| Spec lock | Execution anchors (colors, typography roles, page_rhythm, page_layouts, images) | Default only | design_spec → spec_lock.md | GP:161 |
| Refine spec | Review/edit full spec (page or chat) before lock | Explicit opt-in (`refine_spec: true`) | design_spec.md → revised | refine-spec.md:13-52 |
| Template install | Validates & installs Brand/Style/Layout/Deck roots | Non-free Stage 1 / Quick exact root | roots → `templates/design_spec.<kind>.<id>.md`, SVGs, images, icons | ATW:46-81 |
| Segment precedence | Identity Brand>Deck; structure Layout>Deck; direction Style; app ctx Deck | On install | specs → resolution in context | ATW:85-104 |
| update_spec | Deck-wide colors/font swap | On request (Default only) | spec_lock → updated | RT:51, GP:368 |
| User image analysis | CSV inventory of images | User images present | images/ → analysis/image_analysis.csv | GP:126 |
| AI images | Prompts + generation (API/host-native/manual) | §VIII ai rows | image_prompts.json → images | GP:196 |
| Web images | Search, candidate review, promote | §VIII web rows | image_queries.json → images + image_sources.json | GP:197, 203 |
| Web image review | Multimodal candidate selection | `--save-candidates` + vision | review_sheet.jpg → receipt table | web-image-review.md:11-53 |
| Slicing | Cut sheet into transparent elements | slice rows | sheet.png → named PNGs | GP:198 |
| Image treatment | blur/grayscale/duotone/etc. | derived rows | image → derivative | GP:195 |
| Split mode | Planning in one chat, execution in another | Heavy run / `generation_mode: split` | — → handoff | GP:168, 209-216 |
| Resume execute | Fresh chat continues Steps 6–7 | "继续生成 projects/<name>" | spec+lock → deck | resume-execute.md:13-55 |
| Text calibration | Per-role chars/100px table | Mandatory before P01 | lock/roles → validation/text_calibration.json | GP:251, QG:193 |
| Live preview editor | Browser SVG view, direct edits, annotations | Mandatory auto-start Default Step 6; Step 1 re-open on request | svg_output → lock.json URL | GP:253-259, live-preview.md |
| Annotation apply | Apply browser annotations, re-export | After export, user asks | annotations → SVG edits, annotations.jsonl | live-preview.md:33-41 |
| Early gate | Method-level check after P05 | Rosters ≥7 | SVGs → svg_quality_early_report.json | GP:272-291 |
| Final quality gate | Blocking checker; export fingerprint | Mandatory | SVGs → svg_quality_report.json | GP:293-304 |
| Carrier-receipt review | Compare drawn carriers vs page jobs | Mandatory | report → repairs | GP:306 |
| Verify charts | Recompute chart geometry with calculator | Any data chart | SVG → receipts | verify-charts.md |
| Visual review | Playwright render + subagent rubric fixes | EXPLICIT user request only | SVG → .preview/*.png, .review/ | visual-review.md:11-78 |
| Speaker notes | notes/total.md → per-slide | Default ON; Quick OFF | final SVG → notes/ | GP:308, 331 |
| Native formulas | LaTeX → native math | §IX content | LaTeX → OMML | GP:173, QG:176 |
| Native hyperlinks | `<a href>` incl. #slide-N | §IX content | — | GP:173 |
| Native charts/tables | Editable PowerPoint chart/table | `--native-charts-and-tables` (explicit decision or structured slot) | inline JSON → a:tbl/chart | GP:353, QG:231 |
| Custom animations | Per-slide/object motion, Morph, 48 transitions, 203 effects, sound | animations.json / explicit / §I on | SVG groups → animations.json | customize-animations.md |
| Deck-wide motion | `-a auto`, transitions flags | Deck-wide request | flags | RT:57 |
| Narration audio | TTS per slide (edge/ElevenLabs/MiniMax/Qwen/CosyVoice), SRT, embed, timings | Explicit / §I on | notes → audio/, narrated PPTX | generate-audio.md |
| Native video | PowerPoint MP4 export, sound mix, subtitles | Narration branch, Windows PPT 2016+ | narrated PPTX → MP4 | generate-audio.md:93-100 |
| Video motion plan | Renderer plan from trace | Downstream renderer | trace → video_motion_plan.json | customize-animations.md:111-113 |
| finalize_svg | Self-contained preview | Default 7.2 (Quick skips) | svg_output → svg_final | GP:339 |
| Export | Native PPTX + postflight | Always | svg_output → exports/*.pptx, report.json | GP:348-364 |
| Revision round | Post-delivery edits | User returns with change | — | GP:366-368, QG:235 |
| Beautify | 1:1 re-layout with frozen text | Explicit beautify | PPTX → new PPTX + verify | BP |
| Image to PPTX | Layered reconstruction | Raster pages, Codex | images → PPTX | IP |
| Create Brand/Style/Layout/Deck | Reusable workspaces | Template request | refs → workspace + index | CT, children |
| Template review PPTX | Preview prototypes in PowerPoint | Requested or multi-Master | workspace → exports/*_template_preview.pptx | CT:309-331 |
| Prototype review round | User reacts to prototypes | Layout/Deck, always | roster → revisions | CT:303-305 |
| Edit Native | Round-trip edit preserving native design | Keep-design requests | PPTX → workspace → PPTX | EN |
| Failure recovery | Recovery matrix + resume pointers | On failure | — | FR |

---

## 4. Default vs Quick vs other profiles

| Aspect | Default | Quick | Beautify | Image to PPTX |
|---|---|---|---|---|
| Strategist role (strategist.md) | YES | NO | Default: pre-resolved Strategist; Quick: none | NO |
| Template candidates (Step 3) / catalog selection | YES | NO (exact roots only) | as runtime | NO templates at all |
| Stage-1/Stage-2 confirmation (Confirm UI or chat) | ⛔ YES | NO | Default: ⛔ YES (seeded) | NO |
| Solution candidates | THREE (GP:142) | ONE (QG:108) | source-replica + ≥2 | n/a |
| design_spec.md / spec_lock.md | YES | NO (QG:25) | Default yes | NO |
| strategist-template.md (template-aware planning, `page_layouts`, `template_reuse_scope`) | YES | NO; replaced by frozen Template Application paragraph (QG:93) | — | — |
| refine-spec option | offered (opt-in) | n/a | — | — |
| Split mode / resume | YES | NO; context loss = restart (QG:199) | — | — |
| Five-page lock re-read | YES (GP:243) | NO (no lock); Beautify-Quick rereads inventory every ~5 pages (BP:139) | — | — |
| Design Parameter Confirmation output | YES (GP:251) | NO (calibrate with `--role`) | — | — |
| Live preview auto-start | Mandatory (GP:253) | Not in QG; explicit preview intent forces Default (RT:56) | — | — |
| Speaker notes default | ON | OFF (agent may enable) | — | — |
| Early gate | after P05 if roster ≥7 | same, with `--stage early` | — | — |
| Final checker | `--canonical-authoring --stage final --json` | + `--quick-generate` | — | — |
| finalize_svg.py | YES | NO | — | — |
| Export flag | none | `--quick-generate --with-notes|--no-notes` | — | — |
| AI image failure | blocks, ask 3 options | no-AI replan, continue | — | Codex native, block if Needs-Manual |
| update_spec.py for deck colour change | YES | NO (hand edit) | — | — |
| Video delivery | video-design.md; Custom Animations via §I | forced Custom Animations (QG:45) | — | — |
| Structure | from lock (`mirror`/`layout`/`style`) | inferred from SVG metadata | — | always flat |

---

## 5. Off-by-default / easy-to-miss features

1. **Strategist planning is Default-only**: three Stage-2 solutions, mode/visual-style/rendering catalogs, §IX per-page `Relationships`, `Composition`, `Audience move`, `page_rhythm` — all absent in Quick (GP:91-179, QG:17-25).
2. **strategist-template.md** (template-aware planning) loads only in Default after a template install (GP:107).
3. **refine-spec**: opt-in full spec review page (`spec_review/server.py --daemon`, `check_spec_annotations.py`) — default OFF; the offer line is always shown (GP:169, refine-spec.md:13, 31-42).
4. **visual-review**: explicit request only; Playwright; subagent batches K=5; iteration budget 2 opt-in; Style Review Focus only used here (visual-review.md:11, 49, 76-78; create-style.md:81-83).
5. **Five-page lock re-read** (GP:243).
6. **Early gate + gate-signal method-level bias** rule (GP:282-291).
7. **Text calibration** must run before P01 (GP:251; QG:193).
8. **Live preview** + **Annotate/Direct edit** + post-export `check_annotations.py` apply loop (live-preview.md).
9. **Split mode** & **resume-execute** for heavy decks (GP:168, resume-execute.md).
10. **Custom animations** (Morph, 48 transitions, 203 in-slide effects, sound pass) — off by default; Quick motion-discovery table (customize-animations.md:83-93; QG:35-43).
11. **Narration audio / MP4 / subtitles / sound mix** — off by default; consultant voice suggestions (generate-audio.md:38).
12. **Native editable charts/tables** require `--native-charts-and-tables` (GP:353); otherwise exported as shapes.
13. **verify-charts** calculator modes per chart key (verify-charts.md:27-36).
14. **update_spec.py** deck-wide colour/font substitution (RT:51).
15. **Revision Round** in place, no replanning (GP:366-368).
16. **Template creation sub-workflows**: Brand / Style / Layout / Deck; strategies standard / fidelity / mirror; Prototype Review Round; review PPTX; multi-Master (CT).
17. **Project-scope templates** (unregistered, coexisting kinds in one project) (CT:14).
18. **Web image review** with vision (web-image-review.md).
19. **Beautify** optional source-SVG reference + logo/motif reuse gate (BP:53-60).
20. **Edit Native** for filling a raw PPTX template while keeping native design (EN:13).
21. `--image-sizing display`, `--conversion-trace` export flags (GP:354, 360).
22. Prepared final narration script → `notes/total.md` before P01 (GP:175).
23. Delegation: user may explicitly delegate confirmation; agent decides but records (GP:130, CT:194).

---

## 6. Relevance to consulting-style decks from an installed Deck/Style template

- **Quick skips the whole planning layer** that makes consulting decks good: no Strategist, no 3-solution comparison, no §IX per-page `Relationships`/`Composition`/`Audience move`, no lock, no five-page re-read, no strategist-template.md (QG:17-25, 108; GP:107, 243). A wrapper that runs Quick must replicate these itself or switch to Default.
- **Default with a template**: pass the exact workspace root → Stage-1 candidate (template mode, preselected if sole root) → apply-template-workspace → strategist-template.md → Stage 2 → design_spec + spec_lock with `page_layouts` (GP:141-161; RT:49, 108-110). Structure `mirror`/`layout` reuse prototype slots; `style` locks flat (GP:265-268; refine-spec.md:46).
- **Style alone is flat**: Style owns method + defaults, no canvas/prototype/structure; Style-only and Style+Brand stay `flat`; Style+Layout/Deck follows that owner; Style never triggers visual review (ATW:64-69; RT:63; create-style.md:11).
- **Deck + Style together**: Deck owns structure (unless a Layout is also selected) and identity; Style owns direction/method; verify Style fits the structure or drop it; owner's dominance instructions bind (e.g., Style whitespace never demotes Brand/Deck dominant color) (ATW:87-96).
- **Quick + template**: must read every installed SVG prototype before P01 and freeze a Template Application paragraph; for `replication_mode: mirror` say explicitly literal reuse vs redesign (QG:91-93). Layout/Deck owner → every page is a full structured Slide SVG (Master/Layout/slots), all-or-none (QG:189).
- **Consulting-relevant expression devices**: kicker, lead-in, takeaway line, hero number, pull quote; 187 presets, connectors (SKILL.md:63-69); per-page topology decision for order/link/parent/membership/contrast/overlap (QG:178); chart/table vocabularies + `visualization_recall.py validate` (QG:130); native charts via flag (GP:353); verify-charts for numeric accuracy.
- **Mode/visual-style catalogs** (`references/modes/_index.md`, `visual-styles/_index.md`) are loaded in both runtimes; Default picks via Stage 2, Quick picks one directly (GP:114-115; QG:100-108). A Style spec can name `Preferred Mode` / `Preferred Visual Style` as seeds (create-style.md:53-66).
- **refine-spec** lets the user edit the §IX storyline before any SVG is drawn — the consulting "storyline review" checkpoint (refine-spec.md:9).
- **Reading mode** (`presentation`/`balanced`/`text`) and density tags (`anchor`/`dense`/`breathing`) drive body size; consulting reading-decks → `text` (QG:115-117).
- **Template creation from a purchased PPTX**: Create Template Type A, `pptx_template_import.py`; Deck kind when branded system; Style kind for portable method; `standard`/`fidelity`/`mirror` derived from intent; prototype review round + review PPTX (CT:54-68, 303-331). Install example path in docs: `skills/ppt-master/templates/brands/mckinsey/` (ATW:59, example only).
- **Alternative**: if the goal is to keep a purchased PPTX's native design and fill content, Edit Native PPTX (roster as slide library matched by rhetorical shape) is the intended route, not Generate (EN:13, 58; RT:74).
- **Consultant narration voices** recommended: zh-CN-YunjianNeural / XiaoxiaoNeural; en-US-GuyNeural / JennyNeural (generate-audio.md:38).
- **Visual QA**: static checker is mandatory; real rendered visual review exists but only when the user explicitly asks (GP:314).
