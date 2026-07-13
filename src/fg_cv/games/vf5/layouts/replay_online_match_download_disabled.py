# Online replay Play/Download submenu with the Download option highlighted
# but greyed out (replay cannot be downloaded, e.g. it was already
# downloaded or downloaded-replay storage is full). Same probe points as
# replay_online_match_download; the disabled state renders at roughly 45%
# brightness, far outside the 0.86 similarity window of the enabled colors.
layout = {
    "expected_colors": [
        {"x": 785, "y": 563, "color": "#6b4003"},
        {"x": 801, "y": 585, "color": "#6e4204"},
        {"x": 1157, "y": 566, "color": "#6b3004"},
        {"x": 1151, "y": 584, "color": "#6e3304"},
    ],
    "unexpected_colors": [],
    "threshold": 3,
}
