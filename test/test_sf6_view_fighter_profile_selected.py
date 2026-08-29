import sys
import os
import glob
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


USER_CODE_DIR = "assets/test_images/sf6/user_code"
TARGET = f"{USER_CODE_DIR}/view_fighter_profile_selected.png"

view_fighter_profile_test_data = [
    [TARGET, True],
    # the replay details menu the popup is opened from
    [f"{USER_CODE_DIR}/p1_details_selected.png", False],
    [f"{USER_CODE_DIR}/p2_details_selected.png", False],
    # the Fighter Profile the popup leads to
    [f"{USER_CODE_DIR}/player_details_01.png", False],
    [f"{USER_CODE_DIR}/player_details_02.png", False],
    [f"{USER_CODE_DIR}/player_details_03.png", False],
    [f"{USER_CODE_DIR}/player_details_04.png", False],
    [f"{USER_CODE_DIR}/player_details_05.png", False],
    [f"{USER_CODE_DIR}/player_details_06.png", False],
    [f"{USER_CODE_DIR}/player_details_07.png", False],
    # other SF6 screens
    ["assets/test_images/sf6/replay_details_screen_01.png", False],
    ["assets/test_images/sf6/replay_details_screen_02.png", False],
    ["assets/test_images/sf6/replays_list_row_01.png", False],
    ["assets/test_images/sf6/replays_list_row_02.png", False],
    ["assets/test_images/sf6/match_over_01.png", False],
    ["assets/test_images/sf6/not_match_over_05.png", False],
]


def _cv_for(filename):
    cv = FlexibleCv(game="sf6", layout_name="view_fighter_profile_selected")
    assert os.path.isfile(filename)
    cv.set_frame(cv2.imread(filename))
    return cv


@pytest.mark.parametrize("filename,expected", view_fighter_profile_test_data)
def test_is_view_fighter_profile_selected(filename, expected):
    assert _cv_for(filename).is_view_fighter_profile_selected() == expected


def test_no_false_positives_across_all_test_images():
    """The whole assets/test_images tree must hold exactly one match.

    2XKO images are excluded - they are a different game entirely and are not
    frames this SF6 detection would ever be handed.
    """
    files = sorted(
        filename
        for filename in glob.glob("assets/test_images/**/*.png", recursive=True)
        + glob.glob("assets/test_images/**/*.jpg", recursive=True)
        if not any(
            part.startswith("2xko")
            for part in filename.replace(os.sep, "/").split("/")
        )
    )
    assert TARGET in files

    cv = FlexibleCv(game="sf6", layout_name="view_fighter_profile_selected")
    matched = []
    for filename in files:
        frame = cv2.imread(filename)
        if frame is None:
            continue
        cv.set_frame(frame)
        if cv.is_view_fighter_profile_selected():
            matched.append(filename)

    assert matched == [TARGET]
