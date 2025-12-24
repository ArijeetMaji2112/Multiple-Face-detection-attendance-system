import cv2
import os
import csv
from datetime import datetime
import geocoder
from collections import deque

# ================= GLOBALS =================
printed_already = set()
recognition_buffer = deque(maxlen=10)   # for stability

CONFIDENCE_THRESHOLD = 65     # lower = stricter
MIN_FACE_SIZE = 120           # ignore far faces

# ================= LOCATION FUNCTION =================
def get_location():
    try:
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            return g.latlng[0], g.latlng[1]
    except:
        pass
    return "N/A", "N/A"

# ================= PATH SETUP =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
MODEL_PATH = os.path.join(BASE_DIR, "models", "face_trainer.yml")
EMPLOYEE_CSV = os.path.join(BASE_DIR, "employee_details.csv")
ATTENDANCE_CSV = os.path.join(BASE_DIR, "attendance", "attendance.csv")

# ================= LOAD HAARCASCADE =================
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
if face_cascade.empty():
    print("❌ Error loading Haarcascade")
    exit()

# ================= LOAD MODEL =================
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(MODEL_PATH)

# ================= LOAD EMPLOYEE DETAILS =================
employee_details = {}

with open(EMPLOYEE_CSV, "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        employee_details[row["Employee_ID"]] = {
            "name": row["Name"],
            "designation": row["Designation"]
        }

# ================= ATTENDANCE CHECK =================
def attendance_marked(emp_id, today):
    if not os.path.exists(ATTENDANCE_CSV):
        return False

    with open(ATTENDANCE_CSV, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 2 and row[0] == today and row[2] == emp_id:
                return True
    return False

# ================= MARK ATTENDANCE =================
def mark_attendance(emp_id, name, designation):
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{emp_id}_{today}"

    if attendance_marked(emp_id, today):
        if key not in printed_already:
            print(f"ℹ️ Attendance already marked for {emp_id}")
            printed_already.add(key)
        return

    time_now = datetime.now().strftime("%H:%M:%S")
    latitude, longitude = get_location()

    file_exists = os.path.exists(ATTENDANCE_CSV)

    with open(ATTENDANCE_CSV, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Date", "Time", "Employee_ID",
                "Name", "Designation",
                "Latitude", "Longitude", "Status"
            ])

        writer.writerow([
            today, time_now, emp_id,
            name, designation,
            latitude, longitude,
            "Present"
        ])

    print(f"✅ Attendance marked for {emp_id}")

# ================= CAMERA START =================
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Fullscreen
cv2.namedWindow("Face Attendance System", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Face Attendance System", 900, 600)  

print("📷 Attendance system started. Press 'q' to quit.")

# ================= MAIN LOOP =================
while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:

        # -------- Distance filter --------
        if w < MIN_FACE_SIZE or h < MIN_FACE_SIZE:
            continue

        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        label, confidence = recognizer.predict(face_img)
        emp_id = f"emp_{label:03d}"

        # -------- Recognition Logic --------
        if confidence < CONFIDENCE_THRESHOLD and emp_id in employee_details:
            recognition_buffer.append(emp_id)
        else:
            recognition_buffer.append("Unknown")

        # -------- Majority Voting --------
        if recognition_buffer.count(emp_id) >= 6:
            name = employee_details[emp_id]["name"]
            designation = employee_details[emp_id]["designation"]

            text = f"{emp_id} | {name}"
            color = (0, 255, 0)

            mark_attendance(emp_id, name, designation)

        elif recognition_buffer.count("Unknown") >= 6:
            text = "Unregistered"
            color = (0, 0, 255)
        else:
            text = "Detecting..."
            color = (0, 255, 255)

        # -------- UI --------
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, text, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
