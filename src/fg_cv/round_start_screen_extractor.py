import importlib
from fg_cv.cv_helper import CvHelper


class RoundStartScreenExtractor:
    """
    Abstract base class for extracting VS screen data.
    All game-specific extractors must implement these methods.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(
            f"fg_cv.games.{game}.layouts.round_start"
        ).layout
        self.cv_helper = CvHelper()

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_round_start_screen(self, frame=None):
        if frame is not None:
            self.set_frame(frame=frame)

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

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.91:
                count += 1

        for color in self.layout["unexpected_colors"]:
            if self.factor == 1:
                pixel_color = self.frame[color["y"], color["x"]]
            else:
                pixel_color = self.frame[
                    int(color["y"] * self.factor), int(color["x"] * self.factor)
                ]

            target_bgr = CvHelper.hex_to_bgr(color["color"])

            if CvHelper.rgb_similarity(pixel_color, target_bgr) >= 0.90:
                self.frame = None
                return False

        self.frame = None
        return count >= 5
