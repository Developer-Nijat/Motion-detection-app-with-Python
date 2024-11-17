# Motion Detection with Alert Sound

A Python-based motion detection application that records video and plays an alert sound when motion is detected. It utilizes OpenCV for motion detection and Pygame for sound playback. The application can detect motion and record videos while running in the background, even when your screen is locked.

## Features

- **Motion Detection**: Detects motion using OpenCV and triggers an alert sound.
- **Video Recording**: Records video when motion is detected and saves it to disk.
- **Photo Capture**: Takes snapshots of the scene when motion is detected.
- **Background Operation**: The application continues to detect motion and function properly, even when the screen is locked.

## Table of Contents
1. [Dependencies](#dependencies)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Code Structure](#code-structure)
5. [Background Operation](#background-operation)

## Dependencies

Before running the application, install the necessary dependencies. You can use `pip` to install them.

```bash
pip install opencv-python numpy pygame
```

### Required Python Version

- Python version: `3.12` (Installed from Microsoft Store)
- Platform: Windows 11

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/your-username/motion-detection-alert.git
cd motion-detection-alert
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. **Run the Motion Detection Application**:
   - You can start the motion detection program by running the following:

```bash
python video_recording_with_alert.py
```

2. **Stop the Application**:
   - To stop the application, press `q` on the video window, or simply close the terminal.

3. **Files Captured**:
   - **Photos**: When motion is detected, a snapshot is saved in the `captured_photos/` folder.
   - **Videos**: The recorded video files are saved in the `captured_videos/` folder.
   - **Alert Sound**: The alert sound is played from `assets/sounds/siren-fire-alert.wav`.

### Configuration

The application can be configured by adjusting the following variables in the code:
- **motion sensitivity**: Adjust how sensitive the motion detection is (e.g., `detection_sensitivity = 25`).
- **sound file path**: Specify the path to the alert sound file (`alert_sound_path = "assets/sounds/siren-fire-alert.wav"`).

### Background Operation

The app functions properly even when your screen is locked. When motion is detected, the app will continue to perform its tasks (i.e., recording videos and playing the alert sound) even if the screen is locked or if the laptop is in sleep mode.

**Note**: No specific background operation implementation was required for this functionality, as the app behaves as expected under these conditions without needing additional configuration or services.

## Code Structure

Here's a breakdown of the project structure:

```
motion-detection-alert/
│
├── assets/
│   └── sounds/
│       └── siren-fire-alert.wav      # Alert sound file
│
├── captured_photos/                  # Folder where captured photos will be stored
├── captured_videos/                  # Folder where recorded videos will be saved
├── capture_photo.py                  # Script for capturing photos on motion detection
├── video_recording.py                # Basic video recording script (without alert)
├── video_recording_with_alert.py     # Full version of the script with motion detection and alert sound
└── requirements.txt                  # List of project dependencies
```

### **Scripts**

- **capture_photo.py**: Captures and saves photos when motion is detected.
- **video_recording.py**: Records video when motion is detected, without sound alert.
- **video_recording_with_alert.py**: Main script with motion detection and alert sound.


## Acknowledgements

- [OpenCV](https://opencv.org/) for the powerful computer vision library.
- [Pygame](https://www.pygame.org/) for handling sound playback.

---

If you have any issues or need assistance, feel free to create an issue or contact the repository owner.
```