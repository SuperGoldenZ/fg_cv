import importlib
import numpy as np
import pytesseract
from PIL import Image
from fg_cv.cv_helper import CvHelper


class MatchOverExtractor:
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(
            f"fg_cv.games.{game}.layouts.match_over"
        ).layout

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_match_over_screen(self, frame=None):
        if frame is not None:
            self.frame = frame
            self.set_factor()

        if self.frame is None:
            raise Exception("Frame not set")

        count: int = 0

        for color in self.layout["fixed_colors"]:
            if self.factor == 1:
                pixel_color = self.frame[color["y"], color["x"]]
            else:
                pixel_color = self.frame[
                    int(color["y"] * self.factor), int(color["x"] * self.factor)
                ]

            target_bgr = CvHelper.hex_to_bgr(color["color"])

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.95:
                count += 1

        return count > 5
