import sys
import os
import re
import cv2
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv

# Test filenames use 'over_drive'; icon files use 'od' (p1) and 'overdrive' (p2)
_RESULT_ALIASES = {
    "p1_over_drive": "p1_od",
    "p2_over_drive": "p2_overdrive",
}


def _parse_round_results(path):
    """Parse expected round results from a filename like 'p1_perfect_p2_victory_p1_victory.png'."""
    stem = os.path.splitext(os.path.basename(path))[0]
    parts = re.sub(r"_(p[12]_)", r"||\1", stem).split("||")
    return [_RESULT_ALIASES.get(p, p) for p in parts if p]


test_data = [
    "assets/test_images/sf6/match_details/p1_chip_damage_p1_critical_art.png",
    "assets/test_images/sf6/match_details/p1_draw_p2_draw_p1_draw_p2_draw.png",
    "assets/test_images/sf6/match_details/p1_over_drive_p2_perfect_p1_victory.png",
    "assets/test_images/sf6/match_details/p1_perfect_p2_victory_p1_victory.png",
    "assets/test_images/sf6/match_details/p2_chip_damage_p2_victory.png",
    "assets/test_images/sf6/match_details/p2_super_art_p1_victory_p1_over_drive.png",
    "assets/test_images/sf6/match_details/p2_victory_p1_victory_p2_over_drive.png",
    "assets/test_images/sf6/match_details/p2_victory_p2_critical_art.png",
]


@pytest.mark.parametrize("filename", test_data)
def test_get_round_results(filename):
    expected = _parse_round_results(filename)
    cv = FlexibleCv(game="sf6", layout_name="match_details")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    result = cv.get_round_results()
    assert result == expected    
