import sys
import os
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor
from fg_cv.match_over_extractor import MatchOverExtractor


def test_is_vs():
    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/cammy_vs_elena.png")
    vs.set_frame(frame)
    assert vs.is_vs_screen()

    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/mai_vs_juri.png")
    vs.set_frame(frame)
    assert vs.is_vs_screen()


def test_vs_screen_ocr_1():
    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/cammy_vs_elena.png")
    vs.set_frame(frame)
    text = vs.extract_text()
    assert text["p1_character"] == "CAMMY"
    assert text["p2_character"] == "ELENA"
    assert text["p1_ringname"] == "Kazunoko"
    assert text["p2_ringname"] == "路易十二" or text["p2_ringname"] == "路易十三"
    assert text["p1_legend"] == "85th"
    assert text["p2_legend"] == "137th"
    assert "LEGEND" in text["p1_class"].upper()
    assert "LEGEND" in text["p2_class"].upper()


def test_vs_screen_ocr_2():
    vs = VsScreenExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/blanka_vs_chun_li.png")
    vs.set_frame(frame)
    text = vs.extract_text()    
    assert text["p1_character"] == "BLANKA"
    assert text["p2_character"] == "CHUN-LI"
    assert text["p1_ringname"] == "プロミネンスリボルト"
    assert text["p2_ringname"] == "Mniki"
    assert text["p1_class"] ==  "MASTER"
    assert text["p2_class"] ==  "HIGH MASTER"
    

def test_is_match_over():
    mo = MatchOverExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/match_over.png")
    mo.set_frame(frame)
    assert mo.is_match_over_screen()

    frame = cv2.imread("assets/test_images/cammy_vs_elena.png")
    mo.set_frame(frame)
    assert not mo.is_match_over_screen()
