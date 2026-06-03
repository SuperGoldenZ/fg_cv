layout = {
    "expected_colors": [
        {"x": 100,  "y": 55,  "color": "#ffffff"},  # tab bar white — only on replay list
        {"x": 100,  "y": 90,  "color": "#04050c"},  # below tabs dark background
        {"x": 1800, "y": 200, "color": "#4a5892"},  # right blue panel (upper)
        {"x": 1850, "y": 55,  "color": "#5b6eb7"},  # far-right tab area blue
        {"x": 1820, "y": 400, "color": "#2a345e"},  # right blue panel (mid)
        {"x": 1820, "y": 600, "color": "#282f4b"},  # right blue panel (lower)
    ],
    "unexpected_colors": [],
    "threshold": 6,
    # Row selection detection: at x=selected_x, the selected row has a bright
    # background (brightness > brightness_threshold) while unselected rows are dark.
    "row_y_centers": [304, 429, 554, 679, 804],
    "selected_x": 1296,
    "brightness_threshold": 150,
    # Absolute y of each row's top edge (used to locate ROIs within a row)
    "row_y_tops": [242, 367, 492, 617, 742],
    "row_y_tops_favorite_players": [242 - 35, 367 - 35, 492 - 35, 617 - 35, 742 - 35],
    "row_y_tops_search": [242, 367, 492, 617, 742],
    # P1 result text region: blue = P1 wins, grey = P1 loses
    "p1_result_roi": {
        "x": 609,
        "y_offset": 42,  # pixels below the row's top edge
        "w": 82,
        "h": 45,
        "win_color": "#0d65d6",  # P1 wins  → blue text
        "lose_color": "#49494d",  # P1 loses → grey text
        "color_threshold": 20,  # ± per channel tolerance
        "min_pixels": 5,  # min matching pixels to confirm
    },
    # Match-type badge region (right side of each row)
    "match_type_roi": {
        "x": 1334,
        "y_offset": 38,  # pixels below the row's top edge
        "w": 30,
        "h": 20,
        "ranked_color": "#b12138",  # red badge    → "ranked"
        "custom_color": "#6200e3",  # purple badge → "custom"
        "battle_hub_color": "#0d65d6",  # blue badge   → "battle_hub"
        "color_threshold": 30,  # ± per channel tolerance
        "min_pixels": 5,  # min matching pixels to confirm
    },
    # Date/time text region (top-right of each row)
    "datetime_roi": {
        "x": 1530,
        "y_offset": 5,  # pixels below the row's top edge
        "w": 275,
        "h": 50,
        "chars": " 0123456789:/",  # whitelist — date/time characters only
    },
    # Player MR (Master Rank) number regions — digits only
    "mr_roi": {
        "p1_x": 332,
        "p2_x": 1167,
        "y_offset": 45,
        "w": 62,
        "h": 50,
    },
    # Player ringname text regions (dark text on bright row background)
    "ringname_roi": {
        "p1_x": 216,
        "p2_x": 1050,
        "y_offset": 0,
        "p1_w": 225,
        "p2_w": 200,  # narrower: rank badge starts ~50px before 225 on the P2 side
        "h": 50,
    },
    # Character portrait regions (one per side, no flip needed)
    # Winner has a coloured portrait; loser has a black-and-white portrait.
    # Matching uses grayscale + histogram equalisation so both states work.
    "portrait_roi": {
        "p1_x": 465,
        "p2_x": 843,
        "y_offset": 0,   # pixels below the row's top edge
        "w": 145,
        "h": 118,
        "portraits_dir": "assets/sf6/character_portraits",
    },
}
