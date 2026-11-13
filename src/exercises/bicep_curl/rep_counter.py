# Repetition counting

import math


def calculate_angle(a, b, c):
    """
    Calculate the angle ABC using three 2D or 3D points.
    B is the joint whose angle is measured.
    """
    ba = [a[i] - b[i] for i in range(len(a))]
    bc = [c[i] - b[i] for i in range(len(c))]

    dot_product = sum(x * y for x, y in zip(ba, bc))
    magnitude_ba = math.sqrt(sum(x * x for x in ba))
    magnitude_bc = math.sqrt(sum(x * x for x in bc))

    if magnitude_ba == 0 or magnitude_bc == 0:
        return None

    cosine = dot_product / (magnitude_ba * magnitude_bc)
    cosine = max(-1.0, min(1.0, cosine))

    return math.degrees(math.acos(cosine))


class BicepCurlRepCounter:
    """Counts complete bicep curl repetitions using elbow angles."""

    def __init__(self, extended_angle=150, curled_angle=65):
        self.extended_angle = extended_angle
        self.curled_angle = curled_angle
        self.reps = 0
        self.state = "WAITING"

    def update(self, elbow_angle):
        """
        Update the counter with the latest elbow angle.
        Returns the current repetition count.
        """
        if elbow_angle is None:
            return self.reps

        if self.state == "WAITING":
            if elbow_angle >= self.extended_angle:
                self.state = "READY"

        elif self.state == "READY":
            if elbow_angle <= self.curled_angle:
                self.state = "CURLING"

        elif self.state == "CURLING":
            if elbow_angle >= self.extended_angle:
                self.reps += 1
                self.state = "READY"

        return self.reps

    def reset(self):
        """Reset the repetition counter."""
        self.reps = 0
        self.state = "WAITING"
