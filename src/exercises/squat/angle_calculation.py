import numpy as np


def calculate_angle(a, b, c):
    """
    Calculate the angle between three body points.

    Args:
        a: Coordinates of the first point.
        b: Coordinates of the middle point (joint).
        c: Coordinates of the third point.

    Returns:
        The angle in degrees, between 0 and 180.
    """

    # Convert the input coordinates into NumPy arrays
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    # Calculate the angle between the two lines using arctan2
    radians = np.arctan2(
        c[1] - b[1],
        c[0] - b[0]
    ) - np.arctan2(
        a[1] - b[1],
        a[0] - b[0]
    )

    # Convert the calculated angle from radians to degrees
    angle = np.abs(radians * 180.0 / np.pi)

    # Normalize the angle so that it stays within 0 to 180 degrees
    if angle > 180:
        angle = 360 - angle

    # Return the final joint angle
    return angle