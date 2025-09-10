import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mood Diary Chat", page_icon="📝", layout="centered")
st.title("Mood Diary Chat")
st.write("Share your thoughts and moods. I'll respond like a supportive companion!")

# -----------------------------
# Persistent storage per user
# -----------------------------
DATA_FILE = "user_history.json"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Load previous history if file exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            st.session_state.messages = data.get("messages",_
