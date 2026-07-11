import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


match_over_test_data = [
    ["assets/test_images/vf5/player_data_01.png", True],
    ["assets/test_images/vf5/player_data_02.png", True],
    ["assets/test_images/vf5/ranking_player_data_ids_01.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids_02.png", False],
]


@pytest.mark.parametrize("filename,expected", match_over_test_data)
def test_player_data(filename, expected):
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name="player_data")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match() == expected
