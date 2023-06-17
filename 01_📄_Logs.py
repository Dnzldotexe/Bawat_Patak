import streamlit as st
import streamlit_authenticator as stauth
from modules.formatter import Title
from modules import database as db

# Title page
Title()

users = db.fetch_all_users()

list_usernames = [user['usernames'] for user in users.data]
list_names = [user['names'] for user in users.data]
list_hashed_passwords = [user['passwords'] for user in users.data]

authenticator = stauth.Authenticate(list_names, list_usernames, list_hashed_passwords,
    "logs_cookie", "cookie_key_abcd", 14)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.title(f"📊 Your Dashboard")
    st.write("Some Dashboard")

    st.title("📄 Your Logs ✍")
    st.write("This is a placeholder. I'm checking if changes reflects immediately to streamlit.")

elif authentication_status is False:
    st.error("Username/Password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")
