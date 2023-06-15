import streamlit as st

class Title(object):
    """"
    Update title of each page
    ⚠️ IMPORTANT: Must call page_config() as first function in script 
    """
    def __init__(self):

        self.title = "Bawat Patak"
        self.icon = "💧"
        st.set_page_config(page_title=self.title, page_icon=self.icon)
