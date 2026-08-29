import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


USER_CODE_DIR = "assets/test_images/sf6/user_code"

# (filename, player whose "View ...'s Details" menu item is selected, or None)
details_selected_test_data = [
    [f"{USER_CODE_DIR}/p1_details_selected.png", 1],
    [f"{USER_CODE_DIR}/p2_details_selected.png", 2],
    # "View YHC-<mochi>'s Details" is the selected row here
    ["assets/test_images/sf6/replay_details_screen_02.png", 2],
    # same menu, but the cursor is on another row
    ["assets/test_images/sf6/replay_details_screen_01.png", None],
    ["assets/test_images/sf6/replay_details_screen_03.png", None],
    ["assets/test_images/sf6/replay_details_screen_04.png", None],
    # the "Details" popup has taken focus off the menu
    [f"{USER_CODE_DIR}/view_fighter_profile_selected.png", None],
    # profile already open - row is dimmed blue, not a bright selection
    [f"{USER_CODE_DIR}/player_details_01.png", None],
    [f"{USER_CODE_DIR}/player_details_02.png", None],
    [f"{USER_CODE_DIR}/player_details_05.png", None],
    # unrelated SF6 screens
    ["assets/test_images/sf6/match_over_01.png", None],
    ["assets/test_images/sf6/match_over_06.png", None],
    ["assets/test_images/sf6/replays_list_row_01.png", None],
]


def _cv_for(filename):
    cv = FlexibleCv(game="sf6", layout_name="details_selected")
    assert os.path.isfile(filename)
    cv.set_frame(cv2.imread(filename))
    return cv


@pytest.mark.parametrize("filename,expected", details_selected_test_data)
def test_is_details_menu_selected(filename, expected):
    cv = _cv_for(filename)
    assert cv.is_details_menu_selected() == (expected is not None)


@pytest.mark.parametrize("filename,expected", details_selected_test_data)
def test_get_selected_details_menu_player(filename, expected):
    cv = _cv_for(filename)
    assert cv.get_selected_details_menu_player() == expected
