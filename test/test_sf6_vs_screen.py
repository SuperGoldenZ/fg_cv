import sys
import os
import cv2
import pytest
import glob
from pathlib import Path

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor


vs_screen_images = glob.glob("assets/test_images/sf6/vs_screen/*")

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}

not_vs_screen_images = [
    str(p)
    for p in Path("assets/test_images/sf6").rglob("*")
    if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS and "vs_screen" not in p.parts
]


@pytest.mark.parametrize("filename", vs_screen_images)
def test_is_vs_screen(filename):
    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    vs.set_frame(frame)
    assert vs.is_vs_screen()


@pytest.mark.parametrize("filename", not_vs_screen_images)
def test_not_vs_screen(filename):
    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    vs.set_frame(frame)
    assert not vs.is_vs_screen()
