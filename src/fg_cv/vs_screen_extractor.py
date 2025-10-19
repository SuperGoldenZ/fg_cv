import importlib
import base64
import numpy as np

from PIL import Image
from fg_cv.cv_helper import CvHelper


class VsScreenExtractor:
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(f"fg_cv.games.{game}.layouts.vs").layout
        self.cv_helper = CvHelper()
        self.game = game

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_vs_screen(self, frame=None):
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

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.9:
                count += 1

        return count > self.layout["threshold"]

    def extract_text(self):
        if self.frame is None:
            raise Exception("Frame not set")

        if not "ocr_blocks" in self.layout:
            return {
                "p1_ringname": "n/a",
                "p2_ringname": "n/a",
                "p1_character": "n/a",
                "p2_character": "n/a",
            }

        result = self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])
        if self.game == "sf6" and "LEGEND" in result["p1_class"].upper():
            result["p1_class"] = "LEGEND"
        if self.game == "sf6" and "LEGEND" in result["p2_class"].upper():
            result["p2_class"] = "LEGEND"

        result["p1_class"] = result["p1_class"].upper()
        result["p2_class"] = result["p2_class"].upper()

        if self.game == "sf6" and not "LEGEND" in result["p1_class"]:
            result["p1_rank"] = ""

        if self.game == "sf6" and not "LEGEND" in result["p2_class"]:
            result["p2_rank"] = ""

        return result
