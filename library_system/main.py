from Auth_System import admin_auth, user_auth


def main_menu():


    while True:

        role = ''
        print("\n===> LIBRARY MANAGEMENT SYSTEM <===\n")
        print("1. Admin")
        print("2. User")
        print("3. Exit\n")

        choice = input("Choose: ").strip()

        print("")

        if choice == "1":
            role = 'admin'
            admin_auth.auth_menu()
        elif choice == "2":
            role = 'user'
            user_auth.auth_menu()
    
        elif choice == "3":
            print("\n--- Thank You for Using Library Management System ---\n")
            break

        else:
            print("\n--- Invalid Choice ---\n")


if __name__ == "__main__":
    main_menu()