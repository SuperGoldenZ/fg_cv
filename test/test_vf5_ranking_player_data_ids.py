import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


def test_is_match_over():
    cv: FlexibleCv = FlexibleCv(game="vf5", layout_name="ranking_player_data_ids")
    filename = "assets/test_images/vf5/ranking_player_data_ids.png"

    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    cv.set_frame(frame)
    assert cv.is_match()
    ocr = cv.get_ocr_blocks()
    assert ocr["p2_id"] == "0002ee2f01f44129889f99c7af0647d9"
    assert ocr["p1_id"] == "0002db858f654a9d8df1ce2ec5d78ab2"

    print(ocr)
