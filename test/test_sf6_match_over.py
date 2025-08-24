import sys
import os
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.vs_screen_extractor import VsScreenExtractor
from fg_cv.match_over_extractor import MatchOverExtractor
        
def test_is_match_over():
    mo = MatchOverExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/match_over.png")
    mo.set_frame(frame)    
    assert(mo.is_match_over_screen())    
    
    mo = MatchOverExtractor(game="sf6")
    frame = cv2.imread("assets/test_images/match_over_02.png")
    mo.set_frame(frame)    
    assert(mo.is_match_over_screen())    

    frame = cv2.imread("assets/test_images/cammy_vs_elena.png")
    mo.set_frame(frame)    
    assert(not mo.is_match_over_screen())