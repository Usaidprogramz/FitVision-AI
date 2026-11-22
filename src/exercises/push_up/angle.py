
import math
import mediapipe as mp


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle between three points.
    The angle is measured at point_b.
    """

    vector_1 = (
        point_a[0] - point_b[0],
        point_a[1] - point_b[1]
    )

    vector_2 = (
        point_c[0] - point_b[0],
        point_c[1] - point_b[1]
    )

    magnitude_1 = math.hypot(*vector_1)
    magnitude_2 = math.hypot(*vector_2)

    if magnitude_1 == 0 or magnitude_2 == 0:
        return None

    dot_product = (
        vector_1[0] * vector_2[0]
        + vector_1[1] * vector_2[1]
    )

    cosine_angle = dot_product / (
        magnitude_1 * magnitude_2
    )

    # Prevent floating-point errors
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    angle = math.degrees(math.acos(cosine_angle))

    return round(angle, 2)


def calculate_body_angles(results, frame_shape):
    """
    Calculate left/right elbow and hip angles
    using MediaPipe pose landmarks.
    """

    if not results.pose_landmarks:
        return None

    landmarks = results.pose_landmarks.landmark

    height, width = frame_shape[:2]

    mp_pose = mp.solutions.pose.PoseLandmark

    def get_point(landmark_id):

        landmark = landmarks[landmark_id]

        if landmark.visibility < 0.5:
            return None

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        return (x, y)

    def get_angle(first, middle, last):

        point_a = get_point(first)
        point_b = get_point(middle)
        point_c = get_point(last)

        if point_a is None or point_b is None or point_c is None:
            return None

        return calculate_angle(
            point_a,
            point_b,
            point_c
        )

    # Left elbow angle
    left_elbow = get_angle(
        mp_pose.LEFT_SHOULDER.value,
        mp_pose.LEFT_ELBOW.value,
        mp_pose.LEFT_WRIST.value
    )

    # Right elbow angle
    right_elbow = get_angle(
        mp_pose.RIGHT_SHOULDER.value,
        mp_pose.RIGHT_ELBOW.value,
        mp_pose.RIGHT_WRIST.value
    )

    # Left hip angle
    left_hip = get_angle(
        mp_pose.LEFT_SHOULDER.value,
        mp_pose.LEFT_HIP.value,
        mp_pose.LEFT_KNEE.value
    )

    # Right hip angle
    right_hip = get_angle(
        mp_pose.RIGHT_SHOULDER.value,
        mp_pose.RIGHT_HIP.value,
        mp_pose.RIGHT_KNEE.value
    )

    return {
        "left_elbow": left_elbow,
        "right_elbow": right_elbow,
        "left_hip": left_hip,
        "right_hip": right_hip
    }


# Independent mathematical test
if __name__ == "__main__":

    point_a = (0, 0)
    point_b = (0, 10)
    point_c = (10, 10)

    angle = calculate_angle(
        point_a,
        point_b,
        point_c
    )

    print("Angle Calculation Test")
    print("----------------------")
    print(f"Calculated angle: {angle} degrees")
    print("Expected angle: 90 degrees")
