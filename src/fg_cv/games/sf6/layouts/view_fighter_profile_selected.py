# The "Details" popup opened from a replay details "View <ringname>'s Details"
# row, with its first item - "View Fighter Profile" - selected.
#
# A plain brightness check over the ROI is not enough: bright patches land there
# on plenty of unrelated screens.  What is distinctive is the vertical structure
# at the left edge of the selection bar - a dark blue cap above it, the bright
# bar itself, then the dark popup body below - so each band is checked
# separately.  Band y offsets are relative to the top of the ROI.
layout = {
    "menu_item_roi": {
        "x": 668,
        "y": 353,
        "w": 78,
        "h": 66,
        "bands": [
            # dark blue popup background above the bar, around (71, 43, 8)
            {"y0": 0, "y1": 4, "bgr_min": [40, 20, 0], "bgr_max": [105, 70, 30]},
            # the bright selection bar itself, around (229, 213, 201)
            {"y0": 8, "y1": 46, "bgr_min": [195, 180, 165], "bgr_max": [255, 255, 250]},
            # unselected row below the bar, around (47, 34, 23)
            {"y0": 55, "y1": 66, "bgr_min": [20, 12, 3], "bgr_max": [85, 65, 55]},
        ],
    },
}
