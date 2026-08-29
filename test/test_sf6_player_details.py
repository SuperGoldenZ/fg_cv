import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


USER_CODE_DIR = "assets/test_images/sf6/user_code"

# (filename, expected player whose Fighter Profile is open, or None)
player_details_test_data = [
    [f"{USER_CODE_DIR}/player_details_01.png", 1],
    [f"{USER_CODE_DIR}/player_details_02.png", 2],
    [f"{USER_CODE_DIR}/player_details_03.png", 1],
    [f"{USER_CODE_DIR}/player_details_04.png", 2],
    [f"{USER_CODE_DIR}/player_details_05.png", 1],
    [f"{USER_CODE_DIR}/player_details_06.png", 2],
    [f"{USER_CODE_DIR}/player_details_07.png", 1],
    # replay details menu still has focus - the row is bright, not dimmed
    [f"{USER_CODE_DIR}/p1_details_selected.png", None],
    [f"{USER_CODE_DIR}/p2_details_selected.png", None],
    # the intermediate "Details" popup, before the profile opens
    [f"{USER_CODE_DIR}/view_fighter_profile_selected.png", None],
    # unrelated SF6 screens
    ["assets/test_images/sf6/match_over_01.png", None],
    ["assets/test_images/sf6/match_over_06.png", None],
    ["assets/test_images/sf6/replay_details_screen_01.png", None],
    ["assets/test_images/sf6/replay_details_screen_04.png", None],
    ["assets/test_images/sf6/replays_list_row_01.png", None],
]


def _cv_for(filename):
    cv = FlexibleCv(game="sf6", layout_name="player_details")
    assert os.path.isfile(filename)
    cv.set_frame(cv2.imread(filename))
    return cv


@pytest.mark.parametrize("filename,expected", player_details_test_data)
def test_is_player_details_screen(filename, expected):
    cv = _cv_for(filename)
    assert cv.is_player_details_screen() == (expected is not None)


@pytest.mark.parametrize("filename,expected", player_details_test_data)
def test_get_player_details_player(filename, expected):
    cv = _cv_for(filename)
    assert cv.get_player_details_player() == expected
