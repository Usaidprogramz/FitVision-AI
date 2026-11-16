
import numpy as np


def calculate_angle(a, b, c):

    # Convert points into NumPy arrays
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Calculate angle using three body points
    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    # Convert radians into degrees
    angle = np.abs(radians * 180.0 / np.pi)

    # Keep angle between 0 and 180
    if angle > 180:
        angle = 360 - angle

    return angle
