def check_squat_depth(
    knee_angle,
    standing_threshold=160,
    depth_threshold=90,
    deep_threshold=70
):

    if knee_angle >= standing_threshold:
        return "STANDING"

    elif knee_angle > depth_threshold:
        return "SHALLOW SQUAT"

    elif knee_angle > deep_threshold:
        return "TARGET DEPTH REACHED"

    else:
        return "BELOW TARGET RANGE"