import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from fg_cv import vs_screen_extractor
from fg_cv.video_cv import VideoCv


def main():
    vs = vs_screen_extractor.VsScreenExtractor("sf6")
    result = VideoCv.find_vs_screen(
        "D:/Users/Public/Videos/sf6-2025-08-12_19-37-32.mkv", vs=vs
    )

    cv2.imshow("found vs screen from video", result)
    cv2.waitKey()


if __name__ == "__main__":
    main()
