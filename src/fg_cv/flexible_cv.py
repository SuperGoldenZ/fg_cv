import importlib
import os
import re
from datetime import datetime
from fg_cv.cv_helper import CvHelper
import cv2
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
        row_y_centers = self.layout.get("row_y_centers", [])
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
        """Return the winning player number (1 or 2) for the selected replay row.

        Examines the P1 result text region (defined by ``p1_result_roi`` in the
        layout) within the specified row:
          - Blue  pixels (``win_color``)  → P1 wins  → returns 1
          - Grey  pixels (``lose_color``) → P2 wins  → returns 2

        Args:
            row_num: 1-based row index to examine; if None, auto-detects via
                     get_selected_row().

        Returns:
            1, 2, or None (if no colour matched / no row is selected).
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
        x = int(roi_cfg["x"] * self.factor)
        y = int((row_top + roi_cfg["y_offset"]) * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)

        roi = self.frame[y : y + h, x : x + w]
        thr = roi_cfg.get("color_threshold", 25)
        min_px = roi_cfg.get("min_pixels", 5)

        win_count = CvHelper.count_color_in_roi(
            roi, roi_cfg["win_color"], threshold=thr
        )
        lose_count = CvHelper.count_color_in_roi(
            roi, roi_cfg["lose_color"], threshold=thr
        )

        if win_count >= min_px:
            return 1  # P1 wins
        if lose_count >= min_px:
            return 2  # P2 wins

        print(
            f"could not get winner {win_count} {lose_count} .... {min_px}, returning None"
        )
        cv2.imshow("roi with no player", roi)
        cv2.waitKey(0)
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
        best_char, best_score = None, -99.0
        for char, (ref_eq, penalty) in refs_combined.items():
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
