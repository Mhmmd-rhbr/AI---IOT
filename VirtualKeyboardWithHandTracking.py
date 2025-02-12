import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

def draw_keyboard(img):
    """
    این تابع کیبورد مجازی را رسم می‌کند و موقعیت هر کلید (با حرف مربوطه) را برمی‌گرداند.
    """
    # تعریف ردیف‌های کیبورد به سبک QWERTY، با اضافه کردن دکمه بک‌اسپیس (>) در انتهای ردیف سوم
    keys_rows = [
        list("QWERTYUIOP"),
        list("ASDFGHJKL"),
        list("ZXCVBNM") + [">"]
    ]
    
    key_rects = []  # لیست قرارگیری کلیدها به صورت (x1, y1, x2, y2, letter)
    
    # پارامترهای کلیدها
    key_width = 80
    key_height = 80
    gap = 20  # افزایش فاصله بین کلیدها

    # عرض تصویر (که قبلاً به 1280 تنظیم شده است)
    img_width = img.shape[1]

    # محاسبه موقعیت شروع هر ردیف به‌گونه‌ای که کلیدها به صورت مرکزی نمایش داده شوند
    row_start_x = [
        (img_width - (len(row) * key_width + (len(row) - 1) * gap)) // 2
        for row in keys_rows
    ]
    
    start_y = 50  # فاصله از بالا برای اولین ردیف
    for row_index, row in enumerate(keys_rows):
        y = start_y + row_index * (key_height + gap)
        start_x = row_start_x[row_index]
        for i, key in enumerate(row):
            x = start_x + i * (key_width + gap)
            # ذخیره مختصات و حرف مربوطه
            key_rects.append((x, y, x + key_width, y + key_height, key))
            # انتخاب رنگ: رنگ قرمز برای دکمه بک‌اسپیس و آبی برای حروف
            if key == ">":
                key_color = (0, 0, 255)
            else:
                key_color = (255, 0, 0)
            cv2.rectangle(img, (x, y), (x + key_width, y + key_height), key_color, cv2.FILLED)
            cv2.putText(img, key, (x + 25, y + 55), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
    
    return img, key_rects

def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)  # تنظیم عرض
    cap.set(4, 720)   # تنظیم ارتفاع

    # ایجاد شیء HandDetector بدون استفاده از آرگومان staticMode
    detector = HandDetector(maxHands=2, detectionCon=0.7, minTrackCon=0.7)
    
    output_text = ""      # متن خروجی شامل حروف انتخاب شده
    pressed_keys = []     # لیست کلیدهایی که در فریم جاری لمس شده‌اند (برای جلوگیری از لمس‌های مکرر)

    while True:
        success, img = cap.read()
        if not success:
            print("خطا در دریافت تصویر از دوربین.")
            break

        # آینه‌وار کردن تصویر جهت نمایش طبیعی
        img = cv2.flip(img, 1)
        
        # پیدا کردن دست‌ها
        hands, img = detector.findHands(img, draw=True, flipType=True)
        
        # رسم کیبورد و دریافت موقعیت کلیدها
        img, key_rects = draw_keyboard(img)
        
        # اگر دستی شناسایی شده باشد
        if hands:
            for hand in hands:
                lmList = hand.get('lmList', [])
                if len(lmList) < 9:
                    continue

                # بررسی وضعیت انگشت‌ها (استفاده از متد fingersUp)
                fingers = detector.fingersUp(hand)
                # تنها در صورتی که انگشت اشاره (index finger) باز است، تایپ فعال می‌شود
                if fingers[1] != 1:
                    continue

                # استفاده از نوک انگشت اشاره (landmark شماره 8)
                index_finger_tip = lmList[8]
                ix, iy = index_finger_tip[0], index_finger_tip[1]
                
                # رسم دایره روی نوک انگشت
                cv2.circle(img, (ix, iy), 15, (0, 255, 0), cv2.FILLED)
                
                # بررسی برخورد نوک انگشت با هر کلید
                for rect in key_rects:
                    x1, y1, x2, y2, key = rect
                    if x1 < ix < x2 and y1 < iy < y2:
                        if key not in pressed_keys:
                            if key == ">":
                                print("Backspace Pressed")
                                output_text = output_text[:-1] if output_text else ""
                            else:
                                print(f"Key Pressed: {key}")
                                output_text += key
                            pressed_keys.append(key)
                            
                            # تغییر رنگ کلید برای نشان دادن لمس
                            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, key, (x1 + 25, y1 + 55), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        # حذف کلیدهای لمس شده زمانی که انگشت از روی کلید خارج شود (debounce ساده)
        if hands:
            lmList = hands[0].get('lmList', [])
            if len(lmList) >= 9:
                index_finger_tip = lmList[8]
                ix, iy = index_finger_tip[0], index_finger_tip[1]
                finger_in_key = False
                for rect in key_rects:
                    x1, y1, x2, y2, _ = rect
                    if x1 < ix < x2 and y1 < iy < y2:
                        finger_in_key = True
                        break
                if not finger_in_key:
                    pressed_keys = []
        else:
            pressed_keys = []

        # نمایش متن خروجی در یک ناحیه در پایین تصویر
        cv2.rectangle(img, (50, 350), (1230, 450), (200, 200, 200), cv2.FILLED)
        cv2.putText(img, output_text, (60, 420), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)

        cv2.imshow("Virtual Keyboard", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()