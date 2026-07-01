from utils import (
    load_admin,
    load_books,
    load_users,
    save_books,
    save_admin_data,
)
import random

# =========================
# Trending Features
# =========================


def update_trending_scores():
    loading_books = load_books()

    for book in loading_books:
        if book['trending_score'] == 0:
            book['trending_score'] = round(
                book['ratings']['total_ratings'] * 3 +
                book['favourite_count'] * 1.5 +
                book['read_count'] * 1, 1
            )
            print("\n--- Trending Score Updated Successfully ---\n")

        
    save_books(loading_books)



def generate_random_stats():
    loading_books = load_books()

    if not loading_books:
        print("\n---There is No Book---\n")
        return

    for book in loading_books:
        if book['read_count'] == 0 and book['favourite_count'] == 0:
            book['read_count'] = random.randint(10, 500)
            book['favourite_count'] = random.randint(1, 100)

            users = random.randint(1, 100)
            average = round(random.uniform(1.0, 5.0), 1)

            book['ratings']['users_count'] = users
            book['ratings']['average_rating'] = average
            book['ratings']['total_ratings'] = round(users * average, 1)

    save_books(loading_books)

    print("\n---Random Stats Added Successfully---\n")




# ==================================================
# Category & uid Features
# ==================================================

def choose_category():

    categories = [
        'Sciense Fiction',
        'Romance',
        'Dark Romance',
        'Fantasy',
        'Dark Fantasy',
        'AI & Technology',
        'Space & Universe',
        'Horror',
        'History',
        'ACTION',
        'Thriller & Mystery'
    ]

    for i, v in enumerate(categories, start=1):
        print(f"{i}. {v}")

    categories.append("Custom Category")

    choice = input("Choose Category : ").strip()

    if choice.isdigit():

        choice = int(choice)

        if 1 <= choice <= len(categories) - 1:
            return categories[choice - 1]

        elif choice == len(categories):
            custom_category = input(
                "Enter Custom Category: "
        ).strip()

            return custom_category

    print("\n--INVALID CHOICE--\n.Please Try again...\n")
    return None


def generate_unique_book_id():

    loading_books = load_books()

    unique_id = input("Unique ID for Book: ")

    for identity in loading_books:
        if identity['uid'] == unique_id:
            print(
                "\n---Book On this Unique ID Already Exists---"
                "\n---Please Use Different uid---\n"
            )
            return None

    if not (unique_id.startswith("B") and len(unique_id) == 6):
        print(
            "==> Incorrect uid, Please Enter the Correct uid"
            "\n==> Correct Format"
            "\n\t=> uid Should Start with B."
            "\n\t=> uid Should have 5 Letters or Digits after first 'B'."
        )
        return None

    return unique_id


# ==================================================
# Book Management
# ==================================================

def add_book():

    loading_admin = load_admin()
    books = load_books()

    uid = generate_unique_book_id()

    if uid is None:
        return

    title = input("Title: ").strip()
    author = input("Author: ").strip()

    print("")

    category_chosen = choose_category()

    if category_chosen is None:
        return

    print("")
    print(
        f"\nUniqueID : {uid}\n"
        f"Title : {title}\n"
        f"Author : {author} | Category : {category_chosen}"
    )
    print("")

    confirmation = ['YES', 'NO']

    for i, v in enumerate(confirmation, start=1):
        print(f"{i}. {v}")

    choose = input(
        "Are You Sure You Wanna Add the Book: "
    ).strip().lower()

    if choose == "yes":

        new_book = {
            'uid': uid,
            'title': title,
            'author': author,
            'category': category_chosen,
            'read_count': 0,
            'favourite_count': 0,
            'ratings': {
                'users_count': 0,
                'total_ratings': 0,
                'average_rating': 0,
            },
            'trending_score' : 0
        }

        for admin in loading_admin:
            admin['books_added'] += 1

        save_admin_data(loading_admin)

    else:
        print(f"\nBook Uploading Cancel...\n")
        return

    print(f"\n--- BOOK ADDED SUCCESSFULLY ---\n")

    books.append(new_book)
    save_books(books)


def view_books():

    loading_books = load_books()

    if not loading_books:
        print(f"\n--- There is No Book yet ---\n")
        return

    for index, value in enumerate(loading_books, start=1):

        print(
            f"{index}. uid : {value['uid']} \n"
            f"Title : {value['title']} \n"
            f"Author : {value['author']} | "
            f"Category : {value['category']}"
            f"\nRead Count : {value['read_count']} | "
            f"Favourite : {value['favourite_count']} | "
            f"Ratings : {value['ratings']}\n"
            f"Trending Score : {value['trending_score']}\n{'-' * 30}\n"
        )


def remove_book():

    loading_admin = load_admin()
    loading_books = load_books()

    if not loading_books:
        print("\n---There is No Book---\n")
        return

    book_id = input("Enter uid to Remove Book: ")

    book = None

    for b in loading_books:
        if b['uid'] == book_id:
            book = b
            break

    if not book:
        print("Book Not Found")
        return

    print("\n1. YES\n2. NO")

    choose = input(
        "Are You Sure You Want to Remove the Book: "
    ).strip().lower()

    if choose != "yes":
        print("\nConfirmation Access for Remove Book has been Denied\n")
        return

    new_book_data = [
        b for b in loading_books
        if b['uid'] != book_id
    ]

    for admin in loading_admin:
        admin['remove_books'] = (
            admin.get('remove_books', 0) + 1
        )

    save_admin_data(loading_admin)
    save_books(new_book_data)

    print("\n---Book Removed Successfully---\n")


# ==================================================
# User Management
# ==================================================

def view_users():

    loading_users = load_users()

    if not loading_users:
        print(f"\n---There is No User---\n")
        return

    for index, value in enumerate(loading_users, start=1):

        print(
            f"{index}."
            f"Name : {value['first_name']} {value['last_name']} | "
            f"Email : {value['email']} \n"
            f"Books Read : {value['books_read']}\n"
            f"Favourite : {value['favourites']}\n"
            f"History : {value['history']}\n"
            f"Ratings : {value['ratings']}\n"
            )


def search_user():

    loading_users = load_users()

    if not loading_users:
        print(f"\n---There is No User---\n")
        return

    found = False

    name = input('Enter the User Name to find: ')

    for user in loading_users:

        name = name.lower()

        if (
            name in user["first_name"].lower()
            or name in user["last_name"].lower()
            ):

            found = True

            print()
            print(
                f"Name : {user['first_name']} {user['last_name']}| "
                f"Email : {user['email']} \n"
                f"Books Read : {user['books_read']}\n"
                f"Favourite : {user['favourites']}\n"
                f"History : {user['history']}\n"
                f"Ratings : {user['ratings']}\n"
            )
            

    if not found:
        print(f"\n==> USER NOT FOUND <==\n")


# ==================================================
# Admin Panel
# ==================================================

def admin_panel(logged_in_admin):

    actions = [
        'Add Book',
        'View Books',
        'Remove Book',
        'View Users',
        'Search User',
        'LogOut',
        'Generate Random Stats',
        'Update Trending Score',
    ]

    print("\n===> WELCOME BACK <===\n")

    while True:

        print("\n===>ADMIN PANEL<===\n")

        for i, d in enumerate(actions, start=1):
            print(f"{i}. {d}")

        print("")

        choice = input('Choose: ').strip()

        print("")

        if choice == "1":
            add_book()

        elif choice == "2":
            view_books()

        elif choice == "3":
            remove_book()

        elif choice == "4":
            view_users()

        elif choice == "5":
            search_user()

        elif choice == "6":
            print("\n---Logging Out---\n")
            break
        
        elif choice == "7":
            generate_random_stats()
        
        elif choice == "8":
            update_trending_scores()

        else:
            print("\n---Invalid Choice---\n")


if __name__ == "__main__":
    admin_panel(None)
