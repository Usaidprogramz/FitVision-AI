
import math
from collections import deque


class AngleSmoother:

    def __init__(self, window_size=5):
        self.window_size = window_size
        self.angles = deque(maxlen=window_size)

    def update(self, new_angle):

        if new_angle is None:
            return None

        if not math.isfinite(new_angle):
            return None

        self.angles.append(new_angle)

        smoothed_angle = sum(self.angles) / len(self.angles)

        return smoothed_angle

    def reset(self):
        self.angles.clear()
