import numpy as np


class SquatCalibration:

    def __init__(self):
        self.standing_angles = []
        self.squat_angles = []

        self.standing_average = None
        self.lowest_squat_angle = None

        self.standing_threshold = None
        self.bottom_threshold = None
        self.depth_threshold = None

    def add_standing_angle(self, angle):
        self.standing_angles.append(angle)

    def add_squat_angle(self, angle):
        self.squat_angles.append(angle)

    def calculate_thresholds(self):

        if len(self.standing_angles) < 10:
            raise ValueError("Not enough standing measurements.")

        if len(self.squat_angles) < 10:
            raise ValueError("Not enough squat measurements.")

        self.standing_average = float(
            np.median(self.standing_angles)
        )

        self.lowest_squat_angle = float(
            np.percentile(self.squat_angles, 10)
        )

        # Personalized thresholds
        self.standing_threshold = max(
            150,
            self.standing_average - 15
        )

        self.bottom_threshold = (
            self.lowest_squat_angle + 20
        )

        self.depth_threshold = (
            self.lowest_squat_angle + 10
        )

        # Keep thresholds in a sensible order
        self.bottom_threshold = min(
            self.bottom_threshold,
            self.standing_threshold - 10
        )

        self.depth_threshold = min(
            self.depth_threshold,
            self.bottom_threshold
        )

        return {
            "standing_average": round(self.standing_average, 1),
            "lowest_squat_angle": round(self.lowest_squat_angle, 1),
            "standing_threshold": round(self.standing_threshold, 1),
            "bottom_threshold": round(self.bottom_threshold, 1),
            "depth_threshold": round(self.depth_threshold, 1)
        }