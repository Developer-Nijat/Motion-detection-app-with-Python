import cv2
import datetime
import os
import pygame

# Paths
output_dir = "captured_videos"
alert_sound_path = "assets/sounds/siren-fire-alert.wav"

# Create directories if they don't exist
os.makedirs(output_dir, exist_ok=True)

# Initialize pygame mixer for sound control
pygame.mixer.init()

def play_alert_sound():
    """Play the alert notification sound."""
    try:
        if not pygame.mixer.music.get_busy():  # Check if the sound is already playing
            pygame.mixer.music.load(alert_sound_path)  # Load the sound file
            pygame.mixer.music.play(-1)  # Loop the sound indefinitely
    except Exception as e:
        print(f"[WARNING] Could not play sound: {e}")

def stop_alert_sound():
    """Stop the alert notification sound."""
    try:
        pygame.mixer.music.stop()  # Stop the sound if playing
        print("[INFO] Alert sound stopped.")
    except Exception as e:
        print(f"[WARNING] Could not stop sound: {e}")
        
def start_video_writer(frame, output_dir):
    """Start a video writer."""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(output_dir, f"video_{timestamp}.avi")
    height, width, _ = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_writer = cv2.VideoWriter(file_path, fourcc, 20.0, (width, height))
    print(f"[INFO] Recording started: {file_path}")
    return video_writer, file_path

def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Unable to access the webcam.")
        return

    print("[INFO] Webcam accessed successfully. Press 'q' to quit.")

    # Variables for motion detection
    first_frame = None
    motion_detected = False
    video_writer = None
    recording = False

    # Flag for alert sound control
    alert_sound_playing = False

    # Frame count for stabilization
    frame_counter = 0
    detection_sensitivity = 25  # Adjust for finer or broader motion detection

    while True:
        # Read frame from the webcam
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Unable to read from the webcam.")
            break

        # Convert the frame to grayscale and blur it
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # Skip initial frames to stabilize the feed
        if frame_counter < 30:
            frame_counter += 1
            first_frame = gray  # Update the first frame for stabilization
            continue

        # Compute the absolute difference between the current frame and the first frame
        delta_frame = cv2.absdiff(first_frame, gray)
        thresh_frame = cv2.threshold(delta_frame, detection_sensitivity, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Find contours
        contours, _ = cv2.findContours(thresh_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_detected = False  # Reset motion detected flag

        for contour in contours:
            if cv2.contourArea(contour) < 2000:  # Ignore very small movements
                continue
            motion_detected = True

            # Draw a rectangle around the moving object
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Handle recording logic
        if motion_detected and not recording:
            # Start recording if motion is detected
            video_writer, file_path = start_video_writer(frame, output_dir)
            recording = True
            # Start alert sound if not already playing
            if not alert_sound_playing:
                play_alert_sound()
                alert_sound_playing = True

        if recording:
            # Write frames to the video
            video_writer.write(frame)

        if not motion_detected and recording:
            # Stop recording when motion ends
            print(f"[INFO] Recording stopped: {file_path}")
            video_writer.release()
            recording = False
            # Stop alert sound
            if alert_sound_playing:
                stop_alert_sound()
                alert_sound_playing = False

        # Display the live feed with motion rectangles
        cv2.imshow("Motion Detector", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    if recording:
        video_writer.release()
    cv2.destroyAllWindows()
    print("[INFO] Exiting program.")

if __name__ == "__main__":
    main()
