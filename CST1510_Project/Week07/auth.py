import bcrypt
from pathlib import Path

USER_DATA_FILE = Path("users.txt")

def hash_password(plain_text_password):
    password_bytes = plain_text_password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    try:
        pw_bytes = plain_text_password.encode('utf-8')
        hash_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(pw_bytes, hash_bytes)
    except Exception:
        return False

def user_exists(username):
    if not USER_DATA_FILE.exists():
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts and parts[0] == username:
                return True
    return False

def register_user(username, password, role='user'):
    if user_exists(username):
        print(f"Username '{username}' already exists.")
        return False
    hashed = hash_password(password)
    with open(USER_DATA_FILE, 'a') as f:
        f.write(f"{username},{hashed},{role}\n")
    print(f"User '{username}' registered.")
    return True

def login_user(username, password):
    if not USER_DATA_FILE.exists():
        print("No users registered yet.")
        return False
    with open(USER_DATA_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 2 and parts[0] == username:
                stored_hash = parts[1]
                if verify_password(password, stored_hash):
                    print(f"Welcome, {username}!")
                    return True
                else:
                    print("Invalid password.")
                    return False
    print("Username not found.")
    return False

if __name__ == '__main__':
    # basic interactive CLI for quick testing
    while True:
        print("\n1) Register\n2) Login\n3) Exit")
        choice = input("Choose: ").strip()
        if choice == '1':
            uname = input("Username: ").strip()
            pwd = input("Password: ").strip()
            register_user(uname, pwd)
        elif choice == '2':
            uname = input("Username: ").strip()
            pwd = input("Password: ").strip()
            login_user(uname, pwd)
        else:
            break
