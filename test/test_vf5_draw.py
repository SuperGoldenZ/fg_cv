import sys
import os
import cv2
import pytest
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.draw_screen_extractor import DrawScreenExtractor


true_positive_images = glob.glob("assets/test_images/vf5/round_end_draws/*.png")

negative_images = [
    f
    for f in glob.glob("assets/test_images/vf5/**/*", recursive=True)
    if os.path.isfile(f)
    and "round_end_draws/" not in f.replace(os.sep, "/")
    and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
]


@pytest.mark.parametrize("filename", true_positive_images)
def test_is_draw_screen(filename):
    draw = DrawScreenExtractor(game="vf5")
    frame = cv2.imread(filename)
    draw.set_frame(frame)
    assert draw.is_draw_screen()


@pytest.mark.parametrize("filename", negative_images)
def test_is_not_draw_screen(filename):
    draw = DrawScreenExtractor(game="vf5")
    frame = cv2.imread(filename)
    draw.set_frame(frame)
    assert not draw.is_draw_screen()
