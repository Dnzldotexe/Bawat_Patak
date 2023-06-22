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


def greet(name: str) -> str:
    """
    Greeting the user
    """

    # Setting timezone to Manila
    manila = tz.timezone('Asia/Manila')
    current_time = dt.datetime.now(manila)

    # Getting the user's first name
    first_name = name.split(" ")[0].title()

    if current_time.hour < 12:
        return f"Good morning, {first_name}!"

    if 12 <= current_time.hour < 18:
        return f"Good afternoon, {first_name}!"

    return f"Good evening, {first_name}!"


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

    # Hashing passwords
    hashed_passwords = stauth.Hasher(passwords).generate()

    # Aggregated credentials dictionary
    credentials = {"usernames":{}}
    for username, name, email, password in zip(usernames, names, emails, hashed_passwords):
        user_dict = {"email": email, "name":name,"password":password}
        credentials["usernames"].update({username:user_dict})

    return credentials


def main() -> None:
    """
    Contains the functions of the application
    """
    # Authenticating credentials
    authenticator = stauth.Authenticate(create_config(),
        "logs_cookie", "cookie_key_abcd", 14)

    # Log in UI
    name, authentication_status, username = authenticator.login('Login', 'main')

    # Checking session state/cookie
    if st.session_state["authentication_status"] is False:
        st.error("Username/Password is incorrect")

    if st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "sidebar", key="unique_key")
        st.sidebar.title(f"{greet(name)}")
        st.title("📊 Your Dashboard")
        st.write("Some Dashboard")

        st.title("📄 Your Logs ✍")
        st.write("This is a placeholder.")

    # Registration UI
    try:
        if authenticator.register_user('Register user', preauthorization=False):
            st.success('User registered successfully')
    except Exception as error:
        st.error(error)


# Running main
if __name__ == "__main__":
    main()