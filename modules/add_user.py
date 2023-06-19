"""
This module will be used to add users to the supabase database
"""
import database as db


def register() -> None:
    """
    User Credentials input validation  and registration to the database
    """

    # Asking for user inputs
    username = input("\nPlease Enter a Username: ").strip()
    while not username:
        username = input("Please Enter a Username: ").strip()

    name = input("Please Enter a Name: ").strip()
    while not name:
        name = input("Please Enter a Name: ").strip()

    email = input("Please Enter an Email: ").strip().lower()
    while not email:
        email = input("Please Enter an Email: ").strip()

    password = input("Please Enter a Password: ").strip()
    while not password:
        password = input("Please Enter a Password: ").strip()

    re_enter_pw = input("Please Enter your Password again: ").strip()
    while re_enter_pw != password:
        print("Incorrect")
        re_enter_pw = input("Please Enter your Password again: ").strip()

    # Passing arguments to insert function
    db.insert_user(username, name, email, password)


# Function call
register()
