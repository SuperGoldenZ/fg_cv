import math


class CvHelper:
    @staticmethod
    def hex_to_bgr(hex_color):
        hex_color = hex_color.lstrip("#")
        # Convert hex to RGB, then reverse to BGR
        return tuple(int(hex_color[i : i + 2], 16) for i in (4, 2, 0))

    @staticmethod
    def rgb_similarity(rgb1, rgb2):
        # Extract individual color components
        r1, g1, b1 = rgb1
        r2, g2, b2 = rgb2

        # Calculate Euclidean distance
        distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

        # Normalize distance to a scale of 0 to 1
        similarity = 1 - (distance / math.sqrt(3 * (255**2)))

        return similarity
