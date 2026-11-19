def get_squat_feedback(depth_status):

    feedback_messages = {
        "STANDING": "Stand Straight",
        "SHALLOW SQUAT": "Try Going a Little Lower",
        "TARGET DEPTH REACHED": "Good Depth!",
        "BELOW TARGET RANGE": "You Are Below Your Target Range"
    }

    return feedback_messages.get(
        depth_status,
        "Position Not Detected"
    )