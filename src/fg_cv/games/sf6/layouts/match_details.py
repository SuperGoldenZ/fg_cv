layout = {
    "expected_colors": [
        {"x": 100, "y": 55, "color": "#585858"},   # tab area is grey on details screen
        {"x": 200, "y": 110, "color": "#08304f"},  # header bar present on details screen
    ],
    "unexpected_colors": [
        {"x": 100, "y": 55, "color": "#ffffff"},   # replay list has white here — reject it
    ],
    "threshold": 2,
    "round_result_roi": {
        "p1_x": 886,
        "p2_x": 994,
        "y": 256,
        "w": 62,
        "h": 197,
        "icons_dir": "assets/sf6/round_result_icons",
        "match_threshold": 0.9,
    },
}
