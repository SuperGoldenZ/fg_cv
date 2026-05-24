import importlib
from datetime import datetime
from fg_cv.cv_helper import CvHelper
import cv2
import pytesseract


class FlexibleCv:
    def __init__(self, game, layout_name="first_99"):
        self.game = game

        self.layout = importlib.import_module(
            f"fg_cv.games.{self.game}.layouts.{layout_name}"
        ).layout

        self.frame = None

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

        row_y_tops = self.layout.get("row_y_tops", [])
        roi_cfg = self.layout.get("p1_result_roi")
        if not roi_cfg or row_num < 1 or row_num > len(row_y_tops):
            return None

        row_top = row_y_tops[row_num - 1]
        x = int(roi_cfg["x"] * self.factor)
        y = int((row_top + roi_cfg["y_offset"]) * self.factor)
        w = int(roi_cfg["w"] * self.factor)
        h = int(roi_cfg["h"] * self.factor)

        roi = self.frame[y : y + h, x : x + w]
        thr = roi_cfg.get("color_threshold", 20)
        min_px = roi_cfg.get("min_pixels", 5)

        win_count = CvHelper.count_color_in_roi(roi, roi_cfg["win_color"], threshold=thr)
        lose_count = CvHelper.count_color_in_roi(roi, roi_cfg["lose_color"], threshold=thr)

        if win_count >= min_px:
            return 1  # P1 wins
        if lose_count >= min_px:
            return 2  # P2 wins
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

        row_y_tops = self.layout.get("row_y_tops", [])
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

    def get_match_type_from_selected_row(self, row_num=None):
        """Return the match type for the selected replay row.

        Samples the match-type badge region (``match_type_roi`` in the layout):
          - Red   badge (``ranked_color``) → returns "ranked"
          - Purple badge (``custom_color``) → returns "custom"

        Args:
            row_num: 1-based row index; if None, auto-detects via get_selected_row().

        Returns:
            "ranked", "custom", or None if no badge colour is detected.
        """
        if row_num is None:
            row_num = self.get_selected_row()
        if row_num is None:
            return None

        row_y_tops = self.layout.get("row_y_tops", [])
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

        ranked_count = CvHelper.count_color_in_roi(roi, roi_cfg["ranked_color"], threshold=thr)
        custom_count = CvHelper.count_color_in_roi(roi, roi_cfg["custom_color"], threshold=thr)

        if ranked_count >= min_px:
            return "ranked"
        if custom_count >= min_px:
            return "custom"
        return None
