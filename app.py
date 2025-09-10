import streamlit as st
from datetime import datetime
import pandas as pd
import random
import time

st.set_page_config(page_title="LatnemAI Chat", page_icon="🤖", layout="wide")
st.title("LatnemAI Chat")
st.write("Chat with LatnemAI. Your messages are remembered only while this tab is open. It responds in Gen Z / Gen Alpha style!")

# -----------------------------
# Initialize session memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Optional CSV for mood trends
# -----------------------------
CSV_FILE = "mood_log.csv"
try:
    df = pd.read_csv(CSV_FILE)
except:
    df = pd.DataFrame(columns=["Date","Mood","Notes"])

# -----------------------------
# Define Gen Z / Gen Alpha adaptive responses
# -----------------------------
response_dict = {
    "sad": [
        "ahh nooo 😢 that sucks fr… wanna vent?",
        "yikes… I feel you. spill the tea ☕",
        "lowkey sad vibes, but I’m here 💜"
    ],
    "angry": [
        "fr fr that’s mad annoying 😡",
        "yikes… wanna rant? I got you",
        "ugh I feel you 😤 take a sec to breathe tho"
    ],
    "anxious": [
        "aww that’s stressful fr 😰 deep breaths",
        "lowkey worried vibes… what’s on your mind?",
        "fr fr I get it, this stuff sucks 😓"
    ],
    "happy": [
        "yasss!!! that’s hype 😎 tell me more",
        "omg fr fr happy vibes only ✨",
        "woohoo 🥳 love that for you!"
    ],
    "excited": [
        "omg hypeee 😆 spill what’s going on!",
        "yasss fr fr can’t wait to hear more 😎",
        "woohoo 🥳 tell me everything!"
    ],
    "lonely": [
        "aww 💜 you’re not alone, I got you",
        "lowkey lonely vibes… I’m here 😔",
        "spill the tea ☕, I’m listening"
    ],
    "confused": [
        "hmm 🤔 that’s tricky… can you clarify?",
        "lowkey confused too 😕 explain a bit more?",
        "fr fr I feel you, what’s confusing exactly?"
    ],
    "bored": [
        "meh… I feel that fr 😅 wanna chat?",
        "lowkey bored too 😐 any ideas?",
        "fr fr boredom sucks, spill something fun"
    ],
    "grateful": [
        "aww that’s wholesome 😭💖",
        "fr fr gratitude vibes, I feel that",
        "that’s cute af, tell me more 🙏"
    ],
    "neutral": [
        "meh… I feel that fr",
        "same here… wanna chat or nah?",
        "lowkey chill vibes 😎"
    ]
}

emoji_mood_map = {
    "😢": "sad",
    "😡": "angry",
    "😰": "anxious",
    "😊": "happy",
    "😐": "neutral",
    "😄": "excited",
    "😔": "lonely",
    "😕": "confused",
    "😴": "bored",
    "🙏": "grateful"
}

# -----------------------------
# Mood detection from text + emoji
# -----------------------------
def detect_mood(text):
    text_lower = text.lower()
    for emoji, mood in emoji_mood_map.items():
        if emoji in text:
            return mood
    if any(word in text_lower for word in ["sad", "depressed", "unhappy", "down"]):
        return "sad"
    elif any(word in text_lower for word in ["angry", "mad", "frustrated", "annoyed"]):
        return "angry"
    elif any(word in text_lower for word in ["anxious", "nervous", "worried", "stressed"]):
        return "anxious"
    elif any(word in text_lower for word in ["happy", "good", "great", "joy"]):
        return "happy"
    elif any(word in text_lower for word in ["excited", "hype"]):
        return "excited"
    elif any(word in text_lower for word in ["lonely", "alone"]):
        return "lonely"
    elif any(word in text_lower for word in ["confused", "lost", "unsure"]):
        return "confused"
    elif any(word in text_lower for word in ["bored", "unmotivated", "tired"]):
        return "bored"
    elif any(word in text_lower for word in ["grateful", "thankful"]):
        return "grateful"
    else:
        return "neutral"

# -----------------------------
# User input
# -----------------------------
user_input = st.text_input("Type your message here:")

if st.button("Send") and user_input:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Detect mood
    mood = detect_mood(user_input)
    
    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "mood": mood,
        "timestamp": timestamp
    })
    
    # Save to CSV for trends (optional)
    new_entry = pd.DataFrame({'Date':[timestamp], 'Mood':[mood], 'Notes':[user_input]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    # Simulate LatnemAI typing
    st.session_state.messages.append({"role": "ai", "content": "LatnemAI is typing...", "timestamp": timestamp})
    time.sleep(random.uniform(0.8, 1.5))
    st.session_state.messages.pop()
    
    # Generate adaptive Gen Z response
    ai_response = random.choice(response_dict[mood])
    
    # Reference up to 2 previous user messages if negative mood
    if mood in ["sad", "angry", "anxious", "lonely", "confused"]:
        previous_msgs = [m["content"] for m in st.session_state.messages if m["role"]=="user"]
        if len(previous_msgs) > 1:
            ai_response += f" btw, you said before: '{previous_msgs[-2]}'… wanna tell me more?"

    st.session_state.messages.append({
        "role": "ai",
        "content": ai_response,
        "timestamp": timestamp
    })

# -----------------------------
# Display chat in scrollable Gen Z style bubbles
# -----------------------------
st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0px;
    text-align: right;
}
.ai-msg {
    background-color: #E6E6FA;
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0px;
    text-align: left;
}
.chat-container {
    max-height: 500px;
    overflow-y: auto;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 12px;
    background-color: #f9f9f9;
}
.timestamp {
    font-size: 0.7em;
    color: gray;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    time_label = msg["timestamp"].split()[1]  # HH:MM:SS
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>You ({msg["mood"]}):</b> {msg["content"]} <div class="timestamp">{time_label}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg"><b>LatnemAI:</b> {msg["content"]} <div class="timestamp">{time_label}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Mood chart (optional)
# -----------------------------
if not df.empty:
    st.subheader("Mood History")
    st.dataframe(df.sort_values("Date", ascending=False))
    mood_count = df['Mood'].value_counts().reset_index()
    mood_count.columns = ['Mood','Count']
    st.bar_chart(mood_count.set_index('Mood')['Count'])
