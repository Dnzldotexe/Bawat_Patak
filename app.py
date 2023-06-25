"""
This module contains the main application 
"""
import datetime as dt
import pytz as tz
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from modules import database as db


# Setting page title and icon
st.set_page_config(page_title="Bawat Patak", page_icon=":droplet:")


def greet(name: str) -> str:
    """
    Greeting the user
    """

    # Setting timezone to Manila
    manila = tz.timezone("Asia/Manila")
    current_time = dt.datetime.now(manila)

    # Getting the user's first name
    first_name = name.split(" ")[0].title()

    # Good morning
    if current_time.hour < 12:
        return f"Good morning, {first_name}!"

    # Good afternoon
    if 12 <= current_time.hour < 18:
        return f"Good afternoon, {first_name}!"

    # Good evening
    return f"Good evening, {first_name}!"


def aggregate_credentials():
    """
    Combining all user data into a credentials dictionary

    Returns:
        dict()
    """

    # Fetching all user data
    users = db.fetch_all_users()

    # Converting fetched data into list independent of each other
    usernames = [user["usernames"] for user in users.data]
    names = [user["names"] for user in users.data]
    emails = [user["emails"] for user in users.data]
    passwords = [user["passwords"] for user in users.data]

    # Aggregated credentials dictionary
    credentials = {"usernames":{}}
    for username, name, email, password in zip(usernames, names, emails, passwords):
        user_dict = {"email": email, "name":name,"password":password}
        credentials["usernames"].update({username:user_dict})

    # Returning dictionary
    return credentials


def main() -> None:
    """
    Contains the functions of the application
    """

    # Authenticating credentials
    authenticator = stauth.Authenticate(aggregate_credentials(),
        "bawat-patak_cookie", "cookie_key_abcde", 14)

    # Log in UI
    name, authentication_status, username = authenticator.login("Log In", "main")

    # Checking session state/cookie
    # When wrong input
    if st.session_state["authentication_status"] is False:
        st.error("Username/Password is incorrect")

    # When no input
    if st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

    # Sign up UI
    if not st.session_state["authentication_status"]:
        try:
            if authenticator.register_user("Sign Up", preauthorization=False):
                st.success("User registered successfully")

                # Getting credentials of the new user
                new_user = authenticator.credentials
                new_user = {key.lower(): value for key, value in list(new_user["usernames"].items())[-1:]}

                # Assigning to each variables
                username = list(new_user.keys())[0]
                name = new_user[username]["name"]
                email = new_user[username]["email"]
                password = new_user[username]["password"]

                # Inserting new user to the database
                db.insert_user(username, name, email, password)
                db.fetch_all_users()

        # Raising exception/s
        except Exception as error:
            st.error(error)

    # Main app if logged in
    if st.session_state["authentication_status"]:

        # Side bar log out button
        authenticator.logout("Logout", "sidebar", key="unique_key")

        # Greeting the user
        st.sidebar.title(f"{greet(name)}")

        # Side bar multipage options
        with st.sidebar:
            selected = option_menu(
                menu_title=None,
                options=["Dashboard", "About"],
                icons=["graph-up", "book"],
            )

        # About page
        if selected == "About":

            # Definition
            st.title("📚 About Bawat Patak:")
            st.subheader("Bawat Patak [project definition here]")
            st.divider()

            # SDGs and Institutions
            st.subheader("[💡 Sustainable Development Goal 6](https://sdgs.un.org/goals/goal6)")
            st.subheader("[🌏 UN Water](https://www.unwater.org/about-un-water)")
            st.divider()

            # GitHub repo
            st.subheader("[🤖 GitHub Repository](https://github.com/Dnzldotexe/Bawat_Patak)")

        # Dashboard and Logs page
        if selected == "Dashboard":

            # Dashboard
            st.title("📊 Your Dashboard 🌊")
            st.write("Some Dashboard here")
            st.divider()

            # Logs
            st.title("📄 Your Logs ✍")

            # Consumption Form
            with st.form("Consumption Form"):
                col1, col2 = st.columns(2)

                # Column 1
                with col1:
                    date = st.date_input(
                        "Reading Date",
                        dt.date.today(),
                    )
                    date_string = date.isoformat()

                # Column 2
                with col2:
                    consumption = st.number_input(
                        "Consumption per Cubic Meters",
                        value = 0
                    )

                # Submit button
                submitted = st.form_submit_button("Submit")
                if submitted:
                    # Store user log into the database
                    db.insert_logs(username, date_string, consumption)
                    st.success("Log added successfully")

            # Consumption Table
            logs, count = db.fetch_logs(username)
            dataframe = pd.DataFrame(logs[1])
            st.table(dataframe[["date", "consumption"]])


# Running main
if __name__ == "__main__":
    main()
