# E — ppt-master v6.7.2 `scripts/` capability map

P = `C:/Users/fanrh/.claude/plugins/cache/ppt-master/ppt-master/cc8b722a24e9-32c1cf49/ppt-master`. All paths below are relative to `P/scripts/`. Doc cites are `docs/<file>:line` (or `README.md:line`). Read-only survey; nothing was run except AST extraction of docstrings and argparse calls.

## 1. Inventory

### Docs read in full (7,247 lines)
| File | Lines | Topic |
|---|---:|---|
| README.md | 449 | Toolset index, high-frequency commands, template import, presets, export overview |
| docs/svg-pipeline.md | 1359 | Authoring IR, round-trip, finalize, **svg_to_pptx**, visual_review, text_measure, **checker**, position calculator |
| docs/svg-contract.md | 807 | Closed SVG grammar the checker and exporter enforce |
| docs/conversion.md | 710 | source_to_md backends, pptx_intake, pptx_to_svg, image orientation |
| docs/confirm_ui.md | 564 | Step-4 Confirm UI server + template selection sidecar |
| docs/image.md | 406 | image_gen, image_treat, analyze_images, image_search, watermark, latex_render |
| docs/advanced-image-motion-smoke.md | 390 | Maintainer smoke: crops + Morph + presets |
| docs/pptx-transitions.md | 327 | 48 transitions, options, Morph pairing, kiosk |
| docs/project.md | 323 | project_manager, workflow log, batch_validate, pptx_template_import |
| docs/multilingual-text-smoke.md | 311 | Maintainer smoke: language tags/RTL |
| docs/pptx-animations.md | 309 | 203 object animations, sidecar fields |
| docs/mask-gradient-smoke.md | 273 | Maintainer smoke: gradients/masks |
| docs/spec_review.md | 220 | design_spec.md browser review server |
| docs/template-tools.md | 142 | Create-template tools: import, mirror, template-mode, preview, apply, register |
| docs/video-motion-plan.md | 117 | Trace → video motion plan |
| docs/visualization-recall.md | 114 | Chart/table recall + validate |
| docs/narration.md | 91 | TTS, narration sync, video export/mix/subtitles |
| docs/troubleshooting.md | 87 | Common failures |
| docs/update_spec.md | 69 | Deck-wide color/font propagation |
| docs/prompt_audit.md | 68 | Maintainer prompt budget lint |
| docs/native-data.md | 45 | Native chart/table JSON payload grammar |
| docs/svg_editor.md | 40 | Live-preview editor server |
| docs/chart-recall.md | 26 | Legacy recall wrapper |

### Scripts enumerated (AST: docstring + argparse)
Top-level entry scripts (`[main]`): analyze_images, animation_config, apply_template, attribution_guard, batch_validate, beautify_identity, beautify_inventory, chart_recall, check_annotations, check_spec_annotations, compact_svg_coordinates, compact_svg_styles, config, error_helper, extract_svg_assets, extract_svg_pictures, finalize_svg, gemini_watermark_remover, generate_examples_index, icon_sync, image_gen, image_search, image_treat, latex_render, mirror_template_materialize, narration_sync, notes_to_audio, powerpoint_video, pptx_animations, pptx_delivery_check, pptx_intake, pptx_template_import, pptx_to_svg, preset_shape_svg, project_manager, project_utils, prompt_audit, register_template, rotate_images, shape_boolean_svg, slice_images, sound_sync, source_to_md, stamp_native_fallbacks, svg_authoring_view, svg_position_calculator, svg_quality_checker, svg_to_pptx, template_preview_pptx, text_measure, total_md_split, update_repo, update_spec, video_motion_plan, video_sound_mix, video_subtitles, visual_review, visualization_catalog (import-only despite main guard), visualization_recall, workflow_log.

Top-level library modules (no CLI): authoring_roundtrip (used by `svg_to_pptx --roundtrip`), console_encoding, hyperlink_contract, language_tags, native_payloads, page_context, pptx_effects, pptx_embedded_fonts, pptx_gradients, pptx_opc_validation, pptx_transitions (registry; its CLI is reached through `pptx_animations.py --describe-transition`), pptx_workspace, project_specs, resource_paths, semantic_table, server_common, slide_roster, svg_authoring_contract, svg_compatibility, template_text_slots, workflow_transcript.

Packages:
- `svg_quality/` (checker.py 10,278 lines, svg_contracts.py, slot_capacity.py, cli.py, xml_support.py): implementation behind `svg_quality_checker.py`.
- `svg_finalize/` (embed_icons, align_embed_images, crop_images, embed_images, fix_image_aspect, flatten_tspan, svg_rect_to_path): parts behind `finalize_svg.py`. Each file also has its own CLI.
- `svg_to_pptx/`: `pptx_package/cli.py` (the real CLI), builder.py (8,612 lines), template_structure.py, template_validation.py, narration.py, notes.py, media.py, dimensions.py, discovery.py, slide_xml.py; `drawingml/` (converter, elements, styles, paths, utils, text_properties, text_baseline, theme_colors, theme_fonts, hyperlinks, context); `native_objects/` (chart_*, chartex, table, workbook, formula_*, inline_formula, fallback_hash, marker_*); animation_config, canvas_contract, geometry_properties, semantic_markers, shape_boolean, text_outline, tspan_flattener, use_expander.
- `template_import/` (manifest.py, native_structure.py): used by pptx_template_import.
- `pptx_to_svg/` (25 modules: converter, slide_to_svg, shape_walker, txbody/pic/tbl/chart/chartex/fill/ln/effect/custgeom/prstgeom→svg, color_resolver, animation_import, transition_import, formula_import, notes_import, hyperlinks, normalized_chart_svg, preset_*): the importer.
- `source_to_md/` (pdf/doc/excel/ppt/web_to_md + _dispatcher, _batch, _conversion_profile).
- `svg_editor/` (server.py, annotations.py, static/): live preview editor.
- `spec_review/` (server.py, store.py, static/): Design Spec review.
- `confirm_ui/` (server.py 2,986 lines, static/ with catalogs.json and style_previews/).
- `image_backends/`: 15 providers (bfl, fal, gemini, ideogram, minimax, modelscope, openai, openrouter, qwen, replicate, siliconflow, stability, tencent, volcengine, zhipu) + backend_common.
- `image_sources/`: openverse, pexels, pixabay, wikimedia + provider_common.
- `tts_backends/`: edge, elevenlabs, minimax, qwen, cosyvoice + backend_common.
- `project_management/` (cli.py, page_context.py, project_specs.py, spec_blocks.py, paths.py).
- `pptx_shapes/`: 187-preset DrawingML registry, formula evaluator, semantics, semantic_hash.
- `pptx_ooxml/`: analyzer, chart_read, diagram_read, clone, package, ooxml, edit_safety, slideshow.
- `tests/`: about 50 test_*.py files (maintainer).
- Data: `pptx_animation_presets.json` (576 KB), `prompt_audit_manifest.json`, `assets/bg_48.png`, `assets/bg_96.png`.

## 2. Tool table

Workflow-step names follow the docs: Generate Step 4 = confirm, Step 6 = live preview, Step 7 = post-process/export; "stages/" are workflow stages.

| Script | Purpose | Key flags | Inputs → outputs | Workflow step | Doc |
|---|---|---|---|---|---|
| source_to_md.py | Auto-detect and dispatch any source to Markdown | `-t pdf/doc/excel/pptx/web/markdown/text`, `-o`, `--images all/filtered/none`, `--no-images`, `--filter-images`, `--render-vector-figures`, `--json` | files/URLs/dirs → `<stem>.md`, `<stem>_files/`, `image_manifest.json`, `.conversion_profile.json` | Source intake (Step 1) | conversion.md:40-95 |
| source_to_md/pdf_to_md.py | PyMuPDF PDF → MD (AGPL dependency) | `--images`, `--render-vector-figures`, `--vector-figure-dpi`, `-o` | pdf → md | Intake | conversion.md:97-130 |
| source_to_md/doc_to_md.py | docx/html/epub/ipynb natively, pandoc fallback for others; OMML → LaTeX | `-o` | doc → md | Intake | conversion.md:132-176 |
| source_to_md/excel_to_md.py | xlsx/xlsm → MD tables | `--max-rows`, `--max-cols`, `--include-hidden` | workbook → md | Intake | conversion.md:178-214 |
| source_to_md/ppt_to_md.py | PPTX text, tables, charts, SmartArt, notes, pictures → MD | `-o` | pptx → md + `_files/` | Intake | conversion.md:216-251 |
| source_to_md/web_to_md.py | Web → MD (curl_cffi TLS impersonation) | `-f urls.txt`, `-o`, `-d`, `--emit-result`, `--no-images`, `--insecure`, `--allow-private-hosts` | URL → md | Intake | conversion.md:643-669 |
| pptx_intake.py | PPTX facts bundle (identity, slide library, multi-deck profile) | `-o/--output-dir` | pptx → `<stem>.identity.json`, `<stem>.slide_library.json`, `source_profile.json` | Auto-run by `import-sources` | conversion.md:253-272 |
| pptx_to_svg.py | OOXML → SVG reconstruction; also writes `animations.json` and `conversion-report.json` | `--inheritance-mode both/layered/flat` (default both), `--roundtrip`, `--strict`, `--embed-images`, `--keep-hidden`, `--images-subdir`, `--sounds-subdir`, `-o` | pptx → `svg/`, `svg-flat/`, authoring bundle (roundtrip) | Edit Native PPTX, reconstruction | conversion.md:274-341; svg-pipeline.md:106-236 |
| project_manager.py | Project lifecycle CLI | subcommands `init [--format] [--dir] [--quick-generate]`; `import-sources [--move/--copy] [--no-image-propagation]`; `scaffold-spec`; `scaffold-lock`; `validate`; `info`; `page-context P07 [--pretty] [--record-usage] [--bundle]`; `page-context-report` | → project tree; schema validation of design_spec/spec_lock | Steps 1-4 | project.md:9-188; README.md:81-106 |
| workflow_log.py | Append a manual audit note | `<project> "<msg>"` | → `validation/workflow.log` | Any | project.md:190-236 |
| batch_validate.py | Structure check across many projects | `--all`, `--export`, `--output` | projects → report | Maintenance | project.md:254-264 |
| project_utils.py | Project info and structure helper (CLI prints info) | `<project>` | — | Library | project.md:238-252 |
| error_helper.py | Canned fixes for named errors | `<error_type> [key=val]` | — | Troubleshooting | project.md:315-323 |
| generate_examples_index.py | Rebuild examples README | `<examples_dir>` | — | Maintainer | project.md:266-273 |
| config.py | Canvas formats, colors, industries | subcommands `list-formats`, `list-colors`, `list-industries`, `export`, `format <key>` | — | Lookup (not in docs) | — |
| confirm_ui/server.py | Two-stage Strategist + template-selection page (Flask, port 5050+) | `--daemon`, `--wait-only`, `--wait-stage stage1/final`, `--wait-timeout` (590 s), `--timeout` (900 s), `--port`, `--no-browser`, `--shutdown`, `--wait` | `confirm_ui/recommendations.stage1/2.json` → `result.json`, `template_selection.json` | Generate Step 4 | confirm_ui.md:31-69 |
| apply_template.py | Install the selected Brand/Style/Layout/Deck roots into a project | `--root` (repeatable), `--dry-run`, `--skip-validation` | roots → `<project>/templates/design_spec.<kind>.<id>.md`, roster, images/icons, `template_install.json` | apply-template-workspace stage (after Stage 1) | template-tools.md:123-133 |
| spec_review/server.py | Browser review/edit/comment on design_spec.md (port 6060+) | `--daemon`, `--no-browser`, `--port`, `--timeout` (7200 s), `--hold on/off`, `--shutdown` | design_spec.md ↔ `spec_review/annotations.json`, `edits.jsonl` | Optional, after Design Spec | spec_review.md:9-60 |
| check_spec_annotations.py | Agent-side reader for spec comments | `--ack-edits`, `--applied ID` | → JSON to-dos | With spec_review | spec_review.md:119-133 |
| visualization_recall.py | Chart/table shortlist from tags; validate refs | `recall --page --tag ... --limit 3-8 --family chart/table --semantic-fallback`; `validate <family/key>... [--legacy-bare]` | → JSON | Strategist planning (§VII) | visualization-recall.md:21-101 |
| chart_recall.py | Legacy wrapper of the above | same | — | Legacy | chart-recall.md:1-26 |
| icon_sync.py | Copy chosen library icons into the project | `<project> lib/name ...` | → `icons/<lib>/` | Resource prep (exits non-zero on missing) | (docstring) |
| image_gen.py | AI image generation (Path A), manifest runner | `--manifest`, `--concurrency`, `--render-md`, `--aspect_ratio`, `--image_size`, `-b/--backend`, `-m`, `-o`, `-f`, `--reference-image`, `--list-backends` | prompt/manifest → images; requires `IMAGE_BACKEND` | Step 5 images | image.md:28-160 |
| image_search.py | Openly licensed web image search with provenance | `--batch`, `--save-candidates`, `--candidate-page`, `--max-candidates`, `--promote`, `--from-url`, `--require-terms`, `--query-variant`, `--strict-no-attribution`, `--provider`, `--orientation`, `--min-width/height` | query → image + `image_sources.json` | Step 5 images | image.md:245-385 |
| image_treat.py | Non-destructive bitmap derivative | `--brightness`, `--contrast`, `--desaturate`, `--grayscale`, `--duotone A B`, `--blur`, `--fit WxH`, `--output` | images/x → images/y.png | Image prep | image.md:162-215 |
| analyze_images.py | Objective image facts CSV | `<images_dir>` | → inventory | Before spec/SVG | image.md:217-243 |
| slice_images.py | Cut an AI "illustration sheet" into elements, alpha keying | `--grid`, `--names`, `--prefix`, `--inset`, `--trim`, `--alpha`, `--strict-alpha`, `--bg`, `--tolerance` | sheet → images/ | Image prep | image.md:166-176 |
| rotate_images.py | Orientation contact sheet and fixes | `sheet`, `fix <json>`, `auto`, `gen` | → contact sheet; rotated images | Intake review | conversion.md:671-710 |
| gemini_watermark_remover.py | Strip Gemini watermark | `-o`, `-q` | image → image | Manual | image.md:388-406 |
| latex_render.py | Legacy LaTeX → PNG (not in pipelines) | `--manifest`, `--dpi`, `--providers`, `--dry-run` | manifest → PNG | Legacy | image.md:12-26 |
| preset_shape_svg.py | 187 native PowerPoint preset shapes as SVG fragments | `list [--grouped] [--search]`; `describe <preset> [--compact] [--frame] [--adjust]`; `render <preset> --id --frame x y w h --fill --stroke ... [--filter-id] [--object-kind connector]`; `render-batch --input -` | → stdout fragment | Executor SVG authoring | README.md:238-288; svg-contract.md:273-337 |
| shape_boolean_svg.py | Merge Shapes (union/combine/fragment/intersect/subtract), text → outline | `render <svg> --operation --source a --source b --id [--font-dir]` | → stdout paths | Executor authoring | README.md:290-310; svg-pipeline.md:262-499 |
| text_measure.py | Width/wrap/bounds/calibration with the checker's estimator | `measure`, `wrap --max-width`, `box`, `calibrate <project> [--outline] [--role NAME:FAMILY:SIZE[:bold]]`; global `--size --family --weight --letter-spacing --no-headroom`, `--json` | → widths, wrapped `<tspan>`, `data-pptx-bounds`, `validation/text_calibration.json` | Pre-authoring fit | svg-pipeline.md:1068-1154 |
| svg_position_calculator.py | Chart coordinate calc/verify | `calc bar/pie/radar/line/grid`, `validate`, `analyze`, `interactive`, `from-json` | → coordinate tables | verify-charts stage | svg-pipeline.md:1206-1285 |
| svg_quality_checker.py | SVG + project contract gate | see §3 | → exit code, `validation/svg_quality_*report.json` | After every page batch; final gate before export | svg-pipeline.md:1156-1204 |
| stamp_native_fallbacks.py | Bind SVG-first chart/table fallbacks with a SHA | `--write` | svg/dir → `data-pptx-fallback-sha256` | Before `--native-charts-and-tables` | svg-pipeline.md:601-613 |
| compact_svg_styles.py | Hoist common fonts and drop redundant inherited styles | `--inplace` | svg → svg | Fix `--canonical-authoring` warnings | svg-pipeline.md:526-559 |
| compact_svg_coordinates.py | Round model-facing coordinates to 2 decimals safely | `--inplace`, `--keep-native-frames` | svg → svg | Same | svg-pipeline.md:501-524 |
| update_spec.py | Deck-wide color/font swap in lock + every SVG | `<project> <section>.<key>=<value>`, `-n/--dry-run` | spec_lock.md + svg_output/*.svg | Post-generation tweak | update_spec.md:1-69 |
| total_md_split.py | Split total.md into notes/*.md | `-o`, `-q` | total.md → notes/ | Step 7 (notes on) | svg-pipeline.md:1053-1066 |
| finalize_svg.py | Embed icons/images, expand `<use>`, flatten tspan → self-contained preview | `--only embed-icons/align-images/...`, `-n`, `-q`, `--no-compress`, `--max-dimension 2560`, `--image-scale 2` | svg_output/ → svg_final/ | Step 7.2 (preview only) | svg-pipeline.md:784-796; README.md:356-358 |
| svg_finalize/*.py | Single-step diagnostics (embed_icons, align_embed_images, flatten_tspan, crop_images, embed_images, fix_image_aspect, svg_rect_to_path legacy) | `--dry-run`, etc. | per file | Diagnostics | svg-pipeline.md:1287-1340 |
| svg_to_pptx.py | **Native editable PPTX export** | see §4 | svg_output/ → `exports/*.pptx`, `validation/*.report.json`, `backup/` | Step 7 | svg-pipeline.md:798-1038 |
| template_preview_pptx.py | Export template prototypes as structured review deck | `-o`, `--force`, `--native-charts-and-tables` | template workspace → `exports/<id>_template_preview.pptx` | Create Template review | template-tools.md:115-121; README.md:236 |
| pptx_delivery_check.py | Read-only audit of a finished PPTX | `<pptx>` | → JSON: zip/OPC, content types, relationships, hidden slides, fonts, media footprint, motion | Delivery | project.md:55 (index only) |
| animation_config.py | Animation/Morph sidecar | `scaffold [-o] [--force]`, `list-groups`, `validate [-c]` | → `animations.json` | customize-animations stage | README.md:35; pptx-animations.md:209-214 |
| pptx_animations.py | Registry inspector | `--list`, `--describe <effect>`, `--describe-transition <effect>`, `--demo` | → stdout | Planning motion | pptx-animations.md:111-117; pptx-transitions.md:193-198 |
| sound_sync.py | Copy selected CC0 sounds | `list [--query]`; `<project> ns/id ...` | → `sounds/` | Motion sound | svg-pipeline.md:993 |
| notes_to_audio.py | TTS per slide (edge default; elevenlabs, minimax, qwen, cosyvoice) | `--provider`, `--voice/--voice-id`, `--rate/--pitch/--volume`, `--concurrency`, `--subtitle-max-chars`, `--list-voices --locale`, `--list-common-voices`, many provider-specific flags | notes/ → audio/*.mp3 + .srt | generate-audio stage | narration.md:11-29 |
| narration_sync.py | Cue-bound click-free animation timing; subtitle merge | `fingerprint`; `animations [--narration-start-floor --narration-padding --force]`; `subtitles --pptx` | → `narration_animations.json`, `audio/total.srt` | generate-audio | narration.md:31-50 |
| powerpoint_video.py | Windows PowerPoint COM video export | `--check`, `-o`, `--resolution`, `--fps`, `--quality`, `--timeout` | narrated pptx → mp4 | generate-audio | narration.md:68-75 |
| video_sound_mix.py | Mix transition/object SFX into video | `--pptx --trace --video -o --stem-output --report-output`, gain flags | → mixed mp4 | generate-audio | narration.md:77-83 |
| video_subtitles.py | stable-ts forced-alignment SRT for finished video | `--video --language --model --max-chars` | → .srt | generate-audio | narration.md:85-91 |
| video_motion_plan.py | Conversion trace → renderer-neutral video motion plan | `--style adaptive/restrained/dynamic`, `-o`, `--force` | trace.json → plan.json | Video path | video-motion-plan.md:1-117 |
| svg_editor/server.py | Live preview + direct edit + annotations (port 6060+) | `--daemon`, `--live` (7200 s), `--no-browser`, `--port`, `--timeout`, `--shutdown` | edits svg_output/ in place; `live_preview/lock.json`, `draft.json`, `edits.jsonl` | Step 6 live-preview stage | svg_editor.md:1-40 |
| check_annotations.py | List pending editor annotations (`data-edit-*`) | `<project or svg>` | → summary | After live preview | (docstring) |
| visual_review.py | Playwright render of each page to PNG, matching the live preview | `--pages 02 03`, `--server-url`, `--lock-timeout` | → `<project>/.preview/*.png` + JSON; exits 0/2/3/4 | visual-review stage | svg-pipeline.md:1040-1051 |
| pptx_template_import.py | PPTX → template import workspace | `-o`, `--inheritance-mode layered/both/flat`, `--manifest-only`, `--skip-manifest`, `--embed-images` | pptx → manifest, native_structure, svg/, authoring-svg/, icons/imported/ | Create Template §1 | template-tools.md:5-31; project.md:275-313 |
| svg_authoring_view.py | Compact editable IR from imported SVG; summary refresh; cross-page object move | `-o`, `--projection-kind layered/flat/generic`, `--refresh-summary`, `--adopt-object from.svg:id --into target.svg`, `--force` | → authoring-svg/ + summary/manifest | Create Template, round-trip | svg-pipeline.md:19-104 |
| extract_svg_assets.py | Factor big decorative vectors into `icons/imported/` | `--icons-dir`, `--icon-namespace`, `--inplace`, `--id-prefix`, `--reuse-inventory`, `--min-*`, `--clean-stale` | → `<use data-icon>` + inventory | External SVG / Type B | svg-pipeline.md:561-599 |
| extract_svg_pictures.py | Turn a named `<g>` into one SVG picture | `--select`, `--resource-root`, `--images-dir`, `--bounds`, `--bounds-mode`, `--padding`, `--inplace` | → `<image>` + asset | Create Template standard/fidelity | svg-pipeline.md:703-751 |
| mirror_template_materialize.py | Type A mirror publication from an import workspace | `<import_ws> <template_ws> [--kind deck/layout]` | → templates/*.svg, native_payloads.json.gz, source_themes.json, spec skeleton | Create Template mirror | svg-pipeline.md:615-701; template-tools.md:33-70 |
| register_template.py | Add a template to the library index | `<id> --kind brand/style/layout/deck`, `--dry-run`, `--rebuild-all` | → `templates/<kind>s/<kind>s_index.json` | Create Template end | template-tools.md:135-142 |
| beautify_identity.py | Theme vs observed identity of a source deck | `-o` | pptx → identity.json | beautify-pptx profile | (docstring) |
| beautify_inventory.py | Per-slide ledger joining slide_library + images | `--images`, `--summary`, `--page`, `--verify`, `--with-geometry` | → inventory JSON | beautify-pptx | (docstring) |
| attribution_guard.py | Integrity guard; called by checker and other CLIs | — | fails closed if the bundle was modified | Every run | (docstring) |
| update_repo.py | git pull + pip sync | `--skip-pip` | — | Maintenance | README.md:44-48 |
| prompt_audit.py | Token budget/governance lint of prompt corpus | `--json`, `--root`, `--manifest`, `--skip-near-duplicates` | — | Maintainer only | prompt_audit.md:1-68 |

## 3. Checkers in detail

### 3.1 `svg_quality_checker.py` (→ `svg_quality/cli.py`, `checker.py`, `svg_contracts.py`)
**CLI** (hand-parsed; `svg_quality/cli.py:111-160`):
- Target: an svg file, `svg_output/`, a project, `--all <dir>`, or `<ws>/templates`.
- `--stage early|first-page|page|final`. Default is `final`. `page` needs `--page <name>`; this option is undocumented in docs/.
- `--format <canvas>`; `--json` / `--json-output <p>`; `--export` / `--output <p>` (plain-text report).
- Modes: `--quick-generate`, `--canonical-authoring`, `--roundtrip`, `--template-mode`, `--slot-capacity-report`.
- Report paths: `validation/svg_quality_report.json` (final), `_early_`, `_first_page_`, `_page_` (svg-pipeline.md:1184-1197).

**Severity model**: findings are free-text strings in `errors` or `warnings`. **There are no rule ids.** Aggregation only buckets them as XML / viewBox / foreignObject / Paint / Font / Other (`checker.py:7143-7156`). Only errors set exit 1. Warnings are advisory and never block (svg-pipeline.md:1181-1182; cli.py:157-158). The JSON report separates `blocking`, `introduced`, `inherited` (identical to the prototype) and `source-import` findings, and fingerprints every SVG (svg-pipeline.md:1191-1197). The exporter refuses a missing, stale, non-final or blocking report (svg-pipeline.md:951).

**Per-file checks, in order** (`checker.py:1268-1475`):
1. XML parse. Canonical-authoring drift is a WARN under `--canonical-authoring` (svg-contract.md:49-53).
2. Native payload ref hydration. Quick only: a missing root `lang` on page 1 is a WARN.
3. `viewBox`: positive integer, origin 0, and must match the format/lock; a root transform is an ERROR (svg-contract.md:411-417). Legacy pptx attributes are flagged. A carrier receipt is recorded as info (svg-pipeline.md:952).
4. Nested-svg crop transport exactness (svg-contract.md:626-641).
5. **Forbidden elements (ERROR)** (`svg_contracts.py:197+`): `<style>`, `class`, id+style, xml-stylesheet, `<link stylesheet>`, `@import`, `foreignObject`, `textPath`, `@font-face`, SMIL `animate*`, invalid local `<use>`, `mask` (svg-contract.md:386-387; mask-gradient-smoke.md:168-192). Also ERROR: unknown inline style properties, `!important`, blend/isolation/backdrop.
6. Geometry lengths: unitless ordinary decimals; `px` is a WARN; other units are an ERROR (svg-contract.md:341-392). Shape coordinate ranges are checked.
7. Stroke grammar: dash presets, cap/join, `vector-effect`, dashoffset only on a thick circle (svg-contract.md:643-668).
8. Image contract: decodable sources, `preserveAspectRatio` grammar, clip rules (svg-contract.md:587-641, 89-111).
9. Freeform path/points grammar (svg-contract.md:763-793).
10. Transforms: only translate/scale/rotate/matrix; skew/shear is an ERROR (svg-contract.md:728-761).
11. Opacity ranges. `<g opacity>` gives a fidelity WARN (svg-contract.md:396-405).
12. Authoring-property and text-property surfaces: the font-weight/style/anchor/decoration/baseline-shift/letter-spacing/font-size grammar. `word-spacing`, `dominant-baseline`, `line-height`, `writing-mode` and similar are ERRORs (svg-contract.md:670-726).
13. Preserved `txBody` contract. Paint compatibility: an unknown paint is an ERROR; `rgba()` or non-canonical HEX is a WARN recommending `#RRGGBB` (svg-contract.md:465-503).
14. Reference spelling, definitions, paint references, markers (5 native line-end shapes; anything else is an ERROR) (svg-contract.md:62-85), clip-path.
15. Filters: shadow/glow subset only (svg-contract.md:550-585). Imported effect status `unsupported` is an ERROR.
16. Gradients: ≥2 stops, non-decreasing offsets, objectBoundingBox only, radial focus inside the circle (svg-contract.md:505-532).
17. Font-size values, fonts, `<text>` wrapping structure. Semantic-shape text: at most one direct `<text>` per `data-pptx-semantic-object="shape"` (svg-pipeline.md:225-230).
18. Hyperlinks; image references exist; icon placeholders resolve under project `icons/` (svg-pipeline.md:1337-1340).
19. Unsupported visual elements, hidden elements, preset geometry metadata/transforms (rerendered from the registry; stale is an ERROR) (svg-contract.md:316-328).
20. Animation group ids; `<pattern>` must declare a PPTX preset; native chart/table markers, including SVG-first parity. Parity findings are WARN tagged "blocks --native-charts-and-tables export" (native-data.md:45).
21. Structured-template metadata (Master/Layout/slot) and semantic page/role markers.
22. **spec_lock alignment** (`checker.py:6692-6720`): colors, fonts and sizes are compared with the lock. Extra colors/fonts are *info*. **An undeclared display size may appear on at most two pages; the third occurrence is an ERROR** that requires declaring the role. Skipped in template mode or when there is no lock.
23. Web-image attribution (image_sources.json credit present).

**Text/geometry gates** (svg-contract.md:437-454; svg-pipeline.md:941-942):
- Every visible direct-root `<g>` needs `data-pptx-bounds`. If missing: ERROR on final pages and templates, WARN otherwise.
- Root-group overlap greater than 1px on both axes is an ERROR (slots, structural roles and Morph staging are exempt).
- Text overflow past its module: ≤1px ignored, ≤5% WARN, >5% ERROR. Text past the page `viewBox` is always an ERROR.
- Text that cannot be estimated gets a WARN. Other text checks: positional tspans, fragmented paragraphs, unmergeable leading text (`checker.py:3122, 4779-5004`).

**Directory/project checks** (`check_directory`, `checker.py:7230+`):
- pptx_structure contract (flat vs structured; lock rosters) (`:7521`).
- Illustration resource contract (`:7978`), planned-image closure against spec §VIII (`:8535`), sourced-image provenance (`:9027`).
- `animations.json` contract (`:9111`); template contract (`:9149`).
- Duplicate empty Layout contracts under different keys (svg-pipeline.md:1179).

**Modes**:
- `--template-mode`: globs `*.svg` and skips the lock. Roster vs Design Spec mismatch is an ERROR; a missing conventional placeholder is a WARN, silenced by a `placeholders:` frontmatter map. One Master+Layout is required per root. Ordinary `<g>` inside Master/Layout, nested markers, missing slot bounds and carriers ≠ 1 are ERRORs. Masters must be equal across pages. Identical distinct Layouts give a WARN. Brand/Style kinds are validated against their own contracts (template-tools.md:81-87).
- `--slot-capacity-report` (with `--template-mode`): read-only JSON. For every text slot it gives bounds, font, line pitch, Latin/CJK capacity and the allowed baseline band `[top+0.85·size, bottom−0.35·size]` (template-tools.md:89-113).
- `--roundtrip`: checks only new or edited text. Overflow past an explicit frame or the canvas blocks; the nearest-rect fallback only warns (svg-pipeline.md:213-236).
- `--quick-generate`: lockless. It infers flat vs structured from the roster; a mixed roster is an ERROR (svg-pipeline.md:868-896).

**Configurable**: stage, format, mode flags, report paths. Nothing else: there are no rule toggles, no thresholds and no ignore lists. Canonical compaction warnings are fixed with `compact_svg_styles.py` / `compact_svg_coordinates.py --keep-native-frames`, then rerun `stamp_native_fallbacks.py --write` (svg-pipeline.md:546-553).

### 3.2 Other validators
- `project_manager.py validate`: schema lint of design_spec.md and spec_lock.md against `templates/schemas/*.schema.json`. It reports missing sections and fields (per-slide `Audience move`/`Relationships`), illegal enums and catalog refs. In versioned locks, `## forbidden` items must end with `(user)` (project.md:84-108).
- `animation_config.py validate`: unknown effect/trigger/group, ranges, sound paths (pptx-animations.md:209-214).
- `visualization_recall.py validate`: chart/table refs resolve (visualization-recall.md:62-85).
- `svg_position_calculator.py`: chart geometry recipes (svg-pipeline.md:1240-1285).
- `pptx_delivery_check.py`: post-export audit with issue codes `zip_integrity_failed`, `invalid_content_types`, `invalid_relationship_part`, `orphan_notes_parts`, `hidden_slides`, `font_portability`, `external_media`, `invalid_transition_structure`, `invalid_animation_structure`, `dangling_custom_show_reference`, … Results are split into `errors` and `advisories`; the report also covers the media footprint and top contributors (`pptx_delivery_check.py:92-160`).
- Exporter postflight: the receipt line `[POSTFLIGHT] status quality_gate slides warning_categories`. `font_portability` warns on fonts that need a custom install; fonts are never embedded (svg-pipeline.md:915-923, 953-954).
- `template_preview_pptx.py`: reopens the built PPTX and verifies the Master/Layout graph (template-tools.md:121).

## 4. Export path: `svg_to_pptx.py` (→ `svg_to_pptx/pptx_package/cli.py`)

**Source and route flags**:
- Reads `svg_output/` by default. `-s <dir>` sets another source; `-s final` is a diagnostic only (svg-pipeline.md:929).
- `-o` gives an explicit path and skips `backup/`.
- `-f` canvas format; `-q` quiet; `--primary-language TAG` (deck language, RTL handling, theme script fonts) (svg-pipeline.md:804).

**Release gate**: default and `--quick-generate` exports refuse to run when the final quality report is missing or stale (svg-pipeline.md:951).

**`--quick-generate`**:
- Skips Strategist, Confirm UI, design_spec and spec_lock, and finalize.
- Infers canvas and flat vs structured output from the SVGs.
- Notes, custom animation and narration are off by default; `--with-notes` turns notes on.
- Requires `svg_quality_checker --quick-generate --canonical-authoring --stage final --json` first (svg-pipeline.md:868-896).

**Structure** (`--pptx-structure structured|flat` overrides the lock's `pptx_structure.mode`):
- **flat**: one clean project-owned Master and one Blank Layout built from the lock's colors and typography; stock placeholders removed; date/footer/slide-number hooks kept (svg-pipeline.md:939, 944).
- **structured**: only for `template_reuse_scope: mirror|layout`. It needs explicit `pptx_masters`, `pptx_layouts` and per-page `page_pptx_layouts`, and every SVG root repeats its Master/Layout keys.
  - Master text styles are derived from the title/body anchors: levels 2-9 scale from 15/16 down to 8/16 of the body size (svg-pipeline.md:1010-1016).
  - Each Layout's level-1 size is copied from its prototype (:1018). Placeholder identities, the `p:hf` flags and visibility attributes are written (:1020-1024).
  - After building, the package is read back and checked; a mismatch aborts export (:1028).
- Never clusters or promotes repeated chrome heuristically (README.md:364).

**Theme and colour**:
- Locked typography and colours are mapped into the theme/Master defaults (`drawingml/theme_colors.py`, `theme_fonts.py`). A mirror route installs `templates/source_themes.json`, one theme per Master (svg-pipeline.md:644-647).
- A full-canvas `<rect>` (solid, gradient or preset-pattern fill) is promoted to native `p:bg` (svg-contract.md:419-426).
- **There is no recolor or colorway flag in the exporter.** The only deck-wide colour swap tool is `update_spec.py` (see §6).

**Native objects**:
- Shapes: an authored preset compiles to one `p:sp`/`p:cxnSp`; rounded `rect` becomes `roundRect`; paths become `custGeom`; images become `p:pic` with `srcRect` crop and clip geometry; markers become native line ends; shadow/glow becomes DrawingML effects.
- `--native-charts-and-tables` (alias `--native-objects`) is opt-in: chart/table markers become real PowerPoint charts (with an embedded workbook) and tables. SVG-first markers need `stamp_native_fallbacks` (README.md:388-397; native-data.md).
- Formulas always become editable OMML (svg-pipeline.md:806-825).
- Hyperlinks, including `#slide-N`, are supported.

**Text**:
- Default: one frame per `<text>` that keeps the authored breaks, with no wrap and resize-to-fit.
- `--reflow-text` (alias `--merge-paragraphs`) produces flowing prose; `--no-merge` makes one frame per line (svg-pipeline.md:924-928).
- The first-line baseline comes from the bundled `font_metrics.json` (:1070-1101). An inline `dx` becomes an NBSP spacing run (:1295-1302).

**Images**:
- `--image-sizing cap|display` (default `cap`: keep original bytes unless the image is above 2560 px).
- `--image-scale 2`, `--image-quality 85`, `--image-max-dimension 2560`, `--no-image-optimize` (README.md:356).
- Media files are named by content hash; EMF/WMF are embedded natively (svg-pipeline.md:800, 947).

**Notes**: embedded by default in Default Generate; `--no-notes` disables them (and is required when notes are off, so stale notes are not embedded); `--with-notes` enables them in Quick (svg-pipeline.md:960; README.md:352-354).

**Transitions** (48 native effects plus `none`; pptx-transitions.md:53-139):
- `-t/--transition` (default fade, 0.4 s), `--transition-duration`.
- `--auto-advance N`; `--kiosk` (loop and kiosk mode) (pptx-transitions.md:294-298).
- Explicit Morph pairs are declared in `animations.json` `morph.pairs` (:213-235).

**Object animations** (203 effects; default `none`):
- `-a none|auto|mixed|random|<canonical key>`, `--animation-duration 0.4`, `--animation-stagger 0.5`, `--animation-trigger after-previous|with-previous|on-click`.
- `--animation-config <json>`, `--no-animations`.
- Targets are top-level `<g id>` groups (svg-pipeline.md:975-998; pptx-animations.md:277-309).

**Narration**:
- `--recorded-narration audio` needs audio for every slide (read with ffprobe); output gets the `_narrated` suffix.
- Related flags: `--narration-audio-dir` (partial embedding allowed), `--use-narration-timings`, `--narration-start-floor 0.8`, `--narration-padding 0.5`, `--inherit-motion-from <report>` (svg-pipeline.md:961-974; narration.md:52-66).

**Diagnostics**:
- `--conversion-trace [path]` writes `validation/<stem>.trace.json` (svg-pipeline.md:950).
- `--enable-dangerous-nonconforming-svg-export` is a flat compatibility path that sits outside the quality gate (:929, 938).

**Round-trip** (`--roundtrip`, source-preserving edit of an existing PPTX):
- Reads `authoring-svg-flat/` and an optional `page_plan.json` (select, reorder or repeat slides).
- Unchanged slides pass through byte-for-byte.
- Prints a receipt with passthrough/patched/rebuilt counts (svg-pipeline.md:106-241).

**Outputs**: `exports/<name>_<ts>.pptx`, `validation/<name>_<ts>.report.json` (postflight), `backup/<ts>/svg_output/` (svg-pipeline.md:902-910).

**Always strict**: an unsupported visual element fails the export with file, tag and position; nothing is silently dropped (svg-pipeline.md:938).

## 5. Template import / creation tools

**Type A mirror sequence** (template-tools.md:35-43):
`pptx_template_import.py src.pptx -o ws --inheritance-mode both` → `mirror_template_materialize.py ws tpl [--kind deck|layout]` → `svg_quality_checker.py tpl/templates --template-mode --canonical-authoring` → `template_preview_pptx.py tpl -o preview.pptx` → finish `design_spec.<kind>.TODO.md` → `register_template.py <id> --kind ...`.

**`pptx_template_import.py` outputs** (template-tools.md:11-31):
- `analysis/manifest.json`: theme, fonts, resources, placeholders, `pageTypeCandidates`.
- `analysis/native_structure.json`: Master/Layout keys and picker names.
- `sources/source.pptx`.
- Layered lossless `svg/`, with `svg/inheritance.json`.
- Optional `svg-flat/`.
- Editable `authoring-svg/`, with `authoring_summary.json`; this is what the model reads.
- `icons/imported/` decoration assets; `validation/conversion-report.json`.

**Standard/fidelity authoring (Type B)** (template-tools.md:72-79; svg-pipeline.md:19-104, 703-751):
- `svg_authoring_view.py --projection-kind generic`
- `extract_svg_assets.py ... --min-decoration-bytes 3000 --clean-stale`
- Optional `extract_svg_pictures.py` (turns one named group into a picture)
- `svg_authoring_view.py --refresh-summary` after direct IR edits.

**Install into a project**: `apply_template.py <project> --root <ws>...` is atomic, rolls back on failure and writes `template_install.json` (template-tools.md:123-133).

**Library registration**: `register_template.py` maintains the four index JSONs that the Confirm UI reads (template-tools.md:135-142; confirm_ui.md:105-112).

**Analysis of a source deck (no template)**:
- `pptx_intake.py`: identity and slide_library.
- `beautify_identity.py`: theme vs observed fonts, sizes and colours.
- `beautify_inventory.py`: per-slide ledger.
- `source_to_md/ppt_to_md.py`: content.
- There is **no dedicated "series analysis" tool**. The closest equivalents are `manifest.json pageTypeCandidates` and `source_profile.json` page types (conversion.md:266).

**Round-trip edit of an existing deck**: `pptx_to_svg.py --roundtrip` → edit `authoring-svg-flat/` (+ `page_plan.json`) → `svg_quality_checker --roundtrip --json` → `svg_to_pptx --roundtrip` (README.md:172-199).

## 6. Easy-to-miss tools

### Preview and review servers
| Tool | What it does | Doc |
|---|---|---|
| `svg_editor/server.py --live --daemon` | Live preview in the browser with direct edits (drag, nudge, inspector, undo) and AI annotations written as `data-edit-*`. Read annotations with `check_annotations.py`. Re-export is still a chat step. Port and pid are in `live_preview/lock.json`. | svg_editor.md |
| `visual_review.py` | Playwright PNG per page into `.preview/`, identical to the live preview (CJK fallback included). **Needs the live-preview server running.** This is the supported render-to-image check; cairosvg was rejected for CJK. | svg-pipeline.md:1040-1051 |
| `confirm_ui/server.py` | Two-stage confirmation page: style preview thumbnails, palette and typography editors, template pickers. | confirm_ui.md |
| `spec_review/server.py` + `check_spec_annotations.py` | Block-level review, edit and comments on design_spec.md. | spec_review.md |

### Fit and measurement
| Tool | What it does | Doc |
|---|---|---|
| `text_measure.py` (`measure`/`wrap`/`box`/`calibrate`) | Uses the same estimator as the checker. `calibrate` writes per-role CJK/Latin rates to `validation/text_calibration.json`. | svg-pipeline.md:1103-1154 |
| `svg_quality_checker --template-mode --slot-capacity-report` | Characters that fit in each template slot. | template-tools.md:89-113 |
| `svg_position_calculator.py` | Chart coordinate calc/verify recipes (stacked, waterfall, pareto, …). | svg-pipeline.md:1240-1285 |

### Authoring helpers
| Tool | What it does | Doc |
|---|---|---|
| `preset_shape_svg.py` | Native PowerPoint autoshapes (187 presets). | README.md:238-288 |
| `shape_boolean_svg.py` | Merge Shapes, including text → outline. | README.md:290-310 |
| `compact_svg_styles.py` / `compact_svg_coordinates.py` | Clear `--canonical-authoring` warnings. | svg-pipeline.md:501-559 |
| `stamp_native_fallbacks.py` | Required after editing chart/table fallbacks. | svg-pipeline.md:601-613 |

### Recolor / theme swap: `update_spec.py <project> colors.primary=#HEX`
- Literal HEX replacement in every `svg_output/*.svg` plus the lock; `typography.font_family` replaces every `font-family` attribute.
- **Needs `spec_lock.md`**: it reads the old value from the lock, so it does not work on lockless Quick projects without a lock.
- Does not change derived tints or sizes, and makes no backups (update_spec.md:8-65).
- The exporter has no colorway or theme-swap option.

### Delivery and inventory
| Tool | What it does | Doc |
|---|---|---|
| `pptx_delivery_check.py` | Read-only audit of the final PPTX (fonts, media weight, hidden slides, motion, OPC). | §3.2 |
| `analyze_images.py`, `image_treat.py`, `slice_images.py`, `rotate_images.py`, `icon_sync.py`, `sound_sync.py` | Asset-preparation helpers. | §2 |
| `config.py list-formats` | Lists canvas formats. | — |
| `project_manager.py page-context P07` | Per-page projection of spec and lock. | project.md:116-166 |
| `project_manager.py page-context-report` | Token telemetry. | project.md:116-166 |

### Motion, TTS and video
- Motion: `animation_config.py scaffold|list-groups|validate`, `pptx_animations.py --list/--describe/--describe-transition`, Morph pairs in `animations.json`, kiosk.
- TTS and video: `notes_to_audio.py` (5 providers, SRT) → `narration_sync.py` → `svg_to_pptx --recorded-narration audio` → `powerpoint_video.py` (Windows COM) → `video_sound_mix.py` → `video_subtitles.py`; `video_motion_plan.py`.

### Logging and maintenance
- `validation/workflow.log`: written automatically by every project CLI; `workflow_log.py` adds manual notes.
- `attribution_guard.py`: integrity gate; it fails closed if the plugin bundle is modified.
- Maintainer-only: `prompt_audit.py`, `generate_examples_index.py`, `batch_validate.py`, `update_repo.py`, `error_helper.py`; the smoke docs (advanced-image-motion, mask-gradient, multilingual-text, shape-boolean in svg-pipeline.md:262-499).

### Likely duplication with a wrapper Skill (check against your own scripts)
- Render self-check → `visual_review.py` (or `svg_final/` + PowerPoint).
- Fit/overflow checks → `text_measure.py` and the checker's bounds gate.
- Colorway swap → `update_spec.py`, but only if a spec_lock exists.
- Post-export audit → `pptx_delivery_check.py` plus the exporter postflight receipt.
- Template slot capacity → `--slot-capacity-report`.
- Style compaction → `compact_svg_styles.py`.
- Template review deck → `template_preview_pptx.py`.
- Live page editing → `svg_editor`.
