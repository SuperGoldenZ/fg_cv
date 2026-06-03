import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


@pytest.mark.parametrize(
    "filename, expected_id",
    [
        ("assets/test_images/sf6/replay_details_screen_01.png", "DQ37BBCUX"),
        ("assets/test_images/sf6/replay_details_screen_02.png", "Q7JP9NBDU"),
        ("assets/test_images/sf6/replay_details_screen_03.png", "97CUASKWS"),
        ("assets/test_images/sf6/replay_details_screen_04.png", "SXJHQ45D4"),
    ],
)
def test_get_replay_id(filename, expected_id):
    cv = FlexibleCv(game="sf6", layout_name="replay_details")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.get_replay_id() == expected_id
