import cv2
import os
import csv
from datetime import datetime
def load_employee_details(file_path="employee_details.csv"):
    emp_details = {}
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            emp_details[row["Employee_ID"]] = {
                "name": row["Name"],
                "designation": row["Designation"]
            }
    return emp_details
def already_marked_today(emp_id, today, file_path="attendance/attendance.csv"):
    try:
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if row[0] == today and row[2] == emp_id:
                    return True
    except FileNotFoundError:
        return False
    return False
# Load trained model
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("models/face_trainer.yml")

# Haarcascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Label mapping (same order as training)
label_map = {
    1: "emp_001",
    2: "emp_002",
    3: "emp_003"
}
employee_details = load_employee_details()
attendance_file = "attendance/attendance.csv"

# To prevent duplicate entry in same run
marked = set()
session_marked = set()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        label, confidence = recognizer.predict(face_img)
        emp_id = label_map.get(label, "Unknown")

        # Decide once
        if confidence < 120 and emp_id != "Unknown":
            display_id = emp_id
        else:
            display_id = "Unknown"
        if confidence < 100:  
            emp_id = label_map.get(label, "Unknown")
            if emp_id != "Unknown" and emp_id in employee_details:
                name = employee_details[emp_id]["name"]
                designation = employee_details[emp_id]["designation"]
            else:
                name = "Unknown"
                designation = ""

            if emp_id != "Unknown":
                if emp_id != "Unknown"and emp_id not in session_marked:
                    today = datetime.now().strftime("%Y-%m-%d")
                    time_now = datetime.now().strftime("%H:%M:%S")

                    if not already_marked_today(emp_id, today):
                        with open("attendance/attendance.csv", "a", newline="") as file:
                            writer = csv.writer(file)
                            writer.writerow([today, time_now, emp_id, name, designation, "Present"])
                        print(f"Attendance marked for {emp_id}")
                    else:
                        print(f"Attendance already marked for {emp_id}")
                    session_marked.add(emp_id)
            else:
                name = "Unknown"
                designation = ""
            if emp_id not in marked:
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                with open(attendance_file, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([date, time, emp_id, "Present"])

                marked.add(emp_id)

            cv2.putText(frame, f"{name}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        else:
            cv2.putText(frame, f"{designation}", (x, y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)

    cv2.imshow("Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

