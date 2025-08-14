import importlib
import numpy as np
import math
from fg_cv.cv_helper import CvHelper


class VsScreenExtractor:
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(f"fg_cv.games.{game}.layouts.vs").layout

    def set_frame(self, frame) -> None:
        self.frame = frame

    def is_vs_screen(self):
        if self.frame is None:
            raise Exception("Frame not set")

        for color in self.layout["fixed_colors"]:
            pixel_color = self.frame[color["y"], color["x"]]
            target_bgr = CvHelper.hex_to_bgr(color["color"])

            if CvHelper.rgb_similarity(pixel_color, target_bgr) < 0.9:
                return False

        return True
