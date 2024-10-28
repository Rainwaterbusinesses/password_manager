from cryptography.fernet import Fernet
import os
import json

def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

def encrypt_password(password, key):
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password

def decrypt_password(encrypted_password, key):
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password).decode()
    return decrypted_password

def save_password(site, username, password, key):
    encrypted_password = encrypt_password(password, key)
    data = load_data()

    data[site] = {"username": username, "password": encrypted_password.decode()}
    
    with open("passwords.json", "w") as file:
        json.dump(data, file)
    print(f"Password for {site} saved successfully.")

def load_data():
    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            return json.load(file)
    return {}

def get_password(site, key):
    data = load_data()
    if site in data:
        encrypted_password = data[site]["password"].encode()
        username = data[site]["username"]
        password = decrypt_password(encrypted_password, key)
        print(f"Site: {site}\nUsername: {username}\nPassword: {password}")
    else:
        print(f"No password found for {site}.")

def main():
    key = load_key()
    while True:
        print("\nPassword Manager")
        print("1. Add a new password")
        print("2. Retrieve a password")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            site = input("Enter the site name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            save_password(site, username, password, key)
        elif choice == "2":
            site = input("Enter the site name: ")
            get_password(site, key)
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
