import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor

match_over_test_data = [
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
    "assets/test_images/vf5/vs_screen_wolf_vanessa.png",
    "assets/test_images/vf5/vs_screen_aoi_leifei.png",
]


@pytest.mark.parametrize("filename", match_over_test_data)
def test_is_match_over(filename):
    vs = VsScreenExtractor(game="vf5")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    vs.set_frame(frame)
    assert vs.is_vs_screen()


not_match_over_test_data = [
    "assets/test_images/vf5/match_over_01.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png",
    "assets/test_images/vf5/splash_screen_ws.png",
    "assets/test_images/vf5/replay_top_selected.png",
]


@pytest.mark.parametrize("filename", not_match_over_test_data)
def test_is_not_match_over(filename):
    vs = VsScreenExtractor(game="vf5")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    vs.set_frame(frame)
    assert not vs.is_vs_screen()
