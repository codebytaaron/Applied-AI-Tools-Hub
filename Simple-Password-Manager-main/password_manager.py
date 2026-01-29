import json
import hashlib
import os

FILE_NAME = "passwords.json"


def load_passwords():
    if not os.path.exists(FILE_NAME):
        return {}
    with open(FILE_NAME, "r") as f:
        return json.load(f)


def save_passwords(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=2)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_password(service, password):
    data = load_passwords()
    data[service] = hash_password(password)
    save_passwords(data)
    print("Password saved.")


def get_password(service):
    data = load_passwords()
    if service in data:
        print(f"Stored hash for {service}: {data[service]}")
    else:
        print("No password found for that service.")


def menu():
    print("\nPassword Manager")
    print("1. Add password")
    print("2. Get password")
    print("3. Exit")


while True:
    menu()
    choice = input("Choose an option: ")

    if choice == "1":
        service = input("Service name: ")
        password = input("Password: ")
        add_password(service, password)

    elif choice == "2":
        service = input("Service name: ")
        get_password(service)

    elif choice == "3":
        print("Goodbye.")
        break

    else:
        print("Invalid option.")
