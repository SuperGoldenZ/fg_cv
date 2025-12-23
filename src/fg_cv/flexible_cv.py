import importlib
from fg_cv.cv_helper import CvHelper
import cv2


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
                return False

        # print(f"got count {count} vs {self.layout["threshold"]}")
        return count >= self.layout["threshold"]

    def get_ocr_blocks(self):
        return self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])

    def get_ocr_block_names(self):
        return list(self.layout["ocr_blocks"].keys())

    def get_ocr_values(self):
        return self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])
