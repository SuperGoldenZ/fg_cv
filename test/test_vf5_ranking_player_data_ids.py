import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


match_over_test_data = [
    [
        "assets/test_images/vf5/ranking_player_data_ids.png",
        None,  # "0002db858f654a9d8df1ce2ec5d78ab2",
        "0002ee2f01f44129889f99c7af0647d9",
    ],
    [
        "assets/test_images/vf5/ranking_player_data_ids_01.png",
        "0002ad6cd4e6421bb79ccf2668e379cf",
        None,  # "0002ee2f01f44129889f99c7af0647d9",
    ],
    [
        "assets/test_images/vf5/ranking_player_data_ids_02.png",
        None,  # "0002db858f654a9d8df1ce2ec5d78ab2",
        "00025d8dbeba4637bcfd3cc278f8f4ee",
    ],
]


@pytest.mark.parametrize("filename,p1_id,p2_id", match_over_test_data)
def test_is_match_over(filename, p1_id, p2_id):
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name="ranking_player_data_ids")

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match()
    ocr = cv.get_ocr_blocks()

    if p2_id is not None:
        assert ocr["p2_id"] == p2_id

    if p1_id is not None:
        assert ocr["p1_id"] == p1_id

    print(ocr)
