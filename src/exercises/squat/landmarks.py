
def get_squat_landmarks(pose_landmarks):

    # Get left-side landmarks
    left_hip = pose_landmarks[23]
    left_knee = pose_landmarks[25]
    left_ankle = pose_landmarks[27]

    # Get right-side landmarks
    right_hip = pose_landmarks[24]
    right_knee = pose_landmarks[26]
    right_ankle = pose_landmarks[28]

    return {
        "left_hip": left_hip,
        "left_knee": left_knee,
        "left_ankle": left_ankle,

        "right_hip": right_hip,
        "right_knee": right_knee,
        "right_ankle": right_ankle
    }
