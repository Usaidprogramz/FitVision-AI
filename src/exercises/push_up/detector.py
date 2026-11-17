
import cv2
import mediapipe as mp


class PushUpPoseDetector:

    def __init__(self):

        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def detect_pose(self, frame):

        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # Detect body landmarks
        results = self.pose.process(rgb_frame)

        # Draw skeleton if person is detected
        if results.pose_landmarks:

            self.mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS
            )

        return frame, results

    def close(self):
        self.pose.close()


def main():

    detector = PushUpPoseDetector()

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        detector.close()
        return

    print("Push-up Pose Detection Started")
    print("Press Q to exit.")

    try:

        while True:

            success, frame = cap.read()

            if not success:
                print("Could not read webcam frame.")
                break

            frame, results = detector.detect_pose(frame)

            if results.pose_landmarks:

                cv2.putText(
                    frame,
                    "Person Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            else:

                cv2.putText(
                    frame,
                    "No Person Detected",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            cv2.imshow(
                "FitVision AI - Push Up Detection",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        cap.release()
        detector.close()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
