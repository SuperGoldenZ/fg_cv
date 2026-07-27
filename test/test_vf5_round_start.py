import sys
import os
import cv2
import pytest
import glob

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.round_start_screen_extractor import RoundStartScreenExtractor


true_positive_images = glob.glob("assets/test_images/vf5/round_start_screens/*.png")
false_positive_images = glob.glob(
    "assets/test_images/vf5/round_start_screen_false_positives/*.png"
)


@pytest.mark.parametrize("filename", true_positive_images)
def test_round_start(filename):
    round_start = RoundStartScreenExtractor(game="vf5")
    frame = cv2.imread(filename)
    round_start.set_frame(frame)
    assert round_start.is_round_start_screen()


@pytest.mark.parametrize("filename", false_positive_images)
def test_not_round_start_false_positives(filename):
    round_start = RoundStartScreenExtractor(game="vf5")
    frame = cv2.imread(filename)
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()


def test_not_round_start_during_match_overlay():
    round_start = RoundStartScreenExtractor(game="vf5")
    frame = cv2.imread(
        "assets/test_images/vf5/during_match_replay_round_control_overlay.png"
    )
    round_start.set_frame(frame)
    assert not round_start.is_round_start_screen()
