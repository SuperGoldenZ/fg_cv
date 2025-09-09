import importlib
from fg_cv.cv_helper import CvHelper
import cv2

class LifebarCv:
    def __init__(self, game):
        self.game = game
    
        self.layouts = importlib.import_module(
            f"fg_cv.games.{self.game}.layouts.lifebars"
        ).layouts
        
        self.frame = None
        
        self.cv_helper = CvHelper()

    def set_frame(self, frame) -> None:
        self.frame = frame
        self.set_factor()

    def set_factor(self):
        self.factor = 1

        if self.frame.shape[0] == 720:
            self.factor = 6 / 9

    def get_damage(self, playernum:int):
        count: int = 0

        block = self.layouts[playernum-1]
        x, y, w, h = block["x"], block["y"], block["w"], block["h"]
        roi = self.frame[y : y + h, x : x + w].copy()
        
        for color in self.layouts[playernum-1]["expected_colors"]:
            count += CvHelper.count_color_in_roi(roi=roi, hex_color=color, threshold=3)

        return count        
    
    def is_damage_happening(self):
        for playernum in [1, 2]:
            count: int = 0

            block = self.layouts[playernum-1]
            x, y, w, h = block["x"], block["y"], block["w"], block["h"]
            roi = self.frame[y : y + h, x : x + w].copy()
            
            for color in self.layouts[playernum-1]["expected_colors"]:
                count += CvHelper.count_color_in_roi(roi=roi, hex_color=color, threshold=7)

            if count > self.layouts[playernum-1]["damage_threshold"]:
                return playernum
            
        return False