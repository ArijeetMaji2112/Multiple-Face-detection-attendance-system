import os
import csv
from passkey_verify import verify_passkey

def register_employee():
    print("\n🔐 Employee Registration")
    passkey = input("Enter admin passkey: ")

    if not verify_passkey(passkey):
        print("❌ Registration denied.")
        return

    emp_id = input("Enter Employee ID (e.g. emp_003): ").strip()
    name = input("Enter Employee Name: ").strip()
    designation = input("Enter Designation: ").strip()

    # Save employee details
    file_exists = os.path.isfile("employee_details.csv")

    with open("employee_details.csv", "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Employee_ID", "Name", "Designation"])

        writer.writerow([emp_id, name, designation])

    # Create dataset folder
    dataset_path = os.path.join("dataset", emp_id)
    os.makedirs(dataset_path, exist_ok=True)

    print(f"\n✅ Employee {emp_id} registered successfully")
    print("📸 Now run capture_faces.py to collect face images")

if __name__ == "__main__":
    register_employee()
