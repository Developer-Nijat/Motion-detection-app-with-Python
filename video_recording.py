import cv2
import datetime
import os

# Create a directory to store captured videos
output_dir = "captured_videos"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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

        if recording:
            # Write frames to the video
            video_writer.write(frame)

        if not motion_detected and recording:
            # Stop recording when motion ends
            print(f"[INFO] Recording stopped: {file_path}")
            video_writer.release()
            recording = False

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
