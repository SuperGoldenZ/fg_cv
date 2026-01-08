import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


match_over_test_data = [
    [
        "assets/test_images/vf5/ranking_battle_log_01_selected.png",
        "10/26/2025 20:27",
        "10/26/2025 20:25",
        "10/19/2025 19:46",
    ],
]


@pytest.mark.parametrize(
    "filename,match1_datetime,match2_datetime,match3_datetime", match_over_test_data
)
def test_is_battle_log(filename, match1_datetime, match2_datetime, match3_datetime):
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name="battle_log")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match()
    ocr = cv.get_ocr_blocks()

    assert match1_datetime == ocr["match1_datetime"]
    assert match2_datetime == ocr["match2_datetime"]
    assert match3_datetime == ocr["match3_datetime"]

    print(ocr)


battle_log_no_matches_data = [
    [
        "player_data_battle_log_selected_no_matches",
        "assets/test_images/vf5/player_data_no_battle_log.png",
        True,
    ],
    [
        "player_data_battle_log_selected_no_matches",
        "assets/test_images/vf5/ranking_battle_log_01_selected.png",
        False,
    ],
    [
        "battle_log",
        "assets/test_images/vf5/player_data_no_battle_log.png",
        False,
    ],
]


@pytest.mark.parametrize(
    "layout_name, test_image_filename, expected_result", battle_log_no_matches_data
)
def test_battle_log_no_matches(layout_name, test_image_filename, expected_result):
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name=layout_name)

    assert os.path.isfile(test_image_filename)
    frame = cv2.imread(test_image_filename)
    cv.set_frame(frame)
    assert cv.is_match() == expected_result
