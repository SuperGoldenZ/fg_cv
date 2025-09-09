import sys
import os
import cv2
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.lifebar_cv import LifebarCv

test_data_1 = [(5, 1878, 0), (10, 0, 0), (12, 0, 0), (13, 0, 0)]


@pytest.mark.parametrize("hits,expected_damage_p1,expected_damage_p2", test_data_1)
def test_p2_combos(hits, expected_damage_p1, expected_damage_p2):
    frame = cv2.imread(f"assets/test_images/p2_combo_{hits:02}.png")
    lifebar_cv: LifebarCv = LifebarCv("sf6")

    lifebar_cv.set_frame(frame)
    p1_damage = lifebar_cv.get_damage(1)
    p2_damage = lifebar_cv.get_damage(2)
    print(f"{hits} hits , {expected_damage_p1} , {expected_damage_p2}")
    assert expected_damage_p1 == p1_damage, "p1 damage not as expected"
    assert expected_damage_p2 == p2_damage, "p2 damage not as expected"
    

test_data_2 = [("09", 0, 10200)]


@pytest.mark.parametrize("hits,expected_damage_p1,expected_damage_p2", test_data_2)
def test_p1_combos(hits, expected_damage_p1, expected_damage_p2):
    frame = cv2.imread(f"assets/test_images/p1_combo_{hits:02}.png")
    lifebar_cv: LifebarCv = LifebarCv("sf6")

    lifebar_cv.set_frame(frame)
    p1_damage = lifebar_cv.get_damage(1)
    p2_damage = lifebar_cv.get_damage(2)
    print(f"{hits} hits , {expected_damage_p1} , {expected_damage_p2}")
    assert expected_damage_p1 == p1_damage, "p1 damage not as expected"
    assert expected_damage_p2 == p2_damage, "p2 damage not as expected"