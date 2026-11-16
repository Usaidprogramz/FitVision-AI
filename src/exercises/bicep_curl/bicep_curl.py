# Main bicep curl logic

from rep_counter import BicepCurlRepCounter
from posture_feedback import (
    get_posture_feedback,
    calculate_form_score
)


class BicepCurlSession:
    """Manages the basic bicep curl exercise session."""

    def __init__(self):
        self.rep_counter = BicepCurlRepCounter()

    def process_elbow_angle(self, elbow_angle):
        reps = self.rep_counter.update(elbow_angle)
        feedback = get_posture_feedback(elbow_angle)
        score = calculate_form_score(elbow_angle)

        return {
            "repetitions": reps,
            "elbow_angle": elbow_angle,
            "feedback": feedback,
            "form_score": score
        }


def main():
    session = BicepCurlSession()

    # Temporary sample angles for testing.
    sample_angles = [170, 140, 100, 60, 90, 130, 160]

    for angle in sample_angles:
        result = session.process_elbow_angle(angle)

        print(
            f"Angle: {result['elbow_angle']} | "
            f"Reps: {result['repetitions']} | "
            f"Score: {result['form_score']} | "
            f"Feedback: {result['feedback']}"
        )


if __name__ == "__main__":
    main()
