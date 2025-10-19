import sys
import os
import cv2
import pytest
import pathlib
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.round_start_screen_extractor import RoundStartScreenExtractor



test_images = glob.glob("assets/test_images/sf6/round_start/*png")

@pytest.mark.parametrize("filename", test_images)
def test_round_start(filename):
    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread(filename)
    round_start.set_frame(frame)
    assert round_start.is_round_start_screen()


def test_is_not_found_start():
    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/match_over.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()

    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/cammy_vs_elena.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()

    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/ryu_vs_luke.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()

    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/ed_luke_round_over.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()


def test_final_round_start():
    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/final_round_01.png")
    round_start.set_frame(frame)
    assert round_start.is_round_start_screen()


def test_ko_not_round_start():
    round_start = RoundStartScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/ko_01.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()

    frame = cv2.imread("assets/test_images/ko_02.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()

    frame = cv2.imread("assets/test_images/kimberly.png")
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()
