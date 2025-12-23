import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


downloading_complete_data = [
    ["assets/test_images/vf5/ranked_replay_download_complete.png", True],
    ["assets/test_images/vf5/ranking_player_data_ids.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids_01.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids_02.png", False],
]


@pytest.mark.parametrize("filename,expected", downloading_complete_data)
def test_is_downloading_complete(filename, expected):
    cv: FlexibleCv = FlexibleCv(
        game="vf5", layout_name="ranking_replay_download_complete"
    )

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match() == expected


downloading_data = [
    ["assets/test_images/vf5/ranked_replay_downloading.png", True],
    ["assets/test_images/vf5/ranked_replay_download_complete.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids_01.png", False],
    ["assets/test_images/vf5/ranking_player_data_ids_02.png", False],
]


@pytest.mark.parametrize("filename,expected", downloading_data)
def test_is_downloading(filename, expected):
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name="ranked_replay_downloading")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match() == expected
