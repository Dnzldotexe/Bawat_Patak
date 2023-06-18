"""
This module is the main application 
"""
import datetime
import streamlit as st
import streamlit_authenticator as stauth
from modules import database as db

def greet() -> str:
    """
    Greeting the user 
    """
    current_time = datetime.datetime.now()

    if current_time.hour < 12:
        return "Good Morning, "

    if 12 <= current_time.hour < 18:
        return "Good Afternoon, "

    return "Good Evening, "


# Setting title page
st.set_page_config(page_title="Bawat Patak", page_icon=":droplet:")


# Fetching all the users
users = db.fetch_all_users()

def to_list() -> list[str]:
    """
    Converting fetched data into list independent of each other
    """
    list_usernames = [user['usernames'] for user in users.data]
    list_names = [user['names'] for user in users.data]
    list_emails = [user['emails'] for user in users.data]
    list_hashed_passwords = [user['hashed_passwords'] for user in users.data]

    return list_usernames, list_names, list_emails, list_hashed_passwords

def create_config() -> dict(str):
    """
    Combining all user data into a credentials dictionary
    """
    usernames, names, emails, passwords = to_list()

    credentials = {"usernames":{}}
    for username, name, email, password in zip(usernames, names, emails, passwords):
        user_dict = {"email": email, "name":name,"password":password}
        credentials["usernames"].update({username:user_dict})

    return credentials


def main():
    """
    Contains the functions of the application
    """
    authenticator = stauth.Authenticate(create_config(),
        "logs_cookie", "cookie_key_abcd", 14)

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status is False:
        st.error("Username/Password is incorrect")

    if authentication_status is None:
        st.warning("Please enter your username and password")

    if authentication_status is True:
        st.success(f"Welcome *{username}*")
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")
        st.title("📊 Your Dashboard")
        st.write("Some Dashboard")

        st.title("📄 Your Logs ✍")
        st.write("This is a placeholder.")


if __name__ == "__main__":
    main()
