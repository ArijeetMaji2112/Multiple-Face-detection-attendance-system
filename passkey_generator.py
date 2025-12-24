import json
import secrets
from admin_login import admin_login

def generate_passkey():
    # Generate a secure random passkey
    passkey = secrets.token_hex(4)  # 8-character hex key

    data = {
        "passkey": passkey,
        "used": False
    }

    with open("passkey.json", "w") as file:
        json.dump(data, file)

    print("\n🔑 New passkey generated successfully")
    print("PASSKEY:", passkey)

if __name__ == "__main__":
    if admin_login():
        generate_passkey()
