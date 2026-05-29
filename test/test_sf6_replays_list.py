import sys
import os
import cv2
import pytest
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv.flexible_cv import FlexibleCv


@pytest.mark.parametrize(
    "filename, expected_row",
    [
        ("assets/test_images/sf6/replays_list_row_01.png", 1),
        ("assets/test_images/sf6/replays_list_row_02.png", 2),
        ("assets/test_images/sf6/replays_list_row_03.png", 3),
        ("assets/test_images/sf6/replays_list_row_04.png", 4),
        ("assets/test_images/sf6/replays_list_row_05.png", 5),
    ],
)
def test_get_selected_row(filename, expected_row):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.get_selected_row() == expected_row


@pytest.mark.parametrize(
    "filename",
    [
        "assets/test_images/sf6/replays_list_row_01.png",
        "assets/test_images/sf6/replays_list_row_02.png",
        "assets/test_images/sf6/replays_list_row_03.png",
        "assets/test_images/sf6/replays_list_row_04.png",
        "assets/test_images/sf6/replays_list_row_05.png",
    ],
)
def test_is_replays_list_screen(filename):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.is_match()


@pytest.mark.parametrize(
    "filename, expected_winner",
    [
        ("assets/test_images/sf6/replays_list_row_01.png", 2),  # P1 loses
        ("assets/test_images/sf6/replays_list_row_02.png", 2),  # P1 loses
        ("assets/test_images/sf6/replays_list_row_03.png", 1),  # P1 wins
        ("assets/test_images/sf6/replays_list_row_04.png", 1),  # P1 wins
        ("assets/test_images/sf6/replays_list_row_05.png", 2),  # P1 loses
    ],
)
def test_get_winner_from_selected_row(filename, expected_winner):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.get_winner_from_selected_row() == expected_winner


@pytest.mark.parametrize(
    "filename, expected_datetime",
    [
        ("assets/test_images/sf6/replays_list_row_01.png", datetime(2026, 5, 24, 10, 26)),
        ("assets/test_images/sf6/replays_list_row_02.png", datetime(2026, 5, 24, 10, 24)),
        ("assets/test_images/sf6/replays_list_row_03.png", datetime(2026, 5, 24, 10, 19)),
        ("assets/test_images/sf6/replays_list_row_04.png", datetime(2026, 5, 24, 10, 17)),
        ("assets/test_images/sf6/replays_list_row_05.png", datetime(2026, 5, 24, 10, 13)),
    ],
)
def test_get_datetime_from_selected_row(filename, expected_datetime):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.get_datetime_from_selected_row() == expected_datetime


@pytest.mark.parametrize(
    "filename, expected_type",
    [
        ("assets/test_images/sf6/replays_list_row_01.png",        "ranked"),
        ("assets/test_images/sf6/replays_list_row_02.png",        "ranked"),
        ("assets/test_images/sf6/replays_list_row_03.png",        "ranked"),
        ("assets/test_images/sf6/replays_list_row_04.png",        "ranked"),
        ("assets/test_images/sf6/replays_list_row_05.png",        "ranked"),
        ("assets/test_images/sf6/replays_list_row_04_custom.png",    "custom"),
        ("assets/test_images/sf6/replays_list_row_02_battle_hub.png", "battle_hub"),
    ],
)
def test_get_match_type_from_selected_row(filename, expected_type):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    assert cv.get_match_type_from_selected_row() == expected_type
