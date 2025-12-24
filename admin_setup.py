import hashlib
import json

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

admin_data = {
    "username": "admin",
    "password_hash": hash_password("admin@123")
}

with open("admin_credentials.json", "w") as file:
    json.dump(admin_data, file)

print("Admin credentials created successfully")
