import sys

import cv2

print("Starting FitVision AI webcam...")

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Camera not found!")
    sys.exit()

print("Camera started successfully!")

while True:
    success, frame = camera.read()

    if not success:
        print("Unable to read camera frame!")
        break

    cv2.imshow("FitVision AI - Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()

print("Camera closed successfully!")
