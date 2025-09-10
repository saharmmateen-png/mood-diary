import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date
import json
import os

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="Mood Diary Chat", page_icon="📝", layout="centered")
st.title("Mood Diary Chat")
st.write("Share your thoughts and moods. I'll respond like a supportive companion!")

# -----------------------------
# Files for storage
# -----------------------------
DATA_FILE = "user_history.json"    # chat messages per user (private)
CSV_FILE = "mood_log.csv"          # structured mood history

# -----------------------------
# Load or create CSV mood log
# -----------------------------
try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=["Date", "Mood", "Notes"])

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
# Mood input
# -----------------------------
moods = ["😊 Happy", "😐 Neutral", "😔 Sad", "😰 Anxious", "😡 Angry"]
user_mood = st.selectbox("How are you feeling today?", moods)
notes = st.text_area("Write about your day or your thoughts:")

if st.button("Send"):
    today_str = date.today().strftime("%Y-%m-%d")
    
    # Save to CSV
    new_entry = pd.DataFrame({'Date':[today_str], 'Mood':[user_mood], 'Notes':[notes]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    # Save chat message
    st.session_state.messages.append({
        "role": "user",
        "content": notes,
        "mood": user_mood,
        "timestamp": datetime.now().isoformat()
    })
    
    # -----------------------------
    # Adaptive AI response
    # -----------------------------
    if user_mood in ["😔 Sad", "😰 Anxious", "😡 Angry"]:
        response = "I hear you. It's okay to feel this way. Can you tell me more about it?"
    elif user_mood == "😊 Happy":
        response = "That's great to hear! What made you feel happy today?"
    else:
        response = f"I notice you are feeling {user_mood}. Can you share more about it?"
    
    st.session_state.messages.append({
        "role": "ai",
        "content": response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Save messages to JSON
    with open(DATA_FILE, "w") as f:
        json.dump({"messages": st.session_state.messages}, f, indent=2)
    
    st.success("Your entry has been recorded!")

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
# Display mood history and chart
# -----------------------------
if not df.empty:
    st.subheader("Mood History")
    st.dataframe(df.sort_values("Date", ascending=False))
    
    mood_count = df['Mood'].value_counts().reset_index()
    mood_count.columns = ['Mood','Count']
    fig_pie = px.pie(mood_count, names='Mood', values='Count', title="Mood Distribution")
    st.plotly_chart(fig_pie)
