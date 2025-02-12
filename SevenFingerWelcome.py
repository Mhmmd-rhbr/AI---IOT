import cv2
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.HandTrackingModule import HandDetector
import numpy as np

def main():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # Set frame width
    cap.set(4, 720)   # Set frame height

    # Initialize detectors with proper parameters
    face_detector = FaceMeshDetector(maxFaces=2, minDetectionCon=0.7, minTrackCon=0.7)
    hand_detector = HandDetector(maxHands=2, detectionCon=0.5, minTrackCon=0.5)

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image from camera.")
            break

        # Display welcome text at the top center
        cv2.putText(img, "Welcome", (img.shape[1] // 2 - 100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)

        # --- Face Mesh and Emotion Detection ---
        img, faces = face_detector.findFaceMesh(img, draw=True)
        emotion = "Unknown"
        face_crop = None  # To hold the cropped face image if needed

        if faces:
            for face in faces:
                # Extract key landmarks for emotion detection
                left_eye = face[145]    # Inner corner of left eye
                right_eye = face[374]   # Inner corner of right eye
                left_lip = face[61]     # Upper left lip
                right_lip = face[291]   # Upper right lip
                upper_lip = face[13]    # Upper middle lip
                lower_lip = face[14]    # Lower middle lip

                # Calculate distances between landmarks
                horizontal_lip_distance = np.linalg.norm(np.array(left_lip) - np.array(right_lip))
                vertical_lip_distance = np.linalg.norm(np.array(upper_lip) - np.array(lower_lip))
                eye_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))

                # Check if mouth is open (ratio > 0.3)
                mouth_open = vertical_lip_distance / horizontal_lip_distance > 0.3

                # Emotion classification based on facial measurements
                if mouth_open and vertical_lip_distance > 0.1 * eye_distance:
                    emotion = "Surprised"
                elif vertical_lip_distance / horizontal_lip_distance > 0.18:
                    emotion = "Smiling"  # Happy
                elif 0.03 < vertical_lip_distance / horizontal_lip_distance < 0.06:
                    emotion = "Sad"
                elif eye_distance / horizontal_lip_distance > 1.6:
                    emotion = "Angry"
                else:
                    emotion = "Neutral"

                # Display emotion text above face
                top_point = min(face, key=lambda point: point[1])
                cv2.putText(img, f"Emotion: {emotion}", (top_point[0] - 50, top_point[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # If the face is surprised, display the cropped face in a separate window
                if emotion == "Surprised":
                    x_values = [pt[0] for pt in face]
                    y_values = [pt[1] for pt in face]
                    x_min, x_max = min(x_values), max(x_values)
                    y_min, y_max = min(y_values), max(y_values)
                    
                    # Add padding to the crop region
                    padding = 20
                    x_min = max(0, x_min - padding)
                    y_min = max(0, y_min - padding)
                    x_max = min(img.shape[1], x_max + padding)
                    y_max = min(img.shape[0], y_max + padding)
                    
                    face_crop = img[y_min:y_max, x_min:x_max]
                    if face_crop.size > 0:  # Check if crop is valid
                        cv2.imshow("Surprised Face", face_crop)
                else:
                    # Close "Surprised Face" window if it exists
                    try:
                        cv2.destroyWindow("Surprised Face")
                    except:
                        pass

        # --- Hand Tracking and Finger Counting ---
        hands, img = hand_detector.findHands(img, draw=True, flipType=True)
        totalFingers = 0

        if hands:
            for hand in hands:
                # Count raised fingers
                fingers = hand_detector.fingersUp(hand)
                fingerCount = sum(fingers)
                totalFingers += fingerCount
                
                # Determine hand orientation
                bbox = hand['bbox']
                hand_type = "Palm" if bbox[2] < bbox[3] else "Back of Hand"
                
                # Display hand information
                hand_position = hand['center']
                cv2.putText(img, f"{hand_type}", (hand_position[0] - 50, hand_position[1] - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(img, f"Fingers: {fingerCount}", (hand_position[0] - 50, hand_position[1] - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display total finger count
        cv2.putText(img, f"Total Fingers: {totalFingers}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    
        # If hand gesture shows 7 fingers, display welcome message at the center
        if totalFingers == 7:
            cv2.putText(img, "Welcome!", (img.shape[1] // 2 - 100, img.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)

        # Show the main window
        cv2.imshow("Hand and Face Mesh", img)

        # Exit on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Cleanup resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()