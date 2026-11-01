# FitVision AI -- System Architecture

## Purpose

This document describes the planned high-level architecture. Components
still under development are identified as planned.

## High-Level Processing Flow

1.  User selects an exercise and starts a workout.
2.  Camera captures video frames.
3.  OpenCV reads and prepares frames.
4.  A pose-estimation model detects body landmarks.
5.  Exercise-specific logic analyzes required landmarks and joint
    angles.
6.  A repetition counter tracks movement stages.
7.  Feedback logic evaluates selected visible movement cues.
8.  The interface displays landmarks, repetitions, feedback, and score.
9.  Workout summaries can be saved.

## Architecture Diagram

``` text
              User
               |
       Web / Mobile Interface
               |
        Camera / Video Input
               |
          OpenCV Processing
               |
          Pose Estimation
       (MediaPipe / MoveNet)
               |
        Body Landmark Data
               |
       Exercise Logic Modules
   (Bicep Curl / Squat / Push-up / Lunge)
               |
       Rep Counter and Feedback
               |
       Live Results and Score
               |
       Workout Summary Storage
        (CSV initially; database
          planned for the app)
```

## Main Components

### Camera and Video Input

Captures frames from a webcam or supported camera source. Camera
placement and visibility matter for reliable landmark detection.

### Pose Estimation

Detects body landmarks. The project plans to evaluate MediaPipe Pose and
MoveNet Lightning. Their landmark sets differ, so a common internal
representation may be useful.

### Exercise Logic

Each exercise has separate movement-analysis rules. The current
bicep-curl prototype uses elbow angles and movement states to identify a
curl cycle.

### Repetition Counter

Tracks transitions between movement stages and increments the count when
a complete cycle is detected.

### Posture Feedback and Form Score

Evaluates selected visible cues. Scores are heuristic indicators and
require testing; they are not clinically validated measurements.

### User Interfaces

The planned web and mobile interfaces will support exercise selection,
live workout information, and workout summaries.

### Backend and Storage

A FastAPI backend and database are planned. The current prototype can
save completed repetition details to CSV.

## Pose Model Comparison

MediaPipe Pose and MoveNet Lightning will be evaluated separately using
the same recorded test videos and comparable conditions. The comparison
may include landmark visibility, processing speed, and suitability for
the selected exercises. Both models do not need to run simultaneously
during a normal workout.

## Design Considerations

-   Prefer lightweight inference suitable for modest hardware.
-   Use the same test recordings when comparing models.
-   Keep exercise-specific rules separate from pose detection where
    practical.
-   Avoid confident form assessments when landmarks are unreliable.
-   Store workout summaries rather than continuous video by default.
-   Collect volunteer recordings only with appropriate consent.

## Current Status

The current prototype uses MediaPipe Pose Landmarker, OpenCV, and Python
for webcam-based pose visualization and bicep-curl analysis. CSV logging
is available. Backend, database, web, mobile, and additional exercise
modules remain planned or in development.
