import json

def verify_passkey(input_passkey):
    try:
        with open("passkey.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("❌ No passkey found. Contact admin.")
        return False

    if data["used"]:
        print("❌ Passkey already used.")
        return False

    if input_passkey == data["passkey"]:
        data["used"] = True
        with open("passkey.json", "w") as file:
            json.dump(data, file)

        print("✅ Passkey verified successfully")
        return True
    else:
        print("❌ Invalid passkey")
        return False


if __name__ == "__main__":
    user_passkey = input("Enter passkey: ")
    verify_passkey(user_passkey)
