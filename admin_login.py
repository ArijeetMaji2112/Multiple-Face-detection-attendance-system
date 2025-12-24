import hashlib
import json
import getpass

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def admin_login():
    username = input("Enter admin username: ")
    password = getpass.getpass("Enter admin password: ")

    with open("admin_credentials.json", "r") as file:
        admin_data = json.load(file)

    if (username == admin_data["username"] and
        hash_password(password) == admin_data["password_hash"]):
        print("✅ Admin login successful")
        return True
    else:
        print("❌ Invalid admin credentials")
        return False

if __name__ == "__main__":
    admin_login()
