import sys
import os
import cv2
import pytest


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from fg_cv import FlexibleCv


def test_replay_top_selected():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_first_selected")
    filename = "assets/test_images/vf5/replay_top_selected.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


def test_replay_over_return():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_match_over_return")
    filename = "assets/test_images/vf5/replay_match_over_return_to_replay_list.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


def test_replay_over_return_no():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_match_over_return_no")
    filename = (
        "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png"
    )
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


def test_replay_over_return_yes():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_match_over_return_yes")
    filename = "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


def test_replay_menu_ready_for_play():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_ready_for_play")
    filename = "assets/test_images/vf5/replay_menu_ready_for_play.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


def test_replay_menu_ready_for_play_2():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_ready_for_play")
    filename = "assets/test_images/vf5/replay_menu_ready_for_play_02.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)
