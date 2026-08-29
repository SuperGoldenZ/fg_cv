import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


USER_CODE_DIR = "assets/test_images/sf6/user_code"

user_code_test_data = [
    [f"{USER_CODE_DIR}/player_details_01.png", "4065533546"],
    [f"{USER_CODE_DIR}/player_details_02.png", "3681349424"],
    [f"{USER_CODE_DIR}/player_details_03.png", "2431319348"],
    [f"{USER_CODE_DIR}/player_details_04.png", "4063081378"],
    [f"{USER_CODE_DIR}/player_details_05.png", "2035812521"],
    [f"{USER_CODE_DIR}/player_details_06.png", "3833467565"],
    [f"{USER_CODE_DIR}/player_details_07.png", "2035812521"],
    # screens with no Fighter Profile banner - the label guard rejects these
    [f"{USER_CODE_DIR}/p1_details_selected.png", None],
    [f"{USER_CODE_DIR}/p2_details_selected.png", None],
    [f"{USER_CODE_DIR}/view_fighter_profile_selected.png", None],
    ["assets/test_images/sf6/replay_details_screen_01.png", None],
    ["assets/test_images/sf6/match_over_01.png", None],
]


@pytest.mark.parametrize("filename,expected", user_code_test_data)
def test_get_user_code(filename, expected):
    cv = FlexibleCv(game="sf6", layout_name="player_details")

    assert os.path.isfile(filename)
    cv.set_frame(cv2.imread(filename))
    assert cv.get_user_code() == expected
