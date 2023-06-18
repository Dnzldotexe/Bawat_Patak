"""
This module handles all the functions for the database
"""
import streamlit as st
import streamlit_authenticator as stauth
from supabase import create_client#, Client


@st.cache_resource
def init_connection():
    """
    Initialize connection.
    Uses st.cache_resource to only run once.
    """
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

# Function call
supabase = init_connection()


# Caching the fetched data
@st.cache_data(ttl=600)
def fetch_all_users():
    """
    Fetching all user data from the database
    """
    return supabase.table("users_db").select("*").execute()

def insert_user(username: str, name: str, password:str, cookie_name="bawat-patak_cookie", cookie_key="abcde"):
    """
    Creates a new user with a hashed password.
    """
    data, count = supabase.table('countries').insert({
        "usernames": username, 
        "names": name,
        "passwords": stauth.Hasher(password).generate(),
        "cookie_names": cookie_name,
        "cookie_key": cookie_key,
        }).execute()
