# FitVision AI -- Project Overview

## Introduction

FitVision AI is a lightweight computer vision-based fitness system
designed to analyze selected exercise movements using a camera and pose
estimation. It aims to count repetitions and provide basic visual
feedback about exercise form.

## Problem Statement

People may exercise without a convenient way to monitor repetitions or
receive simple feedback about visible movement patterns. FitVision AI
aims to provide an accessible computer vision-based monitoring system
for selected exercises.

## Objectives

-   Detect human body landmarks from camera input.
-   Recognize selected exercises.
-   Count repetitions automatically.
-   Provide basic real-time visual posture feedback.
-   Calculate an indicative exercise form score.
-   Save workout summaries and history.
-   Develop web and mobile interfaces.
-   Compare MediaPipe Pose and MoveNet Lightning.

## Initial Exercises

1.  Bicep curls
2.  Squats
3.  Push-ups
4.  Lunges

The current working prototype focuses on bicep curls. The other
exercises are planned for implementation.

## Planned Technology Stack

  Area                      Technology
  ------------------------- -----------------------------------
  Programming               Python
  Image processing          OpenCV
  Pose estimation           MediaPipe Pose, MoveNet Lightning
  Numerical operations      NumPy
  Backend                   FastAPI
  Initial database          SQLite
  Possible later database   PostgreSQL
  Web interface             HTML, CSS, JavaScript
  Mobile interface          Flutter
  Version control           Git and GitHub

## Current Prototype Features

-   Webcam pose detection using MediaPipe Pose Landmarker.
-   Body landmark and skeleton visualization.
-   Bicep-curl elbow-angle calculation.
-   Bicep-curl repetition counting using movement thresholds.
-   Basic form feedback and a heuristic score.
-   CSV logging of completed bicep-curl repetitions.

## Planned Features

-   Squat, push-up, and lunge analysis.
-   Exercise selection and recognition workflow.
-   MediaPipe and MoveNet comparison experiments.
-   FastAPI backend and workout history.
-   Web and Flutter mobile interfaces.
-   Workout summaries and progress reports.

## Scope and Limitations

The system focuses on selected exercises and visible movement cues.
Feedback and scores are for general fitness monitoring only; they are
not medical advice, physiotherapy guidance, or professional assessment.
Camera angle, lighting, occlusion, and landmark quality may affect
results. The application should avoid confident assessments when
required landmarks are unreliable.

## Expected Outcome

A lightweight fitness monitoring application that analyzes selected
exercises, counts repetitions, provides basic visual feedback, and
records workout summaries.
