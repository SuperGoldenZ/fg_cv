import os
import sys
import cv2

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from fg_cv import vs_screen_extractor
from fg_cv import match_over_extractor
from fg_cv.video_cv import VideoCv


def main():
    match_over = match_over_extractor.MatchOverExtractor("sf6")
    #test_
    
    vs = vs_screen_extractor.VsScreenExtractor("sf6")
    result = VideoCv.find_vs_screen(
        "D:/Users/Public/next_upload/sf6-dj-sagat2025-08-17_13-12-08.mkv", vs=vs
        #"D:/Users/Public/next_upload/sf6-dhalsim-ryu-2025-08-17_13-07-33.mkv", vs=vs
    )

    print(vs.extract_text())
    cv2.imshow("found vs screen from video", result)
    cv2.waitKey()

    exit()
    result = VideoCv.find_vs_screen(
        "D:/Users/Public/next_upload/sf6-2025-08-12_19-37-32.mkv", vs=vs
    )

    vs.set_frame(result)
    print (vs.extract_text())
    cv2.imshow("found vs screen from video", result)
    cv2.waitKey()

    result = VideoCv.find_vs_screen(
        "D:/Users/Public/Videos/sf6-Cammy vs Elena.mp4", vs=vs
    )

    cv2.imshow("found vs screen from video", result)
    cv2.waitKey()


if __name__ == "__main__":
    main()
