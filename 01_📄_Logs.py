import streamlit as st
import streamlit_authenticator as stauth
from modules.formatter import Title
from modules import database as db

# Title page
Title()

users = db.fetch_all_users()

def generate_credentials():
    list_usernames = [user['usernames'] for user in users.data]
    list_names = [user['names'] for user in users.data]
    list_hashed_passwords = [user['passwords'] for user in users.data]

    user_values = []
    for username, name, password in zip(list_usernames, list_names, list_hashed_passwords):
        user_values.append({'username': username, 'name': name, 'password': password})

    credentials = {'usernames': {}}
    for username, users.data in zip(list_usernames, user_values):
        credentials['usernames'][username] = users.data

    return {'credentials': credentials}

credentials = generate_credentials()

authenticator = stauth.Authenticate(credentials,
    "logs_cookie", "cookie_key_abcd", 14)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status is False:
    st.error("Username/password is incorrect")

if authentication_status is None:
    st.warning("Please enter your username and password")

if authentication_status:
    st.title("📊 {name}'s Dashboard")
    st.write("Some Dashboard")

    st.title("📄 Your Logs ✍")
    st.write("This is a placeholder. I'm checking if changes reflects immediately to streamlit.")