import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor

match_over_test_data = [
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
]


@pytest.mark.parametrize("filename", match_over_test_data)
def test_is_match_over(filename):
    vs = VsScreenExtractor(game="vf5")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    vs.set_frame(frame)
    assert vs.is_vs_screen()
