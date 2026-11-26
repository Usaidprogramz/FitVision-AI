
import cv2
import mediapipe as mp

from angle import calculate_body_angles


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Open laptop camera
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, frame = cap.read()

    if not success:
        print("Unable to access camera")
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Detect body landmarks
    results = pose.process(rgb_frame)

    # Draw landmarks
    if results.pose_landmarks:

        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

        # Calculate body angles
        angles = calculate_body_angles(
            results,
            frame.shape
        )

        if angles:

            y_position = 30

            for name, angle in angles.items():

                if angle is not None:
                    text = f"{name}: {angle} degrees"
                else:
                    text = f"{name}: Not visible"

                cv2.putText(
                    frame,
                    text,
                    (10, y_position),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                y_position += 30

    # Display camera
    cv2.imshow(
        "FitVision AI - Angle Testing",
        frame
    )

    # Press Q to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
pose.close()
cv2.destroyAllWindows()
