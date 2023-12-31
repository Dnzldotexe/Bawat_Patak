"""
This module handles all the functions for the database
"""
import streamlit as st
from supabase import create_client, Client


# Caching resource
@st.cache_resource

def init_connection() -> Client:
    """
    Initialize connection to supabase
    Uses st.cache_resource to only run once
    """
    # Getting the secret url and key
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

# Assigning client
supabase = init_connection()


# Caching the fetched data every 10 seconds
@st.cache_data(ttl=10)

def fetch_all_users():
    """
    Fetching all user data from the database
    
    Returns:
        List of Dictionaries list[dict(str, str)]
    """
    return supabase.table("users_db").select("*").execute()


def insert_user(
        username: str,
        name: str,
        email: str,
        password: str,
        cookie_name: str="bawat-patak_cookie",
        cookie_key: str="cookie_key_abcde"
        ) -> None:
    """
    Inserts new user to the database
    """
    data, count = supabase.table("users_db").insert({
        "usernames": username, 
        "names": name,
        "emails": email,
        "passwords": password,
        "cookie_names": cookie_name,
        "cookie_keys": cookie_key
        }).execute()


def fetch_logs(usernames: str):
    """
    Fetching specific user logs from the database using a foreign key
    
    Returns:
        List of Dictionaries list[dict(str, str)]
    """
    return supabase.table("logs_db").select("*").eq("usernames", f"{usernames}").execute()


def insert_logs(
        usernames: str,
        date: str,
        consumption: int
        ) -> None:
    """
    Inserts new logs to the database
    """
    data, count = supabase.table("logs_db").insert({
        "usernames": usernames,
        "date": date,
        "consumption": consumption
        }).execute()
