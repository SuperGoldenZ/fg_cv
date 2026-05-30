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


@pytest.mark.parametrize(
    "filename, expected_p1, expected_p2",
    [
        ("assets/test_images/sf6/replay_list_row_01/p1_aki_loses_vs_p2_luke.png", "aki", "luke"),
        ("assets/test_images/sf6/replay_list_row_01/p1_aki_loses_vs_p2_manon.png", "aki", "manon"),
        ("assets/test_images/sf6/replay_list_row_01/p1_aki_wins_vs_p2_manon.png", "aki", "manon"),
        ("assets/test_images/sf6/replay_list_row_01/p1_akuma_wins_vs_p2_alex.png", "akuma", "alex"),
        ("assets/test_images/sf6/replay_list_row_01/p1_alex_wins_vs_p2_ingrid.png", "alex", "ingrid"),
        ("assets/test_images/sf6/replay_list_row_01/p1_bison_loses_vs_p2_akuma.png", "bison", "akuma"),
        ("assets/test_images/sf6/replay_list_row_01/p1_bison_wins_vs_p2_marisa.png", "bison", "marisa"),
        ("assets/test_images/sf6/replay_list_row_01/p1_blanka_wins_vs_p2_deejay.png", "blanka", "deejay"),
        ("assets/test_images/sf6/replay_list_row_01/p1_cammy_loses_vs_p2_ryu.png", "cammy", "ryu"),
        ("assets/test_images/sf6/replay_list_row_01/p1_cammy_wins_vs_p2_alex.png", "cammy", "alex"),
        ("assets/test_images/sf6/replay_list_row_01/p1_chunli_wins_vs_p2_zangief.png", "chunli", "zangief"),
        ("assets/test_images/sf6/replay_list_row_01/p1_deejay_wins_vs_p2_chunli.png", "deejay", "chunli"),
        ("assets/test_images/sf6/replay_list_row_01/p1_dhalsim_wins_vs_p2_juri.png", "dhalsim", "juri"),
        ("assets/test_images/sf6/replay_list_row_01/p1_ed_wins_vs_p2_ken.png", "ed", "ken"),
        ("assets/test_images/sf6/replay_list_row_01/p1_guile_wins_vs_p2_akuma.png", "guile", "akuma"),
        ("assets/test_images/sf6/replay_list_row_01/p1_ingrid_loses_vs_p2_jamie.png", "ingrid", "jamie"),
        ("assets/test_images/sf6/replay_list_row_01/p1_ingrid_wins_vs_p2_sagat.png", "ingrid", "sagat"),
        ("assets/test_images/sf6/replay_list_row_01/p1_jamie_wins_vs_p2_bison.png", "jamie", "bison"),
        ("assets/test_images/sf6/replay_list_row_01/p1_jp_loses_vs_p2_ingrid.png", "jp", "ingrid"),
        ("assets/test_images/sf6/replay_list_row_01/p1_jp_wins_vs_p2_sagat.png", "jp", "sagat"),
        ("assets/test_images/sf6/replay_list_row_01/p1_juri_wins_vs_p2_akuma.png", "juri", "akuma"),
        ("assets/test_images/sf6/replay_list_row_01/p1_ken_wins_vs_p2_ingrid.png", "ken", "ingrid"),
        ("assets/test_images/sf6/replay_list_row_01/p1_kimberly_wins_vs_p2_ken.png", "kimberly", "ken"),
        ("assets/test_images/sf6/replay_list_row_01/p1_lily_wins_vs_p2_elena.png", "lily", "elena"),
        ("assets/test_images/sf6/replay_list_row_01/p1_mai_loses_vs_p2_ingrid.png", "mai", "ingrid"),
        ("assets/test_images/sf6/replay_list_row_01/p1_manon_loses_vs_p2_ken.png", "manon", "ken"),
        ("assets/test_images/sf6/replay_list_row_01/p1_manon_wins_vs_p2_ryu.png", "manon", "ryu"),
        ("assets/test_images/sf6/replay_list_row_01/p1_marisa_loses_vs_p2_honda.png", "marisa", "honda"),
        ("assets/test_images/sf6/replay_list_row_01/p1_marisa_wins_vs_p2_jamie.png", "marisa", "jamie"),
        ("assets/test_images/sf6/replay_list_row_01/p1_rashid_wins_vs_p2_juri.png", "rashid", "juri"),
        ("assets/test_images/sf6/replay_list_row_01/p1_sagat_wins_vs_p2_ryu.png", "sagat", "ryu"),
        ("assets/test_images/sf6/replay_list_row_01/p1_sagat_wins_vs_p2_viper.png", "sagat", "viper"),
        ("assets/test_images/sf6/replay_list_row_01/p1_terry_loses_vs_p2_mai.png", "terry", "mai"),
        ("assets/test_images/sf6/replay_list_row_01/p1_terry_wins_vs_p2_juri.png", "terry", "juri"),
        ("assets/test_images/sf6/replay_list_row_01/p1_viper_wins_vs_p2_ingrid.png", "viper", "ingrid"),
        ("assets/test_images/sf6/replay_list_row_01/p1_zangief_loses_vs_p2_elena.png", "zangief", "elena"),
        ("assets/test_images/sf6/replay_list_row_01/p1_zangief_win_vs_p2_kimberly.png", "zangief", "kimberly"),
    ],
)
def test_get_characters_from_selected_row(filename, expected_p1, expected_p2):
    cv = FlexibleCv(game="sf6", layout_name="replays_list")
    frame = cv2.imread(filename)
    assert frame is not None, f"Could not load image: {filename}"
    cv.set_frame(frame)
    p1, p2 = cv.get_characters_from_selected_row()
    assert p1 == expected_p1
    assert p2 == expected_p2
