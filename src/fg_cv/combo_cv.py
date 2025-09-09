import importlib
import base64
import numpy as np

import cv2
from PIL import Image
from fg_cv.cv_helper import CvHelper


class ComboCv:
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(
            f"fg_cv.games.{game}.layouts.combo"
        ).layout
        self.cv_helper = CvHelper()

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_combo_happening(self, frame=None):
        if frame is not None:
            self.set_frame(frame)

        if self.frame is None:
            raise Exception("Frame not set")

        # Return true if game doesn't have combo display
        if len(self.layout["ocr_blocks"].items()) == 0:
            return True

        for block_name, block in self.layout["ocr_blocks"].items():
            count = 0

            x, y, w, h = block["x"], block["y"], block["w"], block["h"]
            roi = self.frame[y : y + h, x : x + w].copy()

            for color in block["colors"]:
                count += CvHelper.count_color_in_roi(roi, color, threshold=8)

            if count >= 7:
                return block_name

        return 0

    def get_combo_hits(self, frame, player_num):
        self.set_frame(frame)

        if self.frame is None:
            raise Exception("Frame not set")

        block = self.layout["ocr_blocks"][player_num]
        x, y, w, h = block["x"], block["y"], block["w"], block["h"]
        roi = self.frame[y : y + h, x : x + w].copy()

        result: str = CvHelper.ocr_from_block(
            roi, block, chars="0123456789", threshold=block["threshold"]
        )
        if result.isdigit():
            return int(result)

        return 0

    def extract_text(self):
        if self.frame is None:
            raise Exception("Frame not set")

        return self.cv_helper.ocr_from_blocks(self.frame, self.layout["ocr_blocks"])
