import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor
from fg_cv.match_over_extractor import MatchOverExtractor

match_over_test_data = [
    "assets/test_images/sf6/match_over_01.png",
    "assets/test_images/sf6/match_over_02.png",
    "assets/test_images/match_over.png",
    "assets/test_images/match_over_02.png",
]


@pytest.mark.parametrize("filename", match_over_test_data)
def test_is_match_over(filename):
    mo = MatchOverExtractor(game="sf6")
    frame = cv2.imread(filename)
    mo.set_frame(frame)
    assert mo.is_match_over_screen()


not_match_over_test_data = [
    "assets/test_images/sf6/not_match_over_01.png",
    "assets/test_images/sf6/not_match_over_02.png",
    "assets/test_images/sf6/not_match_over_03.png",
    "assets/test_images/sf6/not_match_over_04.png",
    "assets/test_images/mai_vs_juri.png",
]


@pytest.mark.parametrize("filename", not_match_over_test_data)
def test_not_match_over(filename: str):
    print(filename)
    mo = MatchOverExtractor(game="sf6")
    frame = cv2.imread(filename)
    mo.set_frame(frame)
    assert not mo.is_match_over_screen()
