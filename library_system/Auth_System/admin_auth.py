from utils import (
    load_admin,
    save_admin_data,
    password_validation,
    hash_password,
)

from main_features import admin




# ==================================================
# Authentication Features
# ==================================================

def register_admin():

    admins = load_admin()

    first_name = input("First Name: ")
    last_name = input("Last Name: ")

    full_name = first_name + " " + last_name


    from utils import validate_email
    email = validate_email('admin')

    if email is None:
        return

    password = password_validation()

    if password is None:
        return

    hashed_password = hash_password(password)

    new_admin = {
        'full_name': full_name,
        'email': email,
        'password': hashed_password,
        'books_added': 0,
        'remove_books': 0,
    }

    admins.append(new_admin)

    save_admin_data(admins)

    print('\n---Admin has been Registered Successfully---\n')


def admin_login():

    admins = load_admin()

    email = input("Email: ")
    password = input("Password: ")

    hashed_password = hash_password(password)

    for admin_data in admins:

        if (
            admin_data['email'] == email
            and
            admin_data['password'] == hashed_password
        ):
            print(
                f"\n---Admin has Logged in Successfully---\n"
            )
            return admin_data

    print(f"\n---Email or password is incorrect---\n")
    return None


# ==================================================
# Admin Records
# ==================================================

def view_admins():

    admins = load_admin()

    if not admins:
        print("\n---There is No admin yet---\n")
        return

    for index, data in enumerate(admins, start=1):

        print(
            f"{index}. Full Name : {data['full_name']} | "
            f"Email : {data['email']}\n"
            f"Books Added : {data['books_added']}"
            f"\nBooks Removed : {data['remove_books']}\n"
        )


# ==================================================
# Menu
# ==================================================

def auth_menu():

    actions = [
        'SignUp',
        'Login',
        'View',
        'LogOut'
    ]

    while True:

        print("\n===>AUTH SYSTEM<===\n")

        for i, d in enumerate(actions, start=1):
            print(f"{i}. {d}")

        print("")

        choice = input('Choose: ').strip()

        print("")

        if choice == "1":
            register_admin()

        elif choice == "2":

            current_admin = admin_login()

            if current_admin:
                admin.admin_panel(current_admin)

        elif choice == "3":
            view_admins()

        elif choice == "4":
            print("\n---Logging Out---\n")
            break

        else:
            print("\n---Invalid Choice---\n")


if __name__ == "__main__":
    auth_menu()
