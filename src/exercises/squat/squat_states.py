def detect_squat_state(knee_angle, standing_threshold=160, bottom_threshold=100):
    if knee_angle >= standing_threshold:
        return "STANDING"
    elif knee_angle <= bottom_threshold:
        return "BOTTOM"
    else:
        return "MOVING"