layout = {
    "expected_colors": [
        {"x": 100,  "y": 55,  "color": "#ffffff"},  # tab bar white element
        {"x": 100,  "y": 90,  "color": "#03040a"},  # below tabs dark background
        {"x": 1800, "y": 200, "color": "#4a5892"},  # right side blue panel
        {"x": 1850, "y": 55,  "color": "#5b6eb7"},  # far-right tab area blue
    ],
    "unexpected_colors": [],
    "threshold": 3,
    # Row selection detection: at x=selected_x, the selected row has a bright
    # background (brightness > brightness_threshold) while unselected rows are dark.
    "row_y_centers": [304, 429, 554, 679, 804],
    "selected_x": 1296,
    "brightness_threshold": 150,
    # Absolute y of each row's top edge (used to locate ROIs within a row)
    "row_y_tops": [242, 367, 492, 617, 742],
    # P1 result text region: blue = P1 wins, grey = P1 loses
    "p1_result_roi": {
        "x": 609,
        "y_offset": 42,          # pixels below the row's top edge
        "w": 82,
        "h": 45,
        "win_color":  "#0d65d6", # P1 wins  → blue text
        "lose_color": "#49494d", # P1 loses → grey text
        "color_threshold": 20,   # ± per channel tolerance
        "min_pixels": 5,         # min matching pixels to confirm
    },
    # Match-type badge region (right side of each row)
    "match_type_roi": {
        "x": 1334,
        "y_offset": 38,             # pixels below the row's top edge
        "w": 30,
        "h": 20,
        "ranked_color": "#b12138",  # red badge   → "ranked"
        "custom_color": "#6200e3",  # purple badge → "custom"
        "color_threshold": 30,      # ± per channel tolerance
        "min_pixels": 5,            # min matching pixels to confirm
    },
    # Date/time text region (top-right of each row)
    "datetime_roi": {
        "x": 1530,
        "y_offset": 5,              # pixels below the row's top edge
        "w": 275,
        "h": 50,
        "chars": " 0123456789:/",   # whitelist — date/time characters only
    },
}
