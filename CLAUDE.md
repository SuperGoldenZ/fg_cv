# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
pytest

# Run a single test file
pytest test/test_sf6_match_details.py

# Run a single test by name
pytest test/test_sf6_match_details.py::test_get_round_results

# Lint (fatal errors only)
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Lint (warnings, non-blocking)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

Dependencies are installed via `pip install -r requirements.txt`. Tesseract OCR must be installed separately (`tesseract-ocr` + `tesseract-ocr-jpn` on Linux; CI installs these automatically). An OpenAI API key can be placed in `.openaikey` in the project root for OCR methods that use GPT-4o.

## Architecture

**fg_cv** extracts structured data from fighting game screenshots and video frames using computer vision. There is no ML training — all detection is rule-based (pixel color sampling, template matching, pytesseract OCR, OpenAI GPT-4o OCR).

### Screen detection pattern

Every screen type has a `layout` dict (e.g. `src/fg_cv/games/sf6/layouts/match_over.py`) with:
- `expected_colors`: list of `{x, y, color}` pixel probes that must match
- `unexpected_colors`: probes that must *not* match (used to reject false positives)
- `threshold`: minimum number of `expected_colors` that must pass

Extractor classes (`MatchOverExtractor`, `VsScreenExtractor`, `RoundStartScreenExtractor`) load the layout via `importlib` and perform pixel-similarity checks. A `factor` scales coordinates when the frame is 720p instead of 1080p.

### FlexibleCv — the main SF6 workhorse

`src/fg_cv/flexible_cv.py` is a generic extractor used for SF6 replay list rows and match details. It reads `ocr_blocks`, `round_result_roi`, `portrait_roi`, `mr_roi`, `ringname_roi`, `datetime_roi`, and `match_type_roi` sections from a layout and exposes typed `get_*` methods.

Key behaviours:
- **`get_round_results()`** — template-matches all `.png` files in `round_result_roi["icons_dir"]` (skipping files ending in `_loses`) against the P1 and P2 icon columns. New icon files are auto-discovered; no code changes needed to add a new finish type.
- **Portrait matching** — histogram-equalised grayscale NCC against reference images in `portrait_roi["portraits_dir"]/{p1,p2}/`. Build references with `tools/build_sf6_character_portraits.py`.
- **OCR** — defaults to OpenAI GPT-4o (`method: "openai"` in a block); individual blocks can override to `"pytesseract"`.

### Game layout directories

```
src/fg_cv/games/
  sf6/layouts/          # Street Fighter 6 screen layouts
  vf5/layouts/          # VF5 REVO layouts
  vf5-kumite/layouts/   # VF5 Kumite variant
  vf5-replay-menu/layouts/
  2xko/layouts/
  2xko-bau/layouts/
  layouts/              # Shared/generic layouts
```

Each game has its own `vs.py`, `match_over.py`, `round_start.py`, `combo.py`, `lifebars.py`, etc.

### Assets

- `assets/test_images/sf6/` — screenshot fixtures used by pytest
- `assets/sf6/round_result_icons/` — SF6 round-end icon templates (`p1_*.png`, `p2_*.png`). Files ending in `_loses` are skipped by `get_round_results()`.
- `assets/sf6/` — other SF6 reference assets (character portraits after build step)

### Test conventions

- Each test file exercises one screen type or extractor.
- Test images are committed to `assets/test_images/` and referenced by path in pytest parametrize lists.
- `test_sf6_match_details.py` derives expected round results from the image filename (e.g. `p1_victory_p2_chip_damage.png` → `["p1_victory", "p2_chip_damage"]`). Filename aliases for icon name mismatches live in `_RESULT_ALIASES` at the top of that file.
