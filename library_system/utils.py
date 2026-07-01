import json
import os
import hashlib


BASE_DIR = os.path.dirname(__file__)
JSON_DIR = os.path.join(BASE_DIR, "json_files")

ADMIN_FILE = os.path.join(JSON_DIR, "admin_auth.json")
BOOKS_FILE = os.path.join(JSON_DIR, "books.json")
USERS_FILE = os.path.join(JSON_DIR, "user_auth.json")



# USER LOAD/DUMP DATA

def load_users():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_user_data(user):
    with open(USERS_FILE, 'w') as f:
        json.dump(user, f, indent=4)


# ---------------------------------------------------------------------------------------------
# ADMIN LOAD/DUMP DATA

def load_admin():
    if not os.path.exists(ADMIN_FILE):
        return []

    try:
        with open(ADMIN_FILE, 'r') as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_admin_data(admin):
    with open(ADMIN_FILE, 'w') as f:
        json.dump(admin, f, indent=4)


# ---------------------------------------------------------------------------------------------
# BOOKS LOAD/DUMP DATA

def load_books():
    if not os.path.exists(BOOKS_FILE):
        return []

    try:
        with open(BOOKS_FILE, 'r') as f:
            return json.load(f)

    except json.JSONDecodeError:
        return []


def save_books(book):
    with open(BOOKS_FILE, 'w') as f:
        json.dump(book, f, indent=4)


# ---------------------------------------------------------------------------------------------


def password_validation():

    special_char = "~!`@#$%^&*,.<>/?:;\|+=-_"

    trail_password = input("Enter the Password: ")
    com_password = input("Confirm Password: ")

    if len(trail_password) < 6:
        print("\n---Password Should be greater than or equal 6 letters or numbers---\n")
        return None

    elif not any(char in special_char for char in trail_password):
        print('\n---Password should contain atleast 1 special character ---\n')
        return None

    elif trail_password != com_password:
        print("\n---Enter correct Password---\n")
        return None

    return trail_password


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()



def validate_email(role):

    existing_users = load_users()
    existing_admin = load_admin()



    username = input("Username for email: ").strip()

    special_characters = "~!`@#$%^&*<>/?:;|+=- "

    domains = ['@gmail.com', '@yahoo.com']


    if role == 'admin':
        for user in existing_admin:
            if (
                user['email'] == username + '@gmail.com'
                or
                user['email'] == username + '@yahoo.com'
            ):
                print('\n---Email Already Exists---\n')
                return None          

    elif role == 'user':
        for user in existing_users:
            if (
                user['email'] == username + '@gmail.com'
                or
                user['email'] == username + '@yahoo.com'
            ):
                print('\n---Email Already Exists---\n')
                return None
            
                      
    if len(username) < 4:

        print(
            '\n---Email Should be greater than '
            'or equal to length 4---\n'
        )
        return None

    elif any(char in special_characters for char in username):

        print(
            '\n---Email Only Contains alphabets , '
            'numbers , . and _---\n'
        )
        return None

    else:

        for index, value in enumerate(domains, start=1):
            print(f"{index}. {value}")

        choice = input('Choose : ').strip()

        if choice == '1':
            email = username + domains[0]

        elif choice == '2':
            email = username + domains[1]

        else:
            print('\n---Invalid Domain Choice---\n')
            return None

    return email

