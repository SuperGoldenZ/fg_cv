import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor_base import VsScreenExtractorBase
from fg_cv.vf5_revo.vs_screen_extractor import VsScreenExtractor

def test_get_ringnames():
    test = VsScreenExtractor()