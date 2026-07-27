# Round-end "DRAW" banner: large green (with lighter/darker green shading)
# outlined text centered on screen. A simple ROI pixel-color-count is
# reliable here since the color palette is distinct from anything else
# that appears in that screen region (verified against every other VF5
# test image, including the round-start "ROUND"/"READY" gold banner text
# which overlaps the same screen area).
#
# The "RING OUT" banner uses the exact same green palette and vertical
# position, but is a wider string of text, so it also lights up the
# center ROI above. The flanking ROIs below sit just outside where
# "DRAW" text ever reaches but land squarely on the "R"/"T" of
# "RING OUT", so requiring them to be (almost) empty of the green
# palette rejects "RING OUT" while never rejecting real "DRAW" frames.
layout = {
    "roi": {"x": 593, "y": 459, "w": 737, "h": 186},
    "expected_colors": ["#36a708", "#9ff377", "#037e14"],
    "color_tolerance": 15,
    "threshold": 1000,
    "unexpected_rois": [
        {"x": 420, "y": 459, "w": 170, "h": 186},
        {"x": 1335, "y": 459, "w": 170, "h": 186},
    ],
    "unexpected_threshold": 60,
}
