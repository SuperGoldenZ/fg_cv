import math
import pytesseract

import cv2
import numpy as np
from openai import OpenAI
import base64
import os


class CvHelper:
    API_KEY = None
    if os.path.isfile(".openaikey"):
        with open(".openaikey", "r") as file:
            API_KEY = file.read()
    else:
        print("WARN: .openaikey does not exist")

    def __init__(self):
        self.openai_client = None

    def ocr_with_openai(self, image_roi):
        if self.openai_client is None:
            self.openai_client = OpenAI(api_key=CvHelper.API_KEY)

        # Encode ROI as PNG in memory
        _, buffer = cv2.imencode(".png", image_roi)
        img_b64 = base64.b64encode(buffer).decode("utf-8")

        # Send to OpenAI for OCR
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4.1" if available in your account
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Extract ONLY the exact text from this image. Do not add explanations or extra words.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                        },
                    ],
                }
            ],
        )

        if "any text" in response.choices[0].message.content:
            return ""

        if "no text" in response.choices[0].message.content:
            return ""

        if "Does not contain" in response.choices[0].message.content:
            return ""

        if "does not contain" in response.choices[0].message.content:
            return ""

        if "can't extract" in response.choices[0].message.content:
            return ""

        if "contains no" in response.choices[0].message.content:
            return ""

        if "can't read" in response.choices[0].message.content:
            return ""

        if "not clear or" in response.choices[0].message.content:
            return ""

        if "I'm sorry" in response.choices[0].message.content:
            return ""

        if "Sorry, I can't" in response.choices[0].message.content:
            return ""

        if "too dark" in response.choices[0].message.content:
            return ""

        if "visible text" in response.choices[0].message.content:
            return ""

        return response.choices[0].message.content

    @staticmethod
    def rgb_similarity(rgb1, rgb2):
        # Extract individual color components
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        # *** CRITICAL FIX: Convert to a signed integer type (e.g., standard int) ***
        # This prevents numpy's uint8 from underflowing when subtracting a larger value
        r1, g1, b1 = int(r1), int(g1), int(b1)
        r2, g2, b2 = int(r2), int(g2), int(b2)

        # Calculate Euclidean distance
        distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

        # Normalize distance to a scale of 0 to 1
        similarity = 1 - (distance / math.sqrt(3 * (255**2)))

        return similarity

    @staticmethod
    def hex_to_bgr(hex_color: str):
        """Convert hex color string to BGR tuple (OpenCV order)."""
        hex_color = hex_color.lstrip("#")
        r, g, b = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
        return (b, g, r)

    @staticmethod
    def replace_color_with_black(image, hex_color, tolerance=2):
        """
        Replace all pixels similar to the given color with black.

        Args:
            image: OpenCV BGR image (np.ndarray).
            hex_color: str, hex color code (e.g. "#f5e8e9").
            tolerance: int, leeway for color matching.

        Returns:
            New image with matching pixels turned black.
        """
        bgr = np.array(CvHelper.hex_to_bgr(hex_color), dtype=np.uint8)

        # Lower and upper bounds with tolerance
        lower = np.clip(bgr - tolerance, 0, 255)
        upper = np.clip(bgr + tolerance, 0, 255)

        # Create mask where color matches
        mask = cv2.inRange(image, lower, upper)

        # Copy image and apply black where mask is true
        result = image.copy()
        result[mask > 0] = (0, 0, 0)

        return result

    @staticmethod
    def replace_color_with_white(image, hex_color, tolerance=2):
        """
        Replace all pixels similar to the given color with black.

        Args:
            image: OpenCV BGR image (np.ndarray).
            hex_color: str, hex color code (e.g. "#f5e8e9").
            tolerance: int, leeway for color matching.

        Returns:
            New image with matching pixels turned black.
        """
        bgr = np.array(CvHelper.hex_to_bgr(hex_color), dtype=np.uint8)

        # Lower and upper bounds with tolerance
        lower = np.clip(bgr - tolerance, 0, 255)
        upper = np.clip(bgr + tolerance, 0, 255)

        # Create mask where color matches
        mask = cv2.inRange(image, lower, upper)

        # Copy image and apply black where mask is true
        result = image.copy()
        result[mask > 0] = (255, 255, 255)

        return result

    @staticmethod
    def ocr_from_pytesseract(roi, block, chars=None, threshold=5, debug=False):
        # all black to white
        target_bgr = np.array(CvHelper.hex_to_bgr("#000000"))
        diff = cv2.absdiff(roi, target_bgr)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(mask, 15, 255, cv2.THRESH_BINARY_INV)[
            1
        ]  # adjust tolerance
        original = roi
        roi[mask == 255] = (255, 255, 255)

        for color in block["colors"]:
            target_bgr = np.array(CvHelper.hex_to_bgr(color))

            # Create mask for pixels matching the target color
            diff = cv2.absdiff(roi, target_bgr)
            mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            mask = cv2.threshold(mask, threshold, 255, cv2.THRESH_BINARY_INV)[
                1
            ]  # adjust tolerance

            # Convert: matching color -> black, others -> white
            # roi = np.where(mask[..., None] == 255, (0,0,0)).astype(np.uint8)
            roi[mask == 255] = (0, 0, 0)

        target_bgr = np.array(CvHelper.hex_to_bgr("#000000"))
        diff = cv2.absdiff(roi, target_bgr)
        mask = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY_INV)[1]  # adjust tolerance

        # Convert: matching color -> black, others -> white
        roi = np.where(mask[..., None] == 255, (0, 0, 0), (255, 255, 255)).astype(
            np.uint8
        )

        if debug:
            cv2.imshow("original", original)
            cv2.imshow("processed", roi)
            cv2.waitKey()

        # OCR with pytesseract
        result = None
        if chars is not None:
            result = pytesseract.image_to_string(
                roi, config=f"--psm 8 -c tessedit_char_whitelist={chars}"
            )
        else:
            result = pytesseract.image_to_string(roi, config=f"--psm 8")

        # print(f"result = {result} chars {chars}")

        # cv2.imshow(f"roi [{result}]", roi)
        # cv2.waitKey()

        return result.strip()

    def ocr_from_blocks(self, image, ocr_blocks, method="openai"):
        results = {}
        text: str = None

        for block_name, block in ocr_blocks.items():
            results[block_name] = []

            x, y, w, h = block["x"], block["y"], block["w"], block["h"]
            roi = image[y : y + h, x : x + w].copy()
            override_method = method
            if "method" in block:
                override_method = block["method"]

            threshold = 5
            if "threshold" in block:
                threshold = block["threshold"]

            chars = None
            if "chars" in block:
                chars = block["chars"]

            if override_method == "pytesseract":
                text = CvHelper.ocr_from_pytesseract(
                    roi, block, threshold=threshold, chars=chars
                )
            elif override_method == "openai":
                text = self.ocr_with_openai(roi)
            results[block_name] = text

        return results

    @staticmethod
    def ocr_from_block(roi, block, chars, threshold=5):
        text: str = "0"

        text = CvHelper.ocr_from_pytesseract(roi, block, chars, threshold=threshold)

        return text

    @staticmethod
    def count_color_in_roi(roi, hex_color, threshold=0):
        """
        Count how many pixels approximately match a given hex RGB color inside an ROI.

        Args:
            roi: np.ndarray (OpenCV image, BGR order)
            hex_color: str, e.g. "#FF00AA" (RGB)
            threshold: int, allowed +/- tolerance per channel (default=0 = exact match)

        Returns:
            count (int): number of matching pixels
        """
        # Convert hex -> RGB -> BGR (since OpenCV is BGR)
        rgb = tuple(int(hex_color[i : i + 2], 16) for i in (1, 3, 5))
        bgr = (rgb[2], rgb[1], rgb[0])

        # Define lower and upper bounds with threshold
        lower = np.array(
            [
                max(0, bgr[0] - threshold),
                max(0, bgr[1] - threshold),
                max(0, bgr[2] - threshold),
            ],
            dtype=np.uint8,
        )

        upper = np.array(
            [
                min(255, bgr[0] + threshold),
                min(255, bgr[1] + threshold),
                min(255, bgr[2] + threshold),
            ],
            dtype=np.uint8,
        )

        # Mask pixels within the tolerance range
        mask = cv2.inRange(roi, lower, upper)

        # Count non-zero pixels (matching color within tolerance)
        count = cv2.countNonZero(mask)

        return count
