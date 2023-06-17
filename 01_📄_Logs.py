import streamlit as st
import streamlit_authenticator as stauth
from modules.formatter import Title
from modules import database as db

# Title page
Title()

users = db.fetch_all_users()

def convert_to_dict(data,credentials=[]):
    for user in data:
        user_dict = {
            "usernames": user['usernames'],
            "names": user['names'],
            "passwords": user['passwords']
        }
        credentials.append(user_dict)
    return credentials

credentials = convert_to_dict(users.data)

authenticator = stauth.Authenticate(credentials,
    "logs_cookie", "abcd", 14)

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