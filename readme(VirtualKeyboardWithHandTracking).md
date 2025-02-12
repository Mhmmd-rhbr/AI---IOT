# 🖥️ Virtual Keyboard with Hand Tracking

_A Python-based virtual keyboard using OpenCV, cvzone, and Mediapipe for real-time hand tracking._

---

## 🚀 Overview
This project is a **virtual keyboard** controlled by **hand gestures** using a webcam. It detects a user's hand and allows them to "type" by hovering their **index finger** over the virtual keys.

The keyboard is implemented in **Python** using:
- `OpenCV` for video processing
- `cvzone` (built on `Mediapipe`) for **hand tracking**
- `NumPy` for numerical operations

This is a **fun and interactive** project where you can type without a physical keyboard! 🕶️💻

---

## 🎯 Features
✅ **Real-time hand tracking** using `cvzone.HandTrackingModule`  
✅ **Virtual keyboard layout** with full **QWERTY** design  
✅ **Detects index finger movement** and registers keystrokes  
✅ **Backspace support (`>` key)** to delete typed characters  
✅ **Prevents accidental key presses** (debounce mechanism)  
✅ **Only registers key presses when the index finger is extended** (avoids typing while making a fist)  
✅ **Designed for use with a webcam**  

---

## 🛠️ Installation & Setup
### **1️⃣ Install Dependencies**
Make sure you have Python installed, then install the required libraries:
```bash
pip install opencv-python numpy cvzone mediapipe
```

### **2️⃣ Run the Script**
Simply execute the script:
```bash
python 12_1_virtualkeyboard.py
```

### **3️⃣ Controls**
- **Hover** your **index finger** over the keys to "press" them.
- **Use the `>` key** (backspace) to delete characters.
- **Close your fist** to disable typing.
- **Press `Q` on your keyboard** to **exit** the program.

---

## 🧩 How It Works
### **Hand Tracking with Mediapipe**
The script detects hands using `cvzone.HandTrackingModule`, which utilizes **Mediapipe's Hand Tracking** model.  
Each hand contains **21 key landmarks** to identify fingers' positions.

### **Virtual Keyboard Logic**
- The keyboard layout is generated dynamically.
- Each key has a **bounding box** that detects finger presence.
- When the **index finger's tip** (landmark **#8**) is within a key's area, it registers a key press.

### **Debounce System**
- The program prevents **accidental multiple presses** by storing previously pressed keys.
- The **fingersUp** method ensures that typing only happens when the **index finger is extended**.

---

## 🖥️ File Structure
```
📂 ML_using_sklearn-master
 ├── 📄 requirements.txt           # Dependencies
 ├── 📄 README.md                  # This file
 ├── 📂 assets/                    # (Optional) Images, GIFs for documentation
```

---

## 🎮 Planned Improvements
🚀 Add a **customizable keyboard layout**  
🚀 Add a **numeric keypad mode**  
🚀 Add **sound effects** for keypress feedback  
🚀 Implement a **word prediction system**  

---

## 🤝 Contributing
💡 Found a bug? Have a cool feature idea? Feel free to contribute!  
- **Fork** the repo  
- Create a **new branch**  
- Submit a **pull request**  

---

## 🏆 Credits
Developed by **[Your Name]**  
Using **OpenCV, cvzone, and Mediapipe**  

🛠️ **Inspired by AI-driven gesture recognition systems!**  

---

## 📝 License
MIT License – Free to use and modify 🚀

