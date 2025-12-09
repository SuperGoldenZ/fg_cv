import sys
import os
import cv2
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv import FlexibleCv


def test_replay_top_selected():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_first_selected")
    frame = cv2.imread("assets/images/vf5/replay_top_selected.png")
    assert cv.is_match(frame)
