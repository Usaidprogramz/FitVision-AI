
import os
import time

import cv2
import mediapipe as mp

from src.exercises.squat.angle_calculation import calculate_angle
from src.exercises.squat.angle_smoothing import AngleSmoother
from src.exercises.squat.calibration import SquatCalibration
from src.exercises.squat.landmarks import get_squat_landmarks
from src.exercises.squat.rep_counter import SquatCounter
from src.exercises.squat.squat_depth import check_squat_depth
from src.exercises.squat.squat_feedback import get_squat_feedback
from src.exercises.squat.squat_states import detect_squat_state

# ==========================================
# 1. MEDIAPIPE COMPONENTS
# ==========================================

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode


# ==========================================
# 2. CONFIGURE POSE DETECTOR
# ==========================================

options = PoseLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/pose_landmarker_lite.task"
    ),
    running_mode=RunningMode.VIDEO,
    num_poses=1,
    min_pose_detection_confidence=0.5,
    min_pose_presence_confidence=0.5,
    min_tracking_confidence=0.5
)


# ==========================================
# 3. INITIALIZE VARIABLES
# ==========================================

camera = None
video_writer = None

counter = SquatCounter()
angle_smoother = AngleSmoother(window_size=5)

calibration = SquatCalibration()

calibration_phase = "STANDING"
calibration_phase_start = None

standing_duration = 3
squat_duration = 8

calibrated = False
calibration_error = ""

standing_threshold = 160
bottom_threshold = 100
depth_threshold = 90
deep_threshold = 70

start_time = time.monotonic()
frame_timestamp = 0


# ==========================================
# 4. VIDEO RECORDING VARIABLES
# ==========================================

os.makedirs("recordings", exist_ok=True)

recording_started = False

video_filename = time.strftime(
    "squat_session_%Y%m%d_%H%M%S.mp4"
)


# ==========================================
# 5. START POSE DETECTION
# ==========================================

try:

    with PoseLandmarker.create_from_options(options) as landmarker:

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():
            raise RuntimeError("Camera not found!")

        calibration_phase_start = time.monotonic()

        print("FitVision AI - Squat Detection Started!")
        print("Calibration started.")
        print("First: Stand straight for 3 seconds.")
        print("Then: Perform slow squats for 8 seconds.")

        while True:

            # ==================================
            # CAPTURE WEBCAM FRAME
            # ==================================

            success, frame = camera.read()

            if not success:
                print("Cannot read camera frame!")
                break

            rgb_frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            elapsed_time = int(
                (time.monotonic() - start_time) * 1000
            )

            frame_timestamp = max(
                frame_timestamp + 1,
                elapsed_time
            )

            results = landmarker.detect_for_video(
                mp_image,
                frame_timestamp
            )

            height, width, _ = frame.shape

            # ==================================
            # 6. INITIALIZE VIDEO RECORDING ONCE
            # ==================================

            if not recording_started:

                fourcc = cv2.VideoWriter_fourcc(*"mp4v")

                video_writer = cv2.VideoWriter(
                    os.path.join("recordings", video_filename),
                    fourcc,
                    20.0,
                    (width, height)
                )

                if not video_writer.isOpened():
                    raise RuntimeError(
                        "Could not start video recording!"
                    )

                recording_started = True

                print("Video recording started!")

            # ==================================
            # 7. CHECK BODY DETECTION
            # ==================================

            if results.pose_landmarks:

                pose_landmarks = results.pose_landmarks[0]

                # Draw body landmarks
                for landmark in pose_landmarks:

                    x = int(landmark.x * width)
                    y = int(landmark.y * height)

                    if 0 <= x < width and 0 <= y < height:

                        cv2.circle(
                            frame,
                            (x, y),
                            5,
                            (0, 255, 0),
                            -1
                        )

                # ==================================
                # 8. EXTRACT SQUAT LANDMARKS
                # ==================================

                points = get_squat_landmarks(
                    pose_landmarks
                )

                left_points = [
                    points["left_hip"],
                    points["left_knee"],
                    points["left_ankle"]
                ]

                right_points = [
                    points["right_hip"],
                    points["right_knee"],
                    points["right_ankle"]
                ]

                left_visibility = min(
                    point.visibility for point in left_points
                )

                right_visibility = min(
                    point.visibility for point in right_points
                )

                # Select side with better visibility
                if left_visibility >= right_visibility:

                    selected_points = left_points
                    selected_side = "LEFT"
                    visibility = left_visibility

                else:

                    selected_points = right_points
                    selected_side = "RIGHT"
                    visibility = right_visibility

                # ==================================
                # 9. CHECK LANDMARK RELIABILITY
                # ==================================

                if visibility >= 0.5:

                    hip, knee, ankle = selected_points

                    raw_angle = calculate_angle(
                        [hip.x, hip.y],
                        [knee.x, knee.y],
                        [ankle.x, ankle.y]
                    )

                    angle = angle_smoother.update(raw_angle)

                    # ==================================
                    # 10. PERSONAL CALIBRATION
                    # ==================================

                    if not calibrated and calibration_phase != "FAILED":

                        phase_elapsed = (
                            time.monotonic() - calibration_phase_start
                        )

                        if calibration_phase == "STANDING":

                            if phase_elapsed < standing_duration:

                                calibration.add_standing_angle(angle)

                                message = "Calibration: Stand straight"

                            else:

                                calibration_phase = "SQUAT"
                                calibration_phase_start = time.monotonic()

                                message = "Now perform slow squats"

                        elif calibration_phase == "SQUAT":

                            if phase_elapsed < squat_duration:

                                calibration.add_squat_angle(angle)

                                message = "Calibration: Perform slow squats"

                            else:

                                try:

                                    values = calibration.calculate_thresholds()

                                    movement_range = (
                                        values["standing_average"]
                                        - values["lowest_squat_angle"]
                                    )

                                    if movement_range < 25:
                                        raise ValueError(
                                            "Not enough difference between standing and squat angles."
                                        )

                                    standing_threshold = values[
                                        "standing_threshold"
                                    ]

                                    bottom_threshold = values[
                                        "bottom_threshold"
                                    ]

                                    depth_threshold = values[
                                        "depth_threshold"
                                    ]

                                    calibrated = True

                                    counter = SquatCounter()

                                    angle_smoother.reset()

                                    print("\nCalibration successful!")
                                    print(values)

                                    message = "Calibration complete!"

                                except ValueError as error:

                                    calibration_phase = "FAILED"
                                    calibration_error = str(error)

                                    message = "Calibration failed!"

                                    print("Calibration failed:", error)

                    # ==================================
                    # 11. NORMAL SQUAT DETECTION
                    # ==================================

                    if calibrated:

                        squat_state = detect_squat_state(
                            angle,
                            standing_threshold=standing_threshold,
                            bottom_threshold=bottom_threshold
                        )

                        depth_status = check_squat_depth(
                            angle,
                            standing_threshold=standing_threshold,
                            depth_threshold=depth_threshold,
                            deep_threshold=deep_threshold
                        )

                        feedback = get_squat_feedback(
                            depth_status
                        )

                        # Update repetition counter
                        rep_count = counter.update(
                            squat_state,
                            depth_status == "TARGET DEPTH REACHED"
                        )

                        # Display knee angle
                        cv2.putText(
                            frame,
                            f"Knee Angle: {int(angle)}",
                            (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 0),
                            2
                        )

                        # Display squat state
                        cv2.putText(
                            frame,
                            f"Squat State: {squat_state}",
                            (30, 90),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2
                        )

                        # Display selected side
                        cv2.putText(
                            frame,
                            f"Side: {selected_side}",
                            (30, 130),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 255),
                            2
                        )

                        # Display feedback
                        cv2.putText(
                            frame,
                            f"Feedback: {feedback}",
                            (30, 170),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 255),
                            2
                        )

                        # Display squat depth
                        cv2.putText(
                            frame,
                            f"Squat Depth: {depth_status}",
                            (30, 210),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255, 255, 0),
                            2
                        )

                        # Display repetition count
                        cv2.putText(
                            frame,
                            f"Reps: {counter.rep_count}",
                            (30, 260),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (0, 255, 255),
                            2
                        )

                        # Display personalized thresholds
                        cv2.putText(
                            frame,
                            f"Standing: {standing_threshold:.0f} "
                            f"Bottom: {bottom_threshold:.0f} "
                            f"Depth: {depth_threshold:.0f} "
                            f"Deep: {deep_threshold:.0f}",
                            (30, 300),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 255),
                            2
                        )

                    else:

                        # Display calibration progress
                        cv2.putText(
                            frame,
                            f"Angle: {int(angle)}",
                            (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (0, 255, 0),
                            2
                        )

                        if calibration_phase == "STANDING":

                            remaining = max(
                                0,
                                standing_duration - int(
                                    time.monotonic() - calibration_phase_start
                                )
                            )

                            message = f"Stand straight: {remaining}s"

                        elif calibration_phase == "SQUAT":

                            remaining = max(
                                0,
                                squat_duration - int(
                                    time.monotonic() - calibration_phase_start
                                )
                            )

                            message = f"Perform slow squats: {remaining}s"

                        elif calibration_phase == "FAILED":

                            message = "Calibration failed - press Q"

                        cv2.putText(
                            frame,
                            message,
                            (30, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (0, 255, 255),
                            2
                        )

                        if calibration_phase == "FAILED":

                            cv2.putText(
                                frame,
                                calibration_error[:65],
                                (30, 140),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,
                                (0, 0, 255),
                                2
                            )

                else:

                    # Reset unreliable angle measurements
                    angle_smoother.reset()

                    # Cancel incomplete repetition
                    counter.reset_pending_rep()

                    cv2.putText(
                        frame,
                        "Move into camera view!",
                        (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 0, 255),
                        2
                    )

            else:

                # Reset when no body is detected
                angle_smoother.reset()

                # Cancel incomplete repetition
                counter.reset_pending_rep()

                cv2.putText(
                    frame,
                    "No body detected!",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 0, 255),
                    2
                )

            # ==========================================
            # 12. SAVE AND DISPLAY VIDEO
            # ==========================================

            if video_writer is not None:
                video_writer.write(frame)

            cv2.imshow(
                "FitVision AI - Squat Detection",
                frame
            )

            # Press Q to quit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


finally:

    if camera is not None:
        camera.release()

    if video_writer is not None:
        video_writer.release()

    cv2.destroyAllWindows()

    print("Squat detection stopped!")

    if recording_started:
        print(
            "Video saved:",
            os.path.join("recordings", video_filename)
        )
