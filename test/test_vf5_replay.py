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


def test_replay_menu():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu")
    filename = "assets/test_images/vf5/replay_menu_ready_for_play.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)

    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_ready_for_play")
    filename = "assets/test_images/vf5/replay_menu_ready_for_play_02.png"
    assert os.path.isfile(filename)

    frame = cv2.imread(filename)
    assert cv.is_match(frame)


ready_for_play_test_data = [
    "assets/test_images/vf5/replay_menu_ready_for_play.png",
    "assets/test_images/vf5/replay_menu_ready_for_play_02.png",
]


@pytest.mark.parametrize("filename", ready_for_play_test_data)
def test_replay_menu_ready_for_play(filename):
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_ready_for_play")
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert cv.is_match(frame)


not_ready_for_play_test_data = [
    "assets/test_images/vf5/match_over_01.png",
    "assets/test_images/vf5/replay_match_over_02.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png",
    "assets/test_images/vf5/replay_top_selected.png",
    "assets/test_images/vf5/splash_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/main_screen_01.png",
    "assets/test_images/vf5/replay_accessing.png",
    "assets/test_images/vf5/replay_menu_online_selected.png",
    "assets/test_images/vf5/ranking_screen_worldwide_selected.png",
    "assets/test_images/vf5/ranking_screen_receiving.png",
    "assets/test_images/vf5/ranking_player_data.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
    "assets/test_images/vf5/ranked_replay_download_complete.png",
    "assets/test_images/vf5/ranked_replay_downloading.png",
    "assets/test_images/vf5/ranking_battle_log_01_selected.png",
    "assets/test_images/vf5/ranking_player_data_ids.png",
    "assets/test_images/vf5/ranking_player_data_ids_01.png",
    "assets/test_images/vf5/ranking_player_data_ids_02.png",
    "assets/test_images/vf5/vs_screen_aoi_leifei.png",
    "assets/test_images/vf5/vs_screen_wolf_vanessa.png",
    "assets/test_images/vf5/leaderboard.png",
    "assets/test_images/vf5/leaderboard_loading.png",
    "assets/test_images/vf5/leaderboard_no_entry.png",
    "assets/test_images/vf5/player_data_01.png",
    "assets/test_images/vf5/player_data_02.png",
    "assets/test_images/vf5/leaderboard_deleted.png",
    "assets/test_images/vf5/player_data_deleted.png",
    "assets/test_images/vf5/player_data_no_battle_log.png",
    "assets/test_images/vf5/battle_log_01.png",
    "assets/test_images/vf5/player_data_03.png",
    "assets/test_images/vf5/battle_log_02.png",
    "assets/test_images/vf5/battle_log_03.png",
    "assets/test_images/vf5/replay_online_match_download.png",
    "assets/test_images/vf5/replay_online_match_loading.png",
    "assets/test_images/vf5/replay_submenu_delete_selected.png",
    "assets/test_images/vf5/sure_delete_replay_no.png",
    "assets/test_images/vf5/sure_delete_replay_yes.png",
]


@pytest.mark.parametrize("filename", not_ready_for_play_test_data)
def test_not_replay_menu_ready_for_play(filename):
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_menu_ready_for_play")
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert not cv.is_match(frame)


def test_replay_submenu_delete_selected():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_submenu_delete_selected")
    filename = "assets/test_images/vf5/replay_submenu_delete_selected.png"
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert cv.is_match(frame)


not_delete_selected_test_data = [
    "assets/test_images/vf5/match_over_01.png",
    "assets/test_images/vf5/replay_match_over_02.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png",
    "assets/test_images/vf5/replay_top_selected.png",
    "assets/test_images/vf5/splash_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/main_screen_01.png",
    "assets/test_images/vf5/replay_accessing.png",
    "assets/test_images/vf5/replay_menu_online_selected.png",
    "assets/test_images/vf5/replay_menu_ready_for_play.png",
    "assets/test_images/vf5/replay_menu_ready_for_play_02.png",
    "assets/test_images/vf5/ranking_screen_worldwide_selected.png",
    "assets/test_images/vf5/ranking_screen_receiving.png",
    "assets/test_images/vf5/ranking_player_data.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
    "assets/test_images/vf5/ranked_replay_download_complete.png",
    "assets/test_images/vf5/ranked_replay_downloading.png",
    "assets/test_images/vf5/ranking_battle_log_01_selected.png",
    "assets/test_images/vf5/ranking_player_data_ids.png",
    "assets/test_images/vf5/ranking_player_data_ids_01.png",
    "assets/test_images/vf5/ranking_player_data_ids_02.png",
    "assets/test_images/vf5/vs_screen_aoi_leifei.png",
    "assets/test_images/vf5/vs_screen_wolf_vanessa.png",
    "assets/test_images/vf5/leaderboard.png",
    "assets/test_images/vf5/leaderboard_loading.png",
    "assets/test_images/vf5/leaderboard_no_entry.png",
    "assets/test_images/vf5/player_data_01.png",
    "assets/test_images/vf5/player_data_02.png",
    "assets/test_images/vf5/leaderboard_deleted.png",
    "assets/test_images/vf5/player_data_deleted.png",
    "assets/test_images/vf5/player_data_no_battle_log.png",
    "assets/test_images/vf5/battle_log_01.png",
    "assets/test_images/vf5/player_data_03.png",
    "assets/test_images/vf5/battle_log_02.png",
    "assets/test_images/vf5/battle_log_03.png",
    "assets/test_images/vf5/replay_online_match_download.png",
    "assets/test_images/vf5/replay_online_match_loading.png",
    "assets/test_images/vf5/sure_delete_replay_no.png",
    "assets/test_images/vf5/sure_delete_replay_yes.png",
]


@pytest.mark.parametrize("filename", not_delete_selected_test_data)
def test_not_replay_submenu_delete_selected(filename):
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "replay_submenu_delete_selected")
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert not cv.is_match(frame)


delete_replay_no_test_data = [
    "assets/test_images/vf5/sure_delete_replay_no.png",
    "assets/test_images/vf5/sure_delete_replay_no_02.png"
]

@pytest.mark.parametrize("filename", delete_replay_no_test_data)
def test_sure_delete_replay_no(filename):    
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "sure_delete_replay_no")    
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert cv.is_match(frame)


not_sure_delete_replay_no_test_data = [
    "assets/test_images/vf5/match_over_01.png",
    "assets/test_images/vf5/replay_match_over_02.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png",
    "assets/test_images/vf5/replay_top_selected.png",
    "assets/test_images/vf5/splash_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/main_screen_01.png",
    "assets/test_images/vf5/replay_accessing.png",
    "assets/test_images/vf5/replay_menu_online_selected.png",
    "assets/test_images/vf5/replay_menu_ready_for_play.png",
    "assets/test_images/vf5/replay_menu_ready_for_play_02.png",
    "assets/test_images/vf5/ranking_screen_worldwide_selected.png",
    "assets/test_images/vf5/ranking_screen_receiving.png",
    "assets/test_images/vf5/ranking_player_data.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
    "assets/test_images/vf5/ranked_replay_download_complete.png",
    "assets/test_images/vf5/ranked_replay_downloading.png",
    "assets/test_images/vf5/ranking_battle_log_01_selected.png",
    "assets/test_images/vf5/ranking_player_data_ids.png",
    "assets/test_images/vf5/ranking_player_data_ids_01.png",
    "assets/test_images/vf5/ranking_player_data_ids_02.png",
    "assets/test_images/vf5/vs_screen_aoi_leifei.png",
    "assets/test_images/vf5/vs_screen_wolf_vanessa.png",
    "assets/test_images/vf5/leaderboard.png",
    "assets/test_images/vf5/leaderboard_loading.png",
    "assets/test_images/vf5/leaderboard_no_entry.png",
    "assets/test_images/vf5/player_data_01.png",
    "assets/test_images/vf5/player_data_02.png",
    "assets/test_images/vf5/leaderboard_deleted.png",
    "assets/test_images/vf5/player_data_deleted.png",
    "assets/test_images/vf5/player_data_no_battle_log.png",
    "assets/test_images/vf5/battle_log_01.png",
    "assets/test_images/vf5/player_data_03.png",
    "assets/test_images/vf5/battle_log_02.png",
    "assets/test_images/vf5/battle_log_03.png",
    "assets/test_images/vf5/replay_online_match_download.png",
    "assets/test_images/vf5/replay_online_match_loading.png",
    "assets/test_images/vf5/replay_submenu_delete_selected.png",
    "assets/test_images/vf5/sure_delete_replay_yes.png",
]


@pytest.mark.parametrize("filename", not_sure_delete_replay_no_test_data)
def test_not_sure_delete_replay_no(filename):
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "sure_delete_replay_no")
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert not cv.is_match(frame)


def test_sure_delete_replay_yes():
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "sure_delete_replay_yes")
    filename = "assets/test_images/vf5/sure_delete_replay_yes.png"
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert cv.is_match(frame)


not_sure_delete_replay_yes_test_data = [
    "assets/test_images/vf5/match_over_01.png",
    "assets/test_images/vf5/replay_match_over_02.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_no_selected.png",
    "assets/test_images/vf5/replay_match_over_return_to_replay_list_yes_selected.png",
    "assets/test_images/vf5/replay_top_selected.png",
    "assets/test_images/vf5/splash_screen_ws.png",
    "assets/test_images/vf5/vs_screen_ws.png",
    "assets/test_images/vf5/main_screen_01.png",
    "assets/test_images/vf5/replay_accessing.png",
    "assets/test_images/vf5/replay_menu_online_selected.png",
    "assets/test_images/vf5/replay_menu_ready_for_play.png",
    "assets/test_images/vf5/replay_menu_ready_for_play_02.png",
    "assets/test_images/vf5/ranking_screen_worldwide_selected.png",
    "assets/test_images/vf5/ranking_screen_receiving.png",
    "assets/test_images/vf5/ranking_player_data.png",
    "assets/test_images/vf5/vs_screen_ws_2p_wolf.png",
    "assets/test_images/vf5/ranked_replay_download_complete.png",
    "assets/test_images/vf5/ranked_replay_downloading.png",
    "assets/test_images/vf5/ranking_battle_log_01_selected.png",
    "assets/test_images/vf5/ranking_player_data_ids.png",
    "assets/test_images/vf5/ranking_player_data_ids_01.png",
    "assets/test_images/vf5/ranking_player_data_ids_02.png",
    "assets/test_images/vf5/vs_screen_aoi_leifei.png",
    "assets/test_images/vf5/vs_screen_wolf_vanessa.png",
    "assets/test_images/vf5/leaderboard.png",
    "assets/test_images/vf5/leaderboard_loading.png",
    "assets/test_images/vf5/leaderboard_no_entry.png",
    "assets/test_images/vf5/player_data_01.png",
    "assets/test_images/vf5/player_data_02.png",
    "assets/test_images/vf5/leaderboard_deleted.png",
    "assets/test_images/vf5/player_data_deleted.png",
    "assets/test_images/vf5/player_data_no_battle_log.png",
    "assets/test_images/vf5/battle_log_01.png",
    "assets/test_images/vf5/player_data_03.png",
    "assets/test_images/vf5/battle_log_02.png",
    "assets/test_images/vf5/battle_log_03.png",
    "assets/test_images/vf5/replay_online_match_download.png",
    "assets/test_images/vf5/replay_online_match_loading.png",
    "assets/test_images/vf5/replay_submenu_delete_selected.png",
    "assets/test_images/vf5/sure_delete_replay_no.png",
]


@pytest.mark.parametrize("filename", not_sure_delete_replay_yes_test_data)
def test_not_sure_delete_replay_yes(filename):
    cv: FlexibleCv = FlexibleCv("vf5-replay-menu", "sure_delete_replay_yes")
    assert os.path.isfile(filename)
    frame = cv2.imread(filename)
    assert not cv.is_match(frame)
