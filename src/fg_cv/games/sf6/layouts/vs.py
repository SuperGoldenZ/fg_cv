# General
P1_CHARACTER_COLORS = [
    "#f5e8e9",
    "#bf8691",
    "#f5e6e9",
    "#fce6e9",
    "#ffe3e9",
    "#ffe0ec",
    "#cb8392",
    "#f9f5f5",
    "#d69eb4",
    "#f5f3f1",
    "#efdee4",
    "#b20050",
    "#ebdfe1",
]

RANK_COLORS = [
    "#cec8b1",
    "#c7c7c7",
    "#c2ccc9",
]

LEGEND_COLORS = [
    "#ffffcf",
    "#ffffff",
]

CHARACTER_WIDTH = 250

layout = {
    "ocr_blocks": {
        "p1_character": {
            "x": 101,
            "y": 824,
            "w": 285,
            "h": 60,
            "colors": P1_CHARACTER_COLORS,
        },
        "p2_character": {
            "x": 1532,
            "y": 824,
            "w": 285,
            "h": 60,
            "colors": ["#e2e3f8", "#f5e6df"],
        },
        "p1_ringname": {
            "x": 330,
            "y": 905,
            "w": 367,
            "h": 40,
            "colors": ["#e8ddde", "#d9d2e0", "#c8bfca"],
        },
        "p2_ringname": {"x": 1346, "y": 905, "w": 367, "h": 40, "colors": ["#d6d4d7"]},
        #        "p1_rank": {
        #            "x": 22,
        #            "y": 990,
        #            "w": 227,
        #            "h": 38,
        #            "colors": RANK_COLORS,
        #        },
        #        "p2_rank": {
        #            "x": 1698,
        #            "y": 990,
        #            "w": 227,
        #            "h": 38,
        #            "colors": RANK_COLORS,
        #        },
        "p1_legend": {"x": 81, "y": 969, "w": 78, "h": 31, "colors": LEGEND_COLORS},
        "p2_legend": {"x": 1750, "y": 969, "w": 78, "h": 31, "colors": LEGEND_COLORS},
    },
    "expected_colors": [
        {"x": 900, "y": 297, "color": "#a100fd"},
        {"x": 1020, "y": 434, "color": "#a905fe"},
        {"x": 723, "y": 797, "color": "#ed0dff"},
        {"x": 1047, "y": 662, "color": "#ba00ff"},
        {"x": 713, "y": 800, "color": "#c700fd"},
        {"x": 1005, "y": 741, "color": "#3c007b"},
        {"x": 926, "y": 264, "color": "#4a01cd"},
        {"x": 695, "y": 618, "color": "#d605ff"},
        {"x": 695, "y": 618, "color": "#d605ff"},
        {"x": 912, "y": 299, "color": "#bf00ff"},
        {"x": 842, "y": 296, "color": "#b400fc"},
    ],
    "threshold": 2,
}
