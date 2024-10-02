import os
import streamlit as st

def get_google_api_key():
    """Retrieve the Google API key from Streamlit secrets or environment variables."""
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        os.environ["GOOGLE_API_KEY"] = api_key
        return api_key
    except KeyError:
        st.error("API key not found. Please provide the key in Streamlit secrets or `.env` file.")
        return None
