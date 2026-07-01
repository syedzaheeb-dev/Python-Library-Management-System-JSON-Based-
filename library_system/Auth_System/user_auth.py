from utils import (
    load_users,
    save_user_data,
    password_validation,
    hash_password
)


# ==================================================
# Authentication Features
# ==================================================

def register_user():

    users = load_users()

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    from utils import validate_email
    email = validate_email("user")

    if email is None:
        return

    password = password_validation()

    if password is None:
        return

    hashed_password = hash_password(password)

    new_user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': hashed_password,
        'favourites': [],
        'history': [],
        'ratings': {},
        'books_read': 0
    }

    users.append(new_user)

    save_user_data(users)

    print('\n---Email has been Registered Successfully---\n')


def user_login():

    users = load_users()

    email = input("Email: ")
    password = input("Password: ")

    hashed_password = hash_password(password)

    for user in users:

        if (
            user['email'] == email
            and
            user['password'] == hashed_password
        ):
            print(f"\n---Login Successfully---\n")
            return user

    print(f"\n---Email or password is incorrect---\n")


# ==================================================
# Menu
# ==================================================

def auth_menu():

    print("\n===>AUTH SYSTEM<===\n")

    actions = [
        'SignUp',
        'Login',
        'LogOut'
    ]

    while True:

        for i, d in enumerate(actions, start=1):
            print(f"{i}. {d}")

        print("")

        choice = input('Choose: ').strip()

        print("")

        if choice == "1":
            register_user()

        elif choice == "2":
            from main_features import user
            current_user = user_login()
            if current_user:
                user.user_panel(current_user)   # <-- fix

        elif choice == "3":

            print("\n---Logging Out---\n")
            break

        else:

            print("\n---Invalid Choice---\n")


if __name__ == "__main__":
    auth_menu()
    
