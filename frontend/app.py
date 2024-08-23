import streamlit as st
import requests

BACKEND_URL = "http://fastapi:8000"

st.title("Welcome to the Basic Streamlit App")

st.write("Hello! This is a basic Streamlit application displaying a sentence.")

st.write("Testing connection to FastAPI...")

try:
    response = requests.get(f"{BACKEND_URL}/test", timeout=60)
    if response.status_code == 200:
        st.success(response.json().get("message"))
    else:
        st.error("Failed to connect to FastAPI. Status code: {}".format(response.status_code))
except Exception as e:
    st.error(f"An error occurred: {e}")
