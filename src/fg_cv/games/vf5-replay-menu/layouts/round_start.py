# Round-start intro screen: P1/P2 "recent history" box is only shown while
# the round-intro freeze / "ROUND N" text is on screen, so its solid red
# (P1) and blue (P2) bands are a much more reliable signal than generic
# HUD elements (black corners, name banners, health bar) that are also
# present during ordinary gameplay and previously caused false positives.
layout = {
    "expected_colors": [
        {"x": 120, "y": 785, "color": "#b00002"},
        {"x": 180, "y": 785, "color": "#b00002"},
        {"x": 240, "y": 785, "color": "#b00002"},
        {"x": 300, "y": 785, "color": "#b00002"},
        {"x": 1600, "y": 780, "color": "#1019cf"},
        {"x": 1650, "y": 780, "color": "#1019cf"},
        {"x": 1700, "y": 780, "color": "#1019cf"},
        {"x": 1750, "y": 780, "color": "#1019cf"},
    ],
    "unexpected_colors": [],
    "threshold": 6,
}
