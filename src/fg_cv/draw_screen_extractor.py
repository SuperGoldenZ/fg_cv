import importlib
from fg_cv.cv_helper import CvHelper


class DrawScreenExtractor:
    """
    Detects the round-end "DRAW" banner screen.
    """

    def __init__(self, game):
        self.frame = None
        self.layout = importlib.import_module(
            f"fg_cv.games.{game}.layouts.draw"
        ).layout

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def is_draw_screen(self, frame=None):
        if frame is not None:
            self.set_frame(frame=frame)

        if self.frame is None:
            raise Exception("Frame not set")

        roi_cfg = self.layout["roi"]
        x, y, w, h = roi_cfg["x"], roi_cfg["y"], roi_cfg["w"], roi_cfg["h"]

        if self.factor != 1:
            x, y, w, h = (
                int(x * self.factor),
                int(y * self.factor),
                int(w * self.factor),
                int(h * self.factor),
            )

        roi = self.frame[y : y + h, x : x + w]

        count = 0
        for color in self.layout["expected_colors"]:
            count += CvHelper.count_color_in_roi(
                roi, color, threshold=self.layout["color_tolerance"]
            )

        if count < self.layout["threshold"]:
            return False

        for flank in self.layout.get("unexpected_rois", []):
            fx, fy, fw, fh = flank["x"], flank["y"], flank["w"], flank["h"]

            if self.factor != 1:
                fx, fy, fw, fh = (
                    int(fx * self.factor),
                    int(fy * self.factor),
                    int(fw * self.factor),
                    int(fh * self.factor),
                )

            flank_roi = self.frame[fy : fy + fh, fx : fx + fw]

            flank_count = 0
            for color in self.layout["expected_colors"]:
                flank_count += CvHelper.count_color_in_roi(
                    flank_roi, color, threshold=self.layout["color_tolerance"]
                )

            if flank_count > self.layout["unexpected_threshold"]:
                return False

        return True
