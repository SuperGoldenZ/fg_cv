import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.extractor_factory import ExtractorFactory


def test_sf6_vs():
    vs = ExtractorFactory.get_vs_screen_extractor("sf6")


def test_vf5_revo_vs():
    vs = ExtractorFactory.get_vs_screen_extractor("vf5_revo")
