Library Management System
A command-line Library Management System built with Python using JSON for data storage. The project includes separate Admin and User panels with authentication, book management, searching, ratings, favourites, reading history, and a trending books system.

Features
Admin
Register & Login
Add Books
Remove Books
View Books
View Registered Users
Search Users
Generate Random Book Statistics
Update Trending Scores
User
Register & Login
Browse Recently Added Books
Search by Title
Search by Author
Search by Category
Browse Books by Category
Read Books
Add Books to Favourites
Rate Books
Update Previous Ratings
Reading History
Books Read Counter
View Trending Books
Technologies Used
Python
JSON
hashlib
os
random
time
Project Structure
Library-Management-System/
│
├── Auth_System/
	└── __init__.py
	└──  admin_auth.py
	└── user_auth.py
├── main_features/
	└── __init__.py
	└──  admin.py
	└── user.py
├── json_files/
	└── __init__.py
	└──  admin_auth.json
	└── user_auth.json
├── main.py
└── utils.py
How to Run
Clone the repository:

git clone <repository-url>
Move to the project folder:

cd Library-Management-System
Run the project:

python main.py
Note
All project data is stored inside the json_files folder using JSON files.
