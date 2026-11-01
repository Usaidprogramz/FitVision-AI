# FitVision AI -- Installation and Run Guide

## Purpose

This guide covers setup of the current Python prototype. Commands use
Windows PowerShell.

## Requirements

-   Python compatible with the installed MediaPipe package.
-   Git.
-   Visual Studio Code (recommended).
-   Webcam.
-   Internet access for package installation and model download.

## 1. Clone the Repository

``` powershell
git clone https://github.com/Usaidprogramz/FitVision-AI.git
cd FitVision-AI
```

## 2. Create and Activate a Virtual Environment

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the activation method permitted by
your computer's security settings or select the virtual environment
through VS Code.

## 3. Install Dependencies

If `requirements.txt` is up to date:

``` powershell
pip install -r requirements.txt
```

Main packages used by the current prototype:

``` powershell
pip install mediapipe opencv-python numpy
```

Keep `requirements.txt` updated when dependencies change.

## 4. Check the Pose Model

The current prototype expects:

``` text
models/pose_landmarker_lite.task
```

If missing, download the official Lite model:
https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task

Save it with the exact filename and location above. It is a binary model
file, not readable Python source.

## 5. Run the Current Prototype

From the project root, with the virtual environment activated:

``` powershell
python src/pose_detection.py
```

Allow camera access if prompted. Close other applications that may be
using the webcam.

## 6. CSV Workout Logs

The CSV-enabled prototype saves completed bicep-curl repetition records
in:

``` text
data/workout_logs/
```

Each session creates a separate CSV file containing per-repetition
measurements, score components, total score, and feedback.

## 7. Troubleshooting

### Webcam does not open

-   Close applications using the camera.
-   Check Windows camera permissions.
-   Confirm the correct camera is connected.

### ModuleNotFoundError

Activate the project's virtual environment and install dependencies:

``` powershell
pip install -r requirements.txt
```

### Pose model file error

Confirm `models/pose_landmarker_lite.task` exists and its filename is
correct.

### Changes do not appear on GitHub

Check the current branch and working tree:

``` powershell
git status
```

Then add, commit, and push to the correct branch.

## Important Notes

-   Run commands from the project root (`FitVision-AI`).
-   Do not commit your virtual environment.
-   Do not commit private data or unapproved volunteer videos.
-   This guide covers the current Python prototype. Add separate
    backend, web, and mobile setup instructions when those components
    are implemented.
