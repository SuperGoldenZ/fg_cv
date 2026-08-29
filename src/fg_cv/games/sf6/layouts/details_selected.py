# "View <ringname>'s Details" rows of the SF6 replay details menu, used to tell
# whether one of them is the currently selected menu item.
#
# The selected row is drawn as a bright near-white bar (mean BGR around
# (187, 173, 163)) while every unselected row stays dark (around (37, 29, 23)).
#
# This is the menu *before* the profile opens.  Once the Fighter Profile overlay
# is up the whole panel dims and the chosen row turns blue instead - see
# layouts/player_details.py.
layout = {
    "player_details_roi": {
        "rois": {
            1: {"x": 566, "y": 707, "w": 130, "h": 55},
            2: {"x": 566, "y": 770, "w": 130, "h": 55},
        },
        "highlight_bgr_min": [150, 140, 130],
        "highlight_bgr_max": [230, 220, 215],
        "dim_bgr_max": [70, 60, 55],
    },
}
