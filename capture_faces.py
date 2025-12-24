import cv2
import os
import time

# ================= EMPLOYEE SETUP =================
emp_id = "emp_004"   # change for new employee
save_path = f"dataset/{emp_id}"
os.makedirs(save_path, exist_ok=True)

# ================= FACE SETTINGS =================
angles = [
    ("FRONT", "Look STRAIGHT at the camera"),
    ("LEFT", "Turn your face LEFT"),
    ("RIGHT", "Turn your face RIGHT"),
    ("UP", "Look UP"),
    ("DOWN", "Look DOWN")
]

images_per_angle = 5
img_size = (200, 200)

# ================= LOAD HAARCASCADE =================
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("\n===== MULTI-ANGLE FACE CAPTURE =====")
print("Total images: 25 (5 per angle)\n")

img_count = 0

for angle_name, instruction in angles:
    print(f"\n➡ {instruction}")
    time.sleep(2)  # time to adjust face

    captured = 0

    while captured < images_per_angle:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, img_size)

            img_count += 1
            captured += 1

            img_name = f"{img_count}_{angle_name}.jpg"
            cv2.imwrite(os.path.join(save_path, img_name), face_img)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # ================= DISPLAY =================
        cv2.putText(frame, instruction, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        cv2.putText(frame, f"Images: {img_count}/25", (10, 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Face Capture", frame)
        time.sleep(0.5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

cap.release()
cv2.destroyAllWindows()

print("\n✅ Face capture completed!")
print(f"📂 25 images saved in: {save_path}")
