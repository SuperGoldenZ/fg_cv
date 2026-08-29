# Fighter Profile ("player details") overlay, opened from the replay details
# panel via "View <ringname>'s Details".
#
# The overlay itself is skinned per player (banner art, title colours), so it
# is not reliable to probe directly.  The replay details panel behind it is:
# it stays on screen, dimmed, with the "View ..." row that was chosen still
# highlighted in blue while the other row stays dark.  Sampling the left edge
# of both rows therefore identifies the screen *and* whose profile is shown.
layout = {
    "player_details_roi": {
        "rois": {
            1: {"x": 566, "y": 707, "w": 130, "h": 55},
            2: {"x": 566, "y": 770, "w": 130, "h": 55},
        },
        # Mean BGR of the dimmed-but-highlighted row, e.g. (117, 62, 16).
        "highlight_bgr_min": [100, 50, 0],
        "highlight_bgr_max": [135, 75, 28],
        # Mean BGR of an unhighlighted row is around (39, 18, 13).  A bright
        # (undimmed) row means the replay details menu still has focus.
        "dim_bgr_max": [70, 40, 35],
    },
    # "User Code: ##########" line of the Fighter Profile banner.
    #
    # The banner art behind it changes per player, but the text is always white
    # with a dark outline, so keeping only near-white pixels leaves clean black
    # glyphs on white for OCR.  The label is a fixed string in a fixed font, so
    # it always occupies x offsets 8-110 and the ten digits 120-247; splitting
    # there lets the digits be read with a digits-only whitelist.
    "user_code_roi": {
        "x": 1196,
        "y": 221,
        "w": 285,
        "h": 41,
        # a pixel counts as text when every BGR channel is at least this bright
        "text_min_channel": 170,
        # pytesseract reads small glyphs better when they are scaled up
        "scale": 3,
        "label": {"x0": 0, "x1": 115, "expected": "usercode"},
        "digits": {"x0": 115, "x1": 260, "length": 10},
    },
}
