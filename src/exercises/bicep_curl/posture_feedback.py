# Form checking and scoring

def get_posture_feedback(elbow_angle):
    """
    Give basic bicep curl feedback based on elbow angle.

    This is an initial visual rule, not a medical assessment.
    """
    if elbow_angle is None:
        return "Cannot detect elbow. Adjust your camera position."

    if elbow_angle > 170:
        return "Start your curl movement."

    if elbow_angle > 150:
        return "Arm is almost fully extended."

    if elbow_angle > 65:
        return "Keep curling."

    return "Good curl position."


def calculate_form_score(elbow_angle):
    """
    Initial range-of-motion score.
    This is a simple prototype score, not a validated form score.
    """
    if elbow_angle is None:
        return 0

    if elbow_angle <= 65:
        return 100

    if elbow_angle >= 150:
        return 0

    score = (150 - elbow_angle) / (150 - 65) * 100
    return round(max(0, min(100, score)), 1)
