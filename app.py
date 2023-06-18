"""
This module is the main application 
"""
import datetime as dt
import pytz as tz
import streamlit as st
import streamlit_authenticator as stauth
from modules import database as db


# Setting title page
st.set_page_config(page_title="Bawat Patak", page_icon=":droplet:")


def greet() -> str:
    """
    Greeting the user 
    """
    manila = tz.timezone('Asia/Manila')
    current_time = dt.datetime.now(manila)

    if current_time.hour < 12:
        return "Good morning,"

    if 12 <= current_time.hour < 18:
        return "Good afternoon,"

    return "Good evening,"


def create_config():
    """
    Combining all user data into a credentials dictionary

    Returns:
        dict()
    """

    # Fetching all user data
    users = db.fetch_all_users()

    # Converting fetched data into list independent of each other
    usernames = [user['usernames'] for user in users.data]
    names = [user['names'] for user in users.data]
    emails = [user['emails'] for user in users.data]
    passwords = [user['passwords'] for user in users.data]

    # hashing passwords
    hashed_passwords = stauth.Hasher(passwords).generate()

    credentials = {"usernames":{}}
    for username, name, email, password in zip(usernames, names, emails, hashed_passwords):
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

    if st.session_state["authentication_status"] is False:
        st.error("Username/Password is incorrect")

    if st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "sidebar", key="unique_key")
        st.sidebar.title(f"{greet()} {name.title()}!")
        st.title("📊 Your Dashboard")
        st.write("Some Dashboard")

        st.title("📄 Your Logs ✍")
        st.write("This is a placeholder.")


if __name__ == "__main__":
    main()
