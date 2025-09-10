import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

st.set_page_config(page_title="Mood Diary Chat", page_icon="📝", layout="centered")
st.title("Mood Diary Chat")
st.write("Chat with your personal mood companion. Type freely and get responses!")

# -----------------------------
# Files for storage
# -----------------------------
DATA_FILE = "user_history.json"  # chat messages per user
CSV_FILE = "mood_log.csv"        # structured mood history

# -----------------------------
# Load or create CSV mood log
# -----------------------------
try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=["Date","Mood","Notes"])

# -----------------------------
# Initialize session state for chat
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Load previous chat history if exists
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
            st.session_state.messages = data.get("messages", [])
        except:
            st.session_state.messages = []

# -----------------------------
# User chat input
# -----------------------------
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input:
    # Record timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # -----------------------------
    # Optional: basic mood detection
    # -----------------------------
    text_lower = user_input.lower()
    if any(word in text_lower for word in ["happy", "good", "great", "excited"]):
        mood = "😊 Happy"
    elif any(word in text_lower for word in ["sad", "depressed", "unhappy"]):
        mood = "😔 Sad"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated"]):
        mood = "😡 Angry"
    elif any(word in text_lower for word in ["anxious", "nervous", "worried"]):
        mood = "😰 Anxious"
    else:
        mood = "😐 Neutral"

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "mood": mood,
        "timestamp": timestamp
    })

    # Save to CSV for mood tracking
    new_entry = pd.DataFrame({'Date':[timestamp], 'Mood':[mood], 'Notes':[user_input]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    # -----------------------------
    # AI response (adaptive)
    # -----------------------------
    if mood in ["😔 Sad", "😰 Anxious", "😡 Angry"]:
        response = "I hear you. It's okay to feel this way. Can you tell me more about it?"
    elif mood == "😊 Happy":
        response = "That's wonderful! What made you feel this way?"
    else:
        response = "Thanks for sharing. How else are you feeling today?"

    st.session_state.messages.append({
        "role": "ai",
        "content": response,
        "timestamp": timestamp
    })

    # Save chat history
    with open(DATA_FILE, "w") as f:
        json.dump({"messages": st.session_state.messages}, f, indent=2)

# -----------------------------
# Display chat messages
# -----------------------------
st.write("### Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"**You ({msg['mood']}):** {msg['content']}")
    else:
        st.markdown(f"**AI:** {msg['content']}")

# -----------------------------
# Display mood chart
# -----------------------------
if not df.empty:
    st.subheader("Mood History")
    st.dataframe(df.sort_values("Date", ascending=False))
    mood_count = df['Mood'].value_counts().reset_index()
    mood_count.columns = ['Mood','Count']
    st.bar_chart(mood_count.set_index('Mood')['Count'])
