import importlib
import os
import re
from datetime import datetime
from fg_cv.cv_helper import CvHelper
import cv2
import numpy as np
import pytesseract


class FlexibleCv:
    def __init__(self, game, layout_name="first_99", suffix=None):
        self.game = game

        self.layout = importlib.import_module(
            f"fg_cv.games.{self.game}.layouts.{layout_name}"
        ).layout

        self.frame = None
        self.row_y_tops_key = "row_y_tops"
        if suffix is not None:
            self.row_y_tops_key = f"row_y_tops_{suffix}"

        self.row_y_centers_key = "row_y_centers"
        if suffix is not None:
            self.row_y_centers_key = f"row_y_centers_{suffix}"

        self.cv_helper = CvHelper()

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_match(self, frame=None):
        if frame is not None:
            self.frame = frame
            self.set_factor()

        if self.frame is None:
            raise Exception("Frame not set")

        count: int = 0

        for color in self.layout["expected_colors"]:
            if self.factor == 1:
                pixel_color = self.frame[color["y"], color["x"]]
            else:
                pixel_color = self.frame[
                    int(color["y"] * self.factor), int(color["x"] * self.factor)
                ]

            target_bgr = CvHelper.hex_to_bgr(color["color"])

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.86:
                count += 1

        for color in self.layout["unexpected_colors"]:
            if self.factor == 1:
                pixel_color = self.frame[color["y"], color["x"]]
            else:
                pixel_color = self.frame[
                    int(color["y"] * self.factor), int(color["x"] * self.factor)
                ]

            target_bgr = CvHelper.hex_to_bgr(color["color"])

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.95:
                # print("unexpected color fail")
                # print(color)
                return False

        # print(f"got count {count} vs {self.layout["threshold"]}")
        # if count < self.layout["threshold"]:
        # print(f"below threshold {count}")
        return count >= self.layout["threshold"]

    def get_ocr_blocks(self):
        return self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])

    def get_ocr_block_names(self):
        return list(self.layout["ocr_blocks"].keys())

    def get_ocr_values(self):
        return self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])

    def get_selected_row(self):
        """Return the 1-based index of the selected row (1–N), or None if none match.

        The layout must define:
          - ``row_y_centers`` – list of y pixel coordinates (1080p) for each row's centre
          - ``selected_x``    – x pixel coordinate to sample (default 1296)
          - ``brightness_threshold`` – average BGR brightness above which a pixel is
            considered part of the selected (highlighted) row (default 150)

        Unselected rows have a dark background (~brightness 30–50); the selected row
        has a bright background (~brightness 229–254), so 150 is a safe midpoint.
        """
        row_y_centers = self.layout.get(self.row_y_centers_key, self.layout.get("row_y_centers", []))
        selected_x = self.layout.get("selected_x", 1296)
        brightness_threshold = self.layout.get("brightness_threshold", 150)

        for i, y in enumerate(row_y_centers):
            scaled_y = int(y * self.factor)
            scaled_x = int(selected_x * self.factor)
            pixel = self.frame[scaled_y, scaled_x]
            brightness = (int(pixel[0]) + int(pixel[1]) + int(pixel[2])) // 3
            if brightness >= brightness_threshold:
                return i + 1  # 1-based row number

        return None

    def get_winner_from_selected_row(self, row_num=None):
        """Return the winning player number for the selected replay row.

        Checks P1 result region (``p1_result_roi``) then P2 result region
        (``p2_result_roi``) if present:
          - P1 blue  → P1 wins  → returns 1
          - P2 blue  → P2 wins  → returns 2
          - P1 grey, no P2 blue → draw → returns 0
          - no match → returns None

        When ``p2_result_roi`` is absent the original two-state logic applies
        (P1 blue → 1, P1 grey → 2).

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            1, 2, 0 (draw), or None.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None

        row_y_tops = self.layout.get(self.row_y_tops_key, [])
        roi_cfg = self.layout.get("p1_result_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            print(f"could not row {row_num}, returning None")
            return None

        row_top = row_y_tops[row_num - 1]
        thr = roi_cfg.get("color_threshold", 25)
        min_px = roi_cfg.get("min_pixels", 5)

        def _sample(cfg, key):
            x = int(cfg["x"] * self.factor)
            y = int((row_top + cfg["y_offset"]) * self.factor)
            w = int(cfg["w"] * self.factor)
            h = int(cfg["h"] * self.factor)
            roi = self.frame[y : y + h, x : x + w]
            return CvHelper.count_color_in_roi(roi, cfg[key], threshold=thr)

        p1_win  = _sample(roi_cfg, "win_color")
        if p1_win >= min_px:
            return 1

        p2_cfg = self.layout.get("p2_result_roi")
        if p2_cfg:
            p2_win = _sample(p2_cfg, "win_color")
            if p2_win >= min_px:
                return 2
            p1_lose = _sample(roi_cfg, "lose_color")
            if p1_lose >= min_px:
                return 0  # draw

        else:
            p1_lose = _sample(roi_cfg, "lose_color")
            if p1_lose >= min_px:
                return 2

        print(f"could not get winner, returning None")
        return None

    def get_datetime_from_selected_row(self, row_num=None):
        """Return the match date/time string from the selected replay row.

        Reads the date/time text region (``datetime_roi`` in the layout) for
        the specified row using pytesseract (PSM 6 — block of text) on a
        grayscale crop.  The dark grey text on a light background provides
        sufficient contrast without colour-replacement preprocessing.

        Args:
            row_num: 1-based row index; if None, auto-detects via
                     get_selected_row().

        Returns:
            datetime object, or None if extraction or parsing fails.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None

        row_y_tops = self.layout.get(self.row_y_tops_key, [])
        roi_cfg = self.layout.get("datetime_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            return None

        row_top = row_y_tops[row_num - 1]
        x = int(roi_cfg["x"] * self.factor)
        y = int((row_top + roi_cfg["y_offset"]) * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)

        roi = self.frame[y : y + h, x : x + w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        text = pytesseract.image_to_string(gray, config="--psm 6").strip()
        if not text:
            return None
        try:
            return datetime.strptime(text, "%m/%d/%Y %H:%M")
        except ValueError:
            return None

    def get_replay_id(self):
        """Return the Replay ID string from the replay details screen.

        Reads the replay ID text region (``replay_id_roi`` in the layout).
        The region contains white text on a dark background; a grayscale
        threshold inversion produces black text on white for pytesseract.

        Returns:
            Replay ID string (uppercase alphanumeric), or None if extraction fails.
        """
        roi_cfg = self.layout.get("replay_id_roi")
        if not roi_cfg:
            return None

        x = int(roi_cfg["x"] * self.factor)
        y = int(roi_cfg["y"] * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)

        roi = self.frame[y : y + h, x : x + w]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        # Otsu: white text → black, dark background → white
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # Upscale and re-binarise so Tesseract gets sharper strokes
        big = cv2.resize(thresh, (w * 2, h * 2), interpolation=cv2.INTER_LANCZOS4)
        _, big = cv2.threshold(big, 127, 255, cv2.THRESH_BINARY)
        padded = cv2.copyMakeBorder(big, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255)

        chars = roi_cfg.get("chars", "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        text = pytesseract.image_to_string(
            padded, config=f"--psm 7 -c tessedit_char_whitelist={chars}"
        )
        return text.strip() or None

    def get_match_type_from_selected_row(self, row_num=None):
        """Return the match type for the selected replay row.

        Samples the match-type badge region (``match_type_roi`` in the layout):
          - Red    badge (``ranked_color``)     → returns "ranked"
          - Purple badge (``custom_color``)     → returns "custom"
          - Blue   badge (``battle_hub_color``) → returns "battle_hub"

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            "ranked", "custom", "battle_hub", or None if no badge colour is detected.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None

        row_y_tops = self.layout.get(self.row_y_tops_key, [])
        roi_cfg = self.layout.get("match_type_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            return None

        row_top = row_y_tops[row_num - 1]
        x = int(roi_cfg["x"] * self.factor)
        y = int((row_top + roi_cfg["y_offset"]) * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)

        roi = self.frame[y : y + h, x : x + w]
        thr = roi_cfg.get("color_threshold", 30)
        min_px = roi_cfg.get("min_pixels", 5)

        ranked_count = CvHelper.count_color_in_roi(
            roi, roi_cfg["ranked_color"], threshold=thr
        )
        custom_count = CvHelper.count_color_in_roi(
            roi, roi_cfg["custom_color"], threshold=thr
        )
        battle_hub_count = CvHelper.count_color_in_roi(
            roi, roi_cfg["battle_hub_color"], threshold=thr
        )

        if ranked_count >= min_px:
            return "ranked"
        if custom_count >= min_px:
            return "custom"
        if battle_hub_count >= min_px:
            return "battle_hub"
        return None

    def _load_portrait_refs_for_side(self, portraits_dir, side):
        """Load and cache histogram-equalised grayscale reference portraits for one side."""
        if not hasattr(self, "_portrait_ref_cache"):
            self._portrait_ref_cache = {}
        key = (portraits_dir, side)
        if key not in self._portrait_ref_cache:
            refs = {}
            side_dir = os.path.join(portraits_dir, side)
            if os.path.isdir(side_dir):
                for fname in os.listdir(side_dir):
                    if fname.endswith(".png"):
                        char = fname[:-4]
                        img = cv2.imread(
                            os.path.join(side_dir, fname), cv2.IMREAD_GRAYSCALE
                        )
                        if img is not None:
                            refs[char] = cv2.equalizeHist(img)
            self._portrait_ref_cache[key] = refs
        return self._portrait_ref_cache[key]

    @staticmethod
    def _match_portrait(query_gray, refs_combined):
        """Return the best-matching character name using histogram-equalised NCC."""
        if not refs_combined:
            return None
        q_eq = cv2.equalizeHist(query_gray)
        qh, qw = q_eq.shape[:2]
        best_char, best_score = None, -99.0
        for char, (ref_eq, penalty) in refs_combined.items():
            rh, rw = ref_eq.shape[:2]
            # matchTemplate requires the reference to cover the whole ROI; a
            # badly cropped reference is skipped rather than crashing every lookup.
            if rh < qh or rw < qw:
                print(
                    f"WARN: portrait reference '{char}' is {rw}x{rh}, "
                    f"smaller than the {qw}x{qh} ROI — skipping"
                )
                continue
            score = (
                float(cv2.matchTemplate(q_eq, ref_eq, cv2.TM_CCOEFF_NORMED)[0, 0])
                - penalty
            )
            if score > best_score:
                best_score = score
                best_char = char
        return best_char

    def get_ringnames_from_selected_row(self, row_num=None):
        """Return (p1_ringname, p2_ringname) for the selected replay row via OCR.

        Extracts the P1 and P2 ringname regions defined by ``ringname_roi`` in
        the layout.  Both regions contain white text on a dark background; the
        preprocessing pipeline inverts and binarises so Tesseract receives black
        text on white.  ``lang='eng+jpn'`` handles both Latin and Japanese names.

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            ``(p1_ringname, p2_ringname)`` strings, or ``(None, None)`` on failure.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None, None

        row_y_tops = (
            self.layout.get(self.row_y_tops_key)
            or self.layout.get("row_y_tops_search")
            or []
        )
        roi_cfg = self.layout.get("ringname_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            return None, None

        row_top = row_y_tops[row_num - 1]
        y = int((row_top + roi_cfg.get("y_offset", 0)) * self.factor)
        h = int(roi_cfg["h"] * self.factor)
        p1_x = int(roi_cfg["p1_x"] * self.factor)
        p2_x = int(roi_cfg["p2_x"] * self.factor)
        p1_w = int(roi_cfg.get("p1_w", roi_cfg.get("w", 225)) * self.factor)
        p2_w = int(roi_cfg.get("p2_w", roi_cfg.get("w", 225)) * self.factor)

        def _ocr_ringname(roi):
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            rh, rw = gray.shape[:2]
            # 3× upscale preserves font anti-aliasing better than binarising first
            big = cv2.resize(gray, (rw * 3, rh * 3), interpolation=cv2.INTER_LANCZOS4)
            padded = cv2.copyMakeBorder(
                big, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255
            )
            text = pytesseract.image_to_string(
                padded, lang="eng+jpn", config="--psm 7"
            ).strip()
            # Tesseract inserts phantom spaces between CJK characters; remove them
            if re.search(r"[぀-ヿ一-鿿]", text):
                text = text.replace(" ", "")
            return text or None

        p1_roi = self.frame[y : y + h, p1_x : p1_x + p1_w]
        p2_roi = self.frame[y : y + h, p2_x : p2_x + p2_w]
        return _ocr_ringname(p1_roi), _ocr_ringname(p2_roi)

    def get_mr_from_selected_row(self, row_num=None):
        """Return (p1_mr, p2_mr) Master Rank integers for the selected replay row.

        Extracts the P1 and P2 MR regions defined by ``mr_roi`` in the layout
        and reads the digit-only content via pytesseract (PSM 6, digit whitelist).

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            ``(p1_mr, p2_mr)`` as integers, or ``(None, None)`` on failure.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None, None

        row_y_tops = (
            self.layout.get(self.row_y_tops_key)
            or self.layout.get("row_y_tops_search")
            or []
        )
        roi_cfg = self.layout.get("mr_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            return None, None

        row_top = row_y_tops[row_num - 1]
        y = int((row_top + roi_cfg["y_offset"]) * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)
        p1_x = int(roi_cfg["p1_x"] * self.factor)
        p2_x = int(roi_cfg["p2_x"] * self.factor)

        def _ocr_mr(roi):
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            rh, rw = gray.shape[:2]
            big = cv2.resize(gray, (rw * 3, rh * 3), interpolation=cv2.INTER_LANCZOS4)
            padded = cv2.copyMakeBorder(
                big, 20, 20, 20, 20, cv2.BORDER_CONSTANT, value=255
            )
            raw = pytesseract.image_to_string(
                padded, config="--psm 6 -c tessedit_char_whitelist=0123456789"
            ).strip()
            return int(raw) if raw.isdigit() else None

        p1_roi = self.frame[y : y + h, p1_x : p1_x + w]
        p2_roi = self.frame[y : y + h, p2_x : p2_x + w]
        return _ocr_mr(p1_roi), _ocr_mr(p2_roi)

    def get_characters_from_selected_row(self, row_num=None):
        """Return (p1_char, p2_char) for the selected replay row via portrait matching.

        Extracts the P1 and P2 portrait ROIs defined by ``portrait_roi`` in the
        layout, converts them to grayscale, applies histogram equalisation (so
        coloured winner and B&W loser portraits both match correctly), then picks
        the highest-scoring reference portrait from the per-side library stored in
        ``portrait_roi["portraits_dir"]``.

        When a character only has a reference on the opposite side (e.g. a character
        that always appeared as P1 in the training data) that cross-side reference is
        used with a small score penalty so same-side references are always preferred
        when available.

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            ``(p1_char, p2_char)`` tuple of lowercase character name strings, or
            ``(None, None)`` if the row cannot be located or no reference images
            are found.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            print("Selected row is none")
            return None, None

        row_y_tops = (
            self.layout.get(self.row_y_tops_key)
            or self.layout.get("row_y_tops_search")
            or []
        )
        cfg = self.layout.get("portrait_roi")
        if not cfg or row_num < 1 or row_num > len(row_y_tops):
            print("not cfg etc")
            return None, None

        row_top = row_y_tops[row_num - 1]
        y = int((row_top + cfg.get("y_offset", 0)) * self.factor)
        w = int(cfg["w"] * self.factor)
        h = int(cfg["h"] * self.factor)
        p1_x = int(cfg["p1_x"] * self.factor)
        p2_x = int(cfg["p2_x"] * self.factor)

        portraits_dir = cfg.get("portraits_dir", "")
        refs_p1 = self._load_portrait_refs_for_side(portraits_dir, "p1")
        refs_p2 = self._load_portrait_refs_for_side(portraits_dir, "p2")

        # Build combined lookups: same-side ref preferred, cross-side as fallback.
        _CROSS_PENALTY = 0.05
        all_chars = set(refs_p1) | set(refs_p2)
        combined_p1 = {
            c: (refs_p1[c], 0.0) if c in refs_p1 else (refs_p2[c], _CROSS_PENALTY)
            for c in all_chars
        }
        combined_p2 = {
            c: (refs_p2[c], 0.0) if c in refs_p2 else (refs_p1[c], _CROSS_PENALTY)
            for c in all_chars
        }

        p1_gray = cv2.cvtColor(
            self.frame[y : y + h, p1_x : p1_x + w], cv2.COLOR_BGR2GRAY
        )
        p2_gray = cv2.cvtColor(
            self.frame[y : y + h, p2_x : p2_x + w], cv2.COLOR_BGR2GRAY
        )

        return (
            self._match_portrait(p1_gray, combined_p1),
            self._match_portrait(p2_gray, combined_p2),
        )

    def is_bottom(self):
        """Return True if the scroll-down indicator pixel matches the expected colour.

        Reads ``bottom_indicator`` from the layout: a single pixel at (x, y) that
        is blue when more list entries exist below the current view.
        """
        cfg = self.layout.get("bottom_indicator")
        if not cfg:
            return False

        x = int(cfg["x"] * self.factor)
        y = int(cfg["y"] * self.factor)
        pixel = self.frame[y, x]
        target_bgr = CvHelper.hex_to_bgr(cfg["color"])
        return CvHelper.rgb_similarity(pixel, target_bgr) >= cfg.get("threshold", 0.95)

    def get_round_results(self):
        """Return winning round result icon names in round order.
        
        Only useable for Street Fighter 6

        Searches both the P1 and P2 icon columns defined by ``round_result_roi``
        in the layout.  For each round, the winner's icon (e.g. ``"p1_victory"``,
        ``"p2_chip_damage"``) is returned; ``*_loses`` icons are ignored.  Draw
        rounds return both ``"p1_draw"`` and ``"p2_draw"`` (one per column).

        Returns:
            List of icon name strings (without extension), sorted by round order.
            Draw rounds contribute two entries (p1_draw, p2_draw) per round.
        """
        cfg = self.layout.get("round_result_roi")
        if not cfg:
            return []

        icons_dir = cfg["icons_dir"]
        match_threshold = cfg.get("match_threshold", 0.9)
        nms_gap = max(1, int(25 * self.factor))
        x_pad_l = max(1, int(20 * self.factor))
        x_pad_r = max(1, int(40 * self.factor))
        y_pad = max(1, int(10 * self.factor))

        p1_templates, p2_templates = {}, {}
        for fname in os.listdir(icons_dir):
            if not fname.endswith(".png"):
                continue
            stem = fname[:-4]
            if stem.endswith("_loses"):
                continue
            img = cv2.imread(os.path.join(icons_dir, fname))
            if img is None:
                continue
            if self.factor != 1:
                h, w = img.shape[:2]
                img = cv2.resize(
                    img,
                    (max(1, int(w * self.factor)), max(1, int(h * self.factor))),
                )
            if stem.startswith("p1_"):
                p1_templates[stem] = img
            elif stem.startswith("p2_"):
                p2_templates[stem] = img

        p1_x = int(cfg["p1_x"] * self.factor)
        p2_x = int(cfg["p2_x"] * self.factor)
        col_y = int(cfg["y"] * self.factor)
        col_w = int(cfg["w"] * self.factor)
        col_h = int(cfg["h"] * self.factor)

        p1_det = self._find_winning_icons(
            self.frame, p1_x, col_y, col_w, col_h, p1_templates,
            x_pad_l, x_pad_r, y_pad, match_threshold, nms_gap,
        )
        p2_det = self._find_winning_icons(
            self.frame, p2_x, col_y, col_w, col_h, p2_templates,
            x_pad_l, x_pad_r, y_pad, match_threshold, nms_gap,
        )

        combined = p1_det + p2_det
        combined.sort()
        return [name for _, name in combined]

    @staticmethod
    def _find_winning_icons(frame, x, y, w, h, templates,
                            x_pad_l, x_pad_r, y_pad, threshold, nms_gap):
        """Match icon templates against a padded search region; return [(y_center, name)]."""
        fh, fw = frame.shape[:2]
        x_start = max(0, x - x_pad_l)
        x_end = min(fw, x + w + x_pad_r)
        y_start = max(0, y - y_pad)
        y_end = min(fh, y + h + y_pad)
        roi = frame[y_start:y_end, x_start:x_end]

        candidates = []
        for name, tmpl in templates.items():
            th, tw = tmpl.shape[:2]
            if th > roi.shape[0] or tw > roi.shape[1]:
                continue
            res = cv2.matchTemplate(roi, tmpl, cv2.TM_CCOEFF_NORMED)
            above_y, above_x = np.where(res >= threshold)
            for y_idx, x_idx in zip(above_y, above_x):
                y_abs = y_start + y_idx + th // 2
                candidates.append((float(res[y_idx, x_idx]), y_abs, name))

        candidates.sort(reverse=True)
        kept = []
        suppressed = set()
        for i, (sc, yy, nm) in enumerate(candidates):
            if i in suppressed:
                continue
            kept.append((yy, nm))
            for j, (sc2, yy2, nm2) in enumerate(candidates):
                if j != i and j not in suppressed and abs(yy2 - yy) < nms_gap:
                    suppressed.add(j)
        kept.sort()
        return kept
