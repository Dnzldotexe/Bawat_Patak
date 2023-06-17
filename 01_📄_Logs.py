import streamlit as st
import streamlit_authenticator as stauth
from modules.formatter import Title
from modules import database as db

# Title page
Title()

users = db.fetch_all_users()

usernames = {"usernames":user['usernames'] for user in users.data}
names = {"names":user['names'] for user in users.data}
hashed_passwords = {"passwords":user['passwords'] for user in users.data}

i=0
while i < len(usernames):
    st.write(usernames)
    st.write(names)
    st.write(hashed_passwords)
    i+=1

# authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
#     "logs_cookie", "abcd", 14)

# name, authentication_status, username = authenticator.login('Login', 'main')

# if authentication_status is False:
#     st.error("Username/password is incorrect")

# if authentication_status is None:
#     st.warning("Please enter your username and password")

# if authentication_status:
#     st.title("📊 {name}'s Dashboard")
#     st.write("Some Dashboard")

#     st.title("📄 Your Logs ✍")
#     st.write("This is a placeholder. I'm checking if changes reflects immediately to streamlit.")