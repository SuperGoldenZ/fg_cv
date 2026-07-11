"""
Build SF6 character portrait reference images from labelled test images.

Extracts a 145x118 crop for each character from both the P1 (x=465) and P2
(x=843) portrait slots.  For each character and slot, the image with the
highest HSV saturation (i.e. the coloured winner portrait) is preferred so
that references capture maximum visual detail.

Output:
    assets/sf6/character_portraits/p1/<char>.png
    assets/sf6/character_portraits/p2/<char>.png

Run from the project root:
    python tools/build_sf6_character_portraits.py
"""

import os
import re
import cv2
import numpy as np

SOURCE_DIR = "assets/test_images/sf6/replay_list_row_01"
OUT_DIR = "assets/sf6/character_portraits"
P1_X, P2_X, Y, W, H = 465, 843, 242, 145, 118
PATTERN = re.compile(r"p1_(.+?)_(wins|win|loses)_vs_p2_(.+)\.png")


def saturation(crop):
    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
    return float(hsv[:, :, 1].mean())


def main():
    os.makedirs(os.path.join(OUT_DIR, "p1"), exist_ok=True)
    os.makedirs(os.path.join(OUT_DIR, "p2"), exist_ok=True)

    best_p1 = {}  # char -> (crop, sat)
    best_p2 = {}  # char -> (crop, sat)

    for fname in sorted(os.listdir(SOURCE_DIR)):
        m = PATTERN.match(fname)
        if not m:
            continue
        p1c, result, p2c = m.group(1), m.group(2), m.group(3)
        img = cv2.imread(os.path.join(SOURCE_DIR, fname))

        p1_crop = img[Y : Y + H, P1_X : P1_X + W]
        p1_sat = saturation(p1_crop)
        if p1c not in best_p1 or p1_sat > best_p1[p1c][1]:
            best_p1[p1c] = (p1_crop.copy(), p1_sat)

        p2_crop = img[Y : Y + H, P2_X : P2_X + W]
        p2_sat = saturation(p2_crop)
        if p2c not in best_p2 or p2_sat > best_p2[p2c][1]:
            best_p2[p2c] = (p2_crop.copy(), p2_sat)

    for char, (crop, sat) in sorted(best_p1.items()):
        path = os.path.join(OUT_DIR, "p1", f"{char}.png")
        cv2.imwrite(path, crop)
        print(f"  p1/{char}.png  (sat={sat:.1f})")

    for char, (crop, sat) in sorted(best_p2.items()):
        path = os.path.join(OUT_DIR, "p2", f"{char}.png")
        cv2.imwrite(path, crop)
        print(f"  p2/{char}.png  (sat={sat:.1f})")

    print(f"\nWrote {len(best_p1)} P1 and {len(best_p2)} P2 reference portraits.")


if __name__ == "__main__":
    main()
