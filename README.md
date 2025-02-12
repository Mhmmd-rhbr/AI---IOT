### **README for SevenFingerWelcome.py**

# **SevenFingerWelcome**
A real-time computer vision project using OpenCV and cvzone to detect faces, track emotions, and recognize hand gestures. The program displays a **"Welcome!"** message when exactly **seven fingers** are detected.

---

## **Features**
✅ **Face Mesh Detection:** Detects facial landmarks and determines emotions such as **Surprised, Smiling, Sad, Angry,** and **Neutral**.  
✅ **Hand Tracking & Finger Counting:** Tracks up to two hands and counts the number of raised fingers.  
✅ **Seven Finger Welcome:** Displays a **"Welcome!"** message if exactly **seven fingers** are detected.  
✅ **Live Webcam Processing:** Real-time detection using the computer’s webcam.  
✅ **Emotion-Based Cropping:** If a surprised face is detected, it displays a cropped version of the face.  

---

## **Installation**
Before running the script, ensure you have Python installed along with the required dependencies.

### **1. Clone the repository**
```bash
git clone https://github.com/yourusername/SevenFingerWelcome.git
cd SevenFingerWelcome
```

### **2. Install Dependencies**
Install the required Python libraries using:
```bash
pip install opencv-python cvzone numpy
```

---

## **Usage**
Run the script using:
```bash
python SevenFingerWelcome.py
```
Press **'q'** to exit the program.

---

## **How It Works**
1. The webcam captures real-time video.
2. **FaceMeshDetector** extracts facial landmarks to determine emotions.
3. **HandDetector** tracks hands and counts raised fingers.
4. If exactly **seven fingers** are detected, a **"Welcome!"** message appears at the center of the screen.

---

## **Demo**
<img src="demo.gif" alt="Demo GIF" width="500">

---

## **Customization**
- Adjust detection sensitivity in:
  ```python
  face_detector = FaceMeshDetector(maxFaces=2, minDetectionCon=0.7, minTrackCon=0.7)
  hand_detector = HandDetector(maxHands=2, detectionCon=0.5, minTrackCon=0.5)
  ```
- Change the **finger count threshold** for triggering the welcome message:
  ```python
  if totalFingers == 7:
      cv2.putText(img, "Welcome!", (img.shape[1] // 2 - 100, img.shape[0] // 2),
                  cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5)
  ```

---

## **Troubleshooting**
- If the webcam does not open, try specifying a different camera index:
  ```python
  cap = cv2.VideoCapture(1)  # Change from 0 to 1 or another index
  ```
- If the hand or face detection is inaccurate, adjust `detectionCon` and `minTrackCon` values.

---

## **License**
This project is open-source under the **MIT License**.

---

## **Author**
Developed by **[Your Name]**. Feel free to contribute or report issues!

🚀 **Enjoy using the SevenFingerWelcome project!** 🎉

