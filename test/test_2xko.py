import sys
import os
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))


from fg_cv.flexible_cv import FlexibleCv

ready_test_data = [
    "assets/test_images/2xko/ready_01.png",
]


@pytest.mark.parametrize("filename", ready_test_data)
def test_is_match_over(filename):
    ready_cv:FlexibleCv = FlexibleCv("2xko", "ready")
    frame = cv2.imread(filename)
    ready_cv.set_frame(frame)
    assert ready_cv.is_match()
