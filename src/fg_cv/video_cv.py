import cv2

from fg_cv.vs_screen_extractor import VsScreenExtractor


class VideoCv:
    @staticmethod
    def find_vs_screen(video_path, vs: VsScreenExtractor):
        """
        Reads a local video file frame-by-frame using OpenCV and processes each frame.

        Parameters:
            video_path (str): Path to the local video file.
            process_frame_callback (function): Function to call for each frame.
                                            Signature: func(frame, frame_index, timestamp_sec)
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise FileNotFoundError(f"Could not open video file: {video_path}")

        frame_index = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        result = None

        while True:
            ret, frame = cap.read()
            if not ret:
                break  # No more frames

            timestamp_sec = frame_index / fps

            vs.set_frame(frame)

            if vs.is_vs_screen():
                result = frame
                break

            frame_index += 1

        cap.release()
        return result
