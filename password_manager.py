import sqlite3

def create_db():
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY,
            account TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_db()



from cryptography.fernet import Fernet
# Generate a key for encryption
def generate_key():
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

# Load the key
def load_key():
    return open('secret.key', 'rb').read()

generate_key()  # Run this once to generate the key

key = load_key()
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password).decode()



def store_password(account, username, password):
    encrypted_password = encrypt_password(password)
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('INSERT INTO passwords (account, username, password) VALUES (?, ?, ?)', (account, username, encrypted_password))
    conn.commit()
    conn.close()

def retrieve_password(account):
    conn = sqlite3.connect('password_manager.db')
    c = conn.cursor()
    c.execute('SELECT username, password FROM passwords WHERE account = ?', (account,))
    result = c.fetchone()
    conn.close()
    if result:
        username, encrypted_password = result
        return username, decrypt_password(encrypted_password)
    return None, None



import string
import random

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))



def main():
    while True:
        print("\nPassword Manager")
        print("1. Store a new password")
        print("2. Retrieve a password")
        print("3. Generate a strong password")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            account = input("Enter the account name: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            store_password(account, username, password)
            print("Password stored successfully!")
        
        elif choice == '2':
            account = input("Enter the account name: ")
            username, password = retrieve_password(account)
            if username:
                print(f"Username: {username}")
                print(f"Password: {password}")
            else:
                print("No password found for the given account.")
        
        elif choice == '3':
            length = int(input("Enter the length of the password: "))
            strong_password = generate_strong_password(length)
            print(f"Generated strong password: {strong_password}")
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()