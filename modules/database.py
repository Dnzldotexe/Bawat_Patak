import streamlit as st
import streamlit_authenticator as stauth
from supabase import create_client#, Client

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)

supabase = init_connection()

@st.cache_data(ttl=600)
def fetch_all_users():
    return supabase.table("users_db").select("*").execute()

def create_user(username, name, password):
    res = supabase.auth.sign_up({
    "usernames": f'{username}',
    "names": f'{name}',
    "passwords": f'{stauth.Hasher(password).generate()}',
    })
    return res
