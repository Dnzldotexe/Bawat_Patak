"""
This module is the main application 
"""
import streamlit as st
import streamlit_authenticator as stauth
from modules import database as db


# Setting title page
icon, title = '💧', 'Bawat Patak'
st.set_page_config(page_title=title, page_icon=icon)


# Fetching all the users
users = db.fetch_all_users()

def to_list() -> list[str]:
    """
    Converting fetched data into list independent of each other
    """
    list_usernames = [user['usernames'] for user in users.data]
    list_names = [user['names'] for user in users.data]
    list_hashed_passwords = [user['hashed_passwords'] for user in users.data]
    list_cookie_names = [user['cookie_names'] for user in users.data]
    list_cookie_keys = [user['cookie_keys'] for user in users.data]

    return list_usernames, list_names, list_hashed_passwords, list_cookie_names, list_cookie_keys
                
def create_config():
    """
    Combining all user data into a dictionary
    """
    list_usernames, list_names, list_passwords, list_cookie_names, list_cookie_keys = to_list()

    user_values = []
    for name, password in zip(list_names, list_passwords):
        user_values.append({'name': name, 'password': password})

    credentials = {'usernames': {}}
    for username, user_data in zip(list_usernames, user_values):
        credentials['usernames'][username] = user_data

    config = {
        'credentials': credentials,
        # 'cookie': dict(zip(list_cookie_names, list_cookie_keys))
    }

    return credentials

def main():
    authenticator = stauth.Authenticate(create_config(),
        "logs_cookie", "cookie_key_abcd", 14)

    name, authentication_status, username = authenticator.login('Login', 'main')

    if authentication_status is False:
        st.error("Username/Password is incorrect")

    if authentication_status is None:
        st.warning("Please enter your username and password")

    if authentication_status:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")
        st.title("📊 Your Dashboard")
        st.write("Some Dashboard")

        st.title("📄 Your Logs ✍")
        st.write("This is a placeholder. I'm checking if changes reflects immediately to streamlit.")


if __name__ == "__main__":
    main()