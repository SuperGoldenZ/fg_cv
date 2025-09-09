import sys
import os
import cv2
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.combo_cv import ComboCv

p2_combo_test_data = [5, 10, 12, 13]


@pytest.mark.parametrize("hits", p2_combo_test_data)
def test_p2_combos(hits):
    combo_cv: ComboCv = ComboCv("sf6")
    frame = cv2.imread(f"assets/test_images/p2_combo_{hits:02}.png")
    combo_cv.set_frame(frame)
    assert combo_cv.is_combo_happening(frame) == 2
    assert combo_cv.get_combo_hits(frame, 2) == hits


def test_p1_combos():
    combo_cv: ComboCv = ComboCv("sf6")
    frame = cv2.imread("assets/test_images/p1_combo_09.png")
    combo_cv.set_frame(frame)
    assert combo_cv.is_combo_happening(frame) == 1

    assert combo_cv.get_combo_hits(frame, 1) == 9


combo_over_images = [
    "assets/test_images/sf6/not_combo_over_01.png",
    "assets/test_images/sf6/not_combo_over_02.png",
    "assets/test_images/sf6/not_combo_over_03.png",
    "assets/test_images/sf6/not_combo_over_04.png",
]


@pytest.mark.parametrize("filename", combo_over_images)
def test_not_combo_over(filename):
    combo_cv: ComboCv = ComboCv("sf6")
    frame = cv2.imread(filename)
    combo_cv.set_frame(frame)
    assert combo_cv.is_combo_happening(frame) != 0
