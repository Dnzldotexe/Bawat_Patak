"""
This module contains the main application 
"""
import datetime as dt   # Date and Time module
import pytz as tz       # Timezone module
import pandas as pd     # Data manipulation module
import streamlit as st  # Web app module

# Setting page title and icon
st.set_page_config(page_title="Bawat Patak", page_icon=":droplet:")

import streamlit_authenticator as stauth    # Authentication module
from streamlit_option_menu import option_menu   # Multipage module
import importer as db   # Database module


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


def view_logs(
        username: str,
        table: bool = False
        ):
    """
    Gets the logs of the user

    Returns:
        Table / Dataframe / Empty Dataframe
    """

    # Fetching logs data of the user
    logs, count = db.fetch_logs(username)
    dataframe = pd.DataFrame(logs[1])

    # If dataframe has values
    if not dataframe.empty:
        # Filtering the data shown to the user
        filtered_logs_view = dataframe[["date", "consumption"]]
        filtered_logs_view.columns = ["Date", "Consumption (m^3)"]

        # Descending table view
        if table:
            # New input appears on top
            return st.table(filtered_logs_view.sort_index(ascending=False))

        # Ascending dataframe view
        return filtered_logs_view

    # Return empty dataframe
    return dataframe


def main() -> None:
    """
    Contains the functions of the application
    """

    # Authenticating credentials
    authenticator = stauth.Authenticate(aggregate_credentials(),
        "bawat-patak_cookie", "cookie_key_abcde", 14)

    # Log in UI
    name, authentication_status, username = authenticator.login("Log In", "main")

    # Checking authentication status/browser cookie
    # When wrong input
    if authentication_status is False:
        st.error("Username/Password is incorrect")

    # When no input
    if authentication_status is None:
        st.warning("Please enter your username and password")

    # Sign up UI
    st.divider()
    if not authentication_status:
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
    if authentication_status:

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
            logs = view_logs(username)

            # If dataframe has no values
            if logs.empty:
                st.write("Please add your water consumption data below🔽")

            # If dataframe has values
            if not logs.empty:
                # Replace index with dates
                logs = logs.set_index("Date")
                consumption = logs["Consumption (m^3)"]

                # Line chart UI
                st.line_chart(consumption)

            st.divider()

            # Logs
            st.title("📄 Your Logs ✍")

            # Consumption Form
            with st.form("Consumption Form"):
                col1, col2 = st.columns(2)

                # Calendar input field
                with col1:
                    date = st.date_input(
                        "Date taken",
                        dt.date.today(),
                    )
                    date_string = date.isoformat()

                # Number input field
                with col2:
                    consumption = st.number_input(
                        "Consumption per Cubic Meters",
                        value = 0
                    )

                # Submit button
                submitted = st.form_submit_button("Submit")
                # Input must be greater than zero
                if submitted and consumption > 0:
                    # Store user log/s into the database
                    db.insert_logs(username, date_string, consumption)
                    st.success("Log added successfully")

            # Getting the logs data of the user
            view_logs(username, True)


# Running main
if __name__ == "__main__":
    main()
