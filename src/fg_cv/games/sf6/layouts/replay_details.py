layout = {
    "expected_colors": [
        {"x": 100, "y": 55, "color": "#585858"},   # tab area is grey on details screen
        {"x": 200, "y": 110, "color": "#08304f"},  # header bar present on details screen
    ],
    "unexpected_colors": [
        {"x": 100, "y": 55, "color": "#ffffff"},   # replay list has white here — reject it
    ],
    "threshold": 2,
    "replay_id_roi": {
        "x": 400,
        "y": 145,
        "w": 142,
        "h": 46,
        "colors": ["#ffffff"],
        "chars": "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    },
}
