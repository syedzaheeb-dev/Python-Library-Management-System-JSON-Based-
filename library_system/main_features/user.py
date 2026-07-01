from utils import (
    load_books,
    load_users,
    save_books,
    save_user_data,
)
import time

# =========================
# Book Actions
# =========================

def book_actions(selected_book, current_user):

    loading_books = load_books()
    loading_users = load_users()

    def sync_books():
        for i , b in enumerate(loading_books):
            if b['uid'] == selected_book['uid']:
                loading_books[i] = selected_book
                break
    def sync_users():
        for i , u in enumerate(loading_users):
            if u['email'] == current_user['email']:
                loading_users[i] = current_user
                break

    while True:
        actions = ['Read', 'Favourite' , 'Ratings' , 'Home Page']

        for index , value in enumerate(actions , start=1):
            print(f"{index}. {value}")
        
        choice = input("Choose: ").strip()
        print("")

        if choice == '1':
            print("Open the book")
            time.sleep(2)
            print("Reading the book")
            time.sleep(2)
            print("Close the book")
            time.sleep(2)

            if selected_book['uid'] not in current_user['history']:
                selected_book['read_count'] += 1
                current_user['history'].append(selected_book['uid'])
                current_user['books_read'] += 1

            sync_books()
            sync_users()
            save_books(loading_books)
            save_user_data(loading_users)
            from main_features import admin
            admin.update_trending_scores()

# ===========================================================================================
        
        
        elif choice == '2':
            if selected_book['uid'] not in current_user['favourites']:
                current_user['favourites'].append(selected_book['uid'])
                selected_book['favourite_count'] += 1
            else:
                print("\n--- You have already favouritize the book ---\n")

            print(f"\nFavourite : {selected_book['favourite_count']}\n")

            sync_books()
            sync_users()
            save_books(loading_books)
            save_user_data(loading_users)
            from main_features import admin
            admin.update_trending_scores()


# ===========================================================================================

        elif choice == "3":
            try:
                rating = float(input("Ratings: "))

                if 1<= rating <= 5:
                    if selected_book['uid'] in current_user['ratings']:

                        old_rating = current_user['ratings'][selected_book['uid']]

                        selected_book['ratings']['total_ratings'] -= old_rating
                        selected_book['ratings']['total_ratings'] += rating

                    else:
                        selected_book['ratings']['total_ratings'] += rating
                        selected_book['ratings']['users_count'] += 1
                    current_user['ratings'][selected_book['uid']] = rating
                    
                    selected_book['ratings']['average_rating'] = round(
                        selected_book['ratings']['total_ratings'] /
                        selected_book['ratings']['users_count'],1
                    )

                    print(f"{'-'*30}\nAverage Rating : {selected_book['ratings']['average_rating']}"
                        f"\n{'-'*30}")
                    
                    sync_books()
                    sync_users()
                    save_books(loading_books)
                    save_user_data(loading_users)
                    from main_features import admin
                    admin.update_trending_scores()
    

                else:
                    print('\nInvalid Ratings\n')
                    break 
            except ValueError:
                print("\nRatings Should be in numbers\n")
                
        elif choice == "4":

            print("\nBack to Home Page...\n")
            break

        else:
            print("\n--- Invalid Choice ---\n")


# =========================
# Home Page
# =========================

def home_page(current_user):

    loading_books = load_books()

    print("")

    if not loading_books:
        print("--- There is No Book yet ---")
        return

    while True:

        home_books = loading_books[-10:]

        for index, value in enumerate(home_books, start=1):
            print(f"{index}. Title : {value['title']} \n")

        choice = input("Choose Book : ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(home_books):

            selected_book = home_books[int(choice) - 1]

            print(
                f"\n\t{selected_book['uid']} \n"
                f"--> Title : {selected_book['title']} \n"
                f"--> Author : {selected_book['author']} | "
                f"Category : {selected_book['category']}\n"
                f"--> Read Count : {selected_book['read_count']}\n"
                f"--> Favourite : {selected_book['favourite_count']}\n"
                f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
                f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
                f"{'-' * 30}\n"
            )

            book_actions(selected_book, current_user)

        else:
            print("Back to Home Page")
            break


# =========================
# Trending Page
# =========================

def get_trending_books():

    loading_books = load_books()

    working_books = loading_books.copy()

    trending_list = sorted(working_books , key=lambda book: 
                           book['trending_score'],
                           reverse=True)




    return trending_list


def show_trending_books(current_user):

    trend = get_trending_books()

    if not trend:
        print("No Trending Books Available")
        return

    for index, book in enumerate(trend, start=1):
        print(f"{index}. {book['title']} | {book['uid']}")

    choice = input("Choose from the list: ")

    if choice.isdigit() and 1 <= int(choice) <= len(trend):

        selected_book = trend[int(choice) - 1]

        print("\nBACK")

        print(
            f"\n\t{selected_book['uid']} \n"
            f"--> Title : {selected_book['title']} \n"
            f"--> Author : {selected_book['author']} | "
            f"Category : {selected_book['category']}\n"
            f"--> Read Count : {selected_book['read_count']}\n"
            f"--> Favourite : {selected_book['favourite_count']}\n"
            f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
            f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
            f"{'-' * 30}\n"
            )
        book_actions(selected_book, current_user)

    else:
        print("Exitting the system")
        return



# =========================
# Category Page
# =========================

    
def category_search(current_user):
    loading_books = load_books()

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
        'Thriller & Mystery',
        'Back to Menu'
    ]

    for index, value in enumerate(categories, start=1):
        print(f"{index}. {value}")

    choice_category = input("Choose category: ")

    if not choice_category.isdigit() or not (1 <= int(choice_category) <= len(categories)):
        print("--- Incorrect Choice of Categories ---\n")
        return

    selected_category = categories[int(choice_category) - 1]

    choosen_category = []

    for book in loading_books:
        if book['category'] == selected_category:
            choosen_category.append(book)

    if not choosen_category:
        print("\n---> No Books Found in This Category <---\n")
        return

    print("\n--- Available Books ---\n")

    for index, book in enumerate(choosen_category, start=1):
        print(f"{index}. {book['title']} | Category : {book['category']}")
        print("-" * 30)

    choice_book = input("Choose book: ")

    if choice_book.isdigit() and 1 <= int(choice_book) <= len(choosen_category):
        selected_book = choosen_category[int(choice_book) - 1]

        print(f"\n{'-' * 30}"
            f"\n\t{selected_book['uid']} \n"
            f"--> Title : {selected_book['title']} \n"
            f"--> Author : {selected_book['author']} | "
            f"Category : {selected_book['category']}\n"
            f"--> Read Count : {selected_book['read_count']}\n"
            f"--> Favourite : {selected_book['favourite_count']}\n"
            f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
            f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
            f"{'-' * 30}\n"
            )

        book_actions(selected_book, current_user)

    else:
        print("--- Incorrect Choice of Books ---\n")



# =========================
# Search Engine
# =========================


def search(current_user):

    loading_books = load_books()

    search_by = ['Title', 'Author' , 'Category']

    while True:

        for index , action in enumerate(search_by, start=1):
            print(f"{index}. {action}")
        print("")
        choice = input("Choose Filter: ")
        print("")

# ----------------------------------------------------------------------------------------------------
# Search By Title:-
# ----------------------------------------------------------------------------------------------------
        if choice == "1":
            title = input('Title : ')
            
            search_result = []
            found = False
            for book in loading_books:
                if title.lower() in book['title'].lower():
                    search_result.append(book)
                    found = True
                
            for index , selected_book in enumerate(search_result, start=1):
                print(f"\n{'-' * 30}"
                    f"\n{index}.{selected_book['uid']} \n"
                    f"--> Title : {selected_book['title']} \n"
                    f"--> Author : {selected_book['author']} | "
                    f"Category : {selected_book['category']}\n"
                    f"--> Read Count : {selected_book['read_count']}\n"
                    f"--> Favourite : {selected_book['favourite_count']}\n"
                    f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
                    f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
                    f"{'-' * 30}\n"
                    )


                
            choice = input("Choose from the list: ")

            if choice.isdigit() and 1 <= int(choice) <= len(search_result):
                selected_book = search_result[int(choice) - 1]
                book_actions(selected_book , current_user)

            
            else:
                print('\n\t Search \t\n')



            if not found:
                print(f"{'-'*30}\nBook Not Found\n")
                    

# ----------------------------------------------------------------------------------------------------
# Search By Author:-
# ----------------------------------------------------------------------------------------------------


        elif choice == "2":
            author = input('Author : ')
            
            search_result = []
            found = False
            for index , selected_book in enumerate(loading_books , start=1):
                if author.lower() in selected_book['author'].lower():
                    search_result.append(selected_book)
                    found = True
                
                    print(f"\n{'-' * 30}"
                        f"\n{index}.{selected_book['uid']} \n"
                        f"--> Title : {selected_book['title']} \n"
                        f"--> Author : {selected_book['author']} | "
                        f"Category : {selected_book['category']}\n"
                        f"--> Read Count : {selected_book['read_count']}\n"
                        f"--> Favourite : {selected_book['favourite_count']}\n"
                        f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
                        f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
                        f"{'-' * 30}\n"
                        )


            if not found:
                print(f"{'-'*30}\nBook Not Found\n")
                return

            choice = input("Choose from the list: ")

            if choice.isdigit() and 1 <= int(choice) <= len(search_result):
                selected_book = search_result[int(choice) - 1]
                book_actions(selected_book , current_user)

            
            else:
                print('\n\t Search \t\n')



                    

# ----------------------------------------------------------------------------------------------------
# Search By Category:-
# ----------------------------------------------------------------------------------------------------


        elif choice == "3":
            category = input('category : ')
            
            search_result = []
            found = False
            for book in loading_books:
                if category.lower() in book['category'].lower():
                    search_result.append(book)
                    found = True
                
            for index , selected_book in enumerate(search_result, start=1):
                print(f"\n{'-' * 30}"
                        f"\n{index}.{selected_book['uid']} \n"
                        f"--> Title : {selected_book['title']} \n"
                        f"--> Author : {selected_book['author']} | "
                        f"Category : {selected_book['category']}\n"
                        f"--> Read Count : {selected_book['read_count']}\n"
                        f"--> Favourite : {selected_book['favourite_count']}\n"
                        f"--> Ratings : {selected_book['ratings']['average_rating']}\n"
                        f"--> Ratings Given by : {selected_book['ratings']['users_count']}\n"
                        f"{'-' * 30}\n"
                        )
                
            if not found:
                print(f"{'-'*30}\nBook Not Found\n")
                return None
            choice = input("Choose from the list: ")

            if choice.isdigit() and 1 <= int(choice) <= len(search_result):
                selected_book = search_result[int(choice) - 1]
                book_actions(selected_book , current_user)

            
            else:
                print('\n\t Search \t\n')




# ----------------------------------------------------------------------------------------------------
        elif choice == "4":
            print('\n==> Back To Menu <==\n')
            break

        else:
            print("\n== Invalid Choice ==\n")




# =========================
# User Panel
# =========================


def user_panel(logged_in_user):

    actions = [
        'Home Page',
        'Tending Page',
        'Category Search',
        'LogOut',
        'Search'
    ]

    print("\n\t===> WELCOME BACK <===\n")

    while True:

        print("\n===>USER PANEL<===\n")

        for i, d in enumerate(actions, start=1):
            print(f"{i}. {d}")

        print("")

        choice = input('Choose: ').strip()

        print("")

        if choice == "1":
            home_page(logged_in_user)

        elif choice == "2":
            show_trending_books(logged_in_user)

        elif choice == "3":
            category_search(logged_in_user)

        elif choice == "4":
            print("\n---Logging Out---\n")
            break

        elif choice == "5":
            search(logged_in_user)

        else:
            print("\n---Invalid Choice---\n")


    



if __name__ == "__main__":
    user_panel(None)

