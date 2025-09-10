import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(page_title="LatnemAI Chat", page_icon="🤖", layout="wide")
st.title("LatnemAI Chat")
st.write("Chat with LatnemAI. Your messages are remembered only while this tab is open!")

# -----------------------------
# Initialize session memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Gen Z / Gen Alpha adaptive responses
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

basic_responses = {
    "hi": ["Heyyy! 😎", "Yo! How’s it going?", "Hi hi! 😁"],
    "hello": ["Heyy! ✨", "Hello hello! 😄", "Yo! What’s up?"],
    "how are you": ["I’m vibin’ 😎 u?", "Good fr fr, how about you?", "Pretty chill 😌 u?"],
    "what's up": ["Not much, just chillin’ 😏", "Same old, same old 😎 u?", "Vibin’ fr fr, u?"]
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
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Check for basic greetings first
    matched_basic = None
    for key in basic_responses:
        if key in user_input.lower():
            matched_basic = key
            break
    
    # Determine AI response
    if matched_basic:
        ai_response = random.choice(basic_responses[matched_basic])
        mood = detect_mood(user_input)
    else:
        mood = detect_mood(user_input)
        ai_response = random.choice(response_dict[mood])
        # Reference previous user message for context if mood negative
        if mood in ["sad", "angry", "anxious", "lonely", "confused"]:
            prev_user_msgs = [m["content"] for m in st.session_state.messages if m["role"]=="user"]
            if len(prev_user_msgs) > 0:
                ai_response += f" btw, before you said: '{prev_user_msgs[-1]}', wanna tell me more?"
    
    # Save messages in session only
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "mood": mood,
        "timestamp": timestamp
    })
    # Simulate typing
    st.session_state.messages.append({"role": "ai", "content": "LatnemAI is typing...", "timestamp": timestamp})
    time.sleep(random.uniform(0.8, 1.5))
    st.session_state.messages.pop()
    
    st.session_state.messages.append({
        "role": "ai",
        "content": ai_response,
        "timestamp": timestamp
    })

# -----------------------------
# Display chat
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
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg"><b>You ({msg["mood"]}):</b> {msg["content"]} <div class="timestamp">{msg["timestamp"]}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="ai-msg"><b>LatnemAI:</b> {msg["content"]} <div class="timestamp">{msg["timestamp"]}</div></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
