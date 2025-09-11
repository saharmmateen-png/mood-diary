import streamlit as st
import random
import time
from datetime import datetime

st.set_page_config(page_title="LatnemAI Chat", page_icon="🤖", layout="wide")
st.title("LatnemAI Chat")
st.write("Your chat is private and only remembered while this tab is open. Talk to me like texting a friend.")

# -----------------------------
# Initialize session memory
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Response libraries
# -----------------------------
basic_responses = {
    "hi": ["heyy 👋", "hey hey 😁", "heyyy ✨"],
    "hello": ["heyy ✨", "hello hello 😄", "heyyy, what’s up?"],
    "how are you": ["I’m vibin’ 😌 u?", "pretty chill rn 😎 wbu?", "I’m good, hru?"],
    "what's up": ["not much, just chillin’ 😏", "same vibes, hbu?", "lowkey just hanging 😎"]
}

keyword_responses = {
    "depressed": ["just goon 🥀💔"],
    "school": ["ugh school drains the soul fr 📚 wanna talk abt it?", "school stress be too real 😮‍💨 how’s it hitting you?"],
    "teacher": ["damn 😔 teachers can be so extra… that must’ve stung", "ugh teachers yelling is the worst fr, I feel you"],
    "exam": ["exams hit diff 😵‍💫 did it go bad?", "ugh tests are brutal fr 📖 how’d it go?"],
    "test": ["tests be draining af 😩 wanna vent?", "ugh I hate tests too… fr fr how was it?"],
    "friend": ["friendship drama sucks the most fr 😓 wanna vent?", "ugh friend probs hit hard 😞 what happened?"],
    "family": ["family stress hits deep 🥀 wanna let it out?", "damn… family stuff can be tough fr 😔"],
    "mom": ["ugh moms be like that sometimes 😬 wanna talk?", "fr fr mom probs can be rough 😔"],
    "dad": ["dad stress can hurt too 😕 wanna vent?", "ugh fr fr dad stuff hits deep 💔"],
    "breakup": ["💔 breakups are brutal fr fr… you’ll heal tho, I got u", "ugh heartbreak sucks 😭 wanna talk it out?"],
    "relationship": ["relationships be messy sometimes 😔 wanna vent?", "ugh fr… love probs hit diff 💔"],
    "lonely": ["feeling alone sucks 🥀 but ur not alone rn, I’m here", "loneliness be heavy ❤️ but I got you"],
    "alone": ["ur not alone rn, I got you ❤️", "lonely vibes suck 🥀 wanna chat more?"],
    "angry": ["damn 😡 that’s tough, wanna rant abt it?", "fr fr being mad drains you… what happened?"],
    "fight": ["fights be exhausting 😤 tell me what went down", "ugh conflict vibes suck 😕 wanna share?"],
    "confused": ["hmm 🤔 that sounds confusing, wanna break it down?", "lowkey tricky 😵‍💫 explain more?"],
    "grateful": ["aww that’s actually wholesome 🥹 love that vibe ❤️", "fr fr gratitude vibes, that’s cute af 🙏"]
}

fallback_responses = [
    "fr fr I feel you 😔 tell me more",
    "that’s rough… wanna explain a bit? ❤️",
    "lowkey heavy vibes, I’m here to listen 🥀",
    "ugh I get you… wanna vent more?"
]

# -----------------------------
# Detect response logic
# -----------------------------
def get_ai_response(user_input):
    text_lower = user_input.lower()
    if "depressed" in text_lower:
        return "just goon 🥀💔"
    for key in basic_responses:
        if key in text_lower:
            return random.choice(basic_responses[key])
    for key in keyword_responses:
        if key in text_lower:
            return random.choice(keyword_responses[key])
    return random.choice(fallback_responses)

# -----------------------------
# CSS for chat bubbles
# -----------------------------
st.markdown("""
<style>
.user-msg {
    background-color: #a3d9a5;
    color: #000;
    padding: 12px;
    border-radius: 12px;
    margin: 5px 0px;
    text-align: right;
}
.ai-msg {
    background-color: #ffd6d6;
    color: #000;
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

chat_placeholder = st.empty()

# -----------------------------
# Display chat
# -----------------------------
def display_chat(scroll=True):
    with chat_placeholder.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(
                    f'<div class="user-msg"><b>You:</b> {msg["content"]} '
                    f'<div class="timestamp">{msg["timestamp"]}</div></div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="ai-msg"><b>LatnemAI:</b> {msg["content"]} '
                    f'<div class="timestamp">{msg["timestamp"]}</div></div>',
                    unsafe_allow_html=True
                )
        st.markdown('</div>', unsafe_allow_html=True)
    if scroll:
        st.markdown("<script>window.scrollTo(0, document.body.scrollHeight);</script>", unsafe_allow_html=True)

display_chat(scroll=False)

# -----------------------------
# Input at bottom
# -----------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Type your message here:", key="input")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.messages.append({"role": "user", "content": user_input, "timestamp": timestamp})

    # Fake typing animation with random delay
    st.session_state.messages.append({"role": "ai", "content": "LatnemAI is typing...", "timestamp": timestamp})
    display_chat()
    time.sleep(random.uniform(0.6, 2.0))  # random typing pause
    st.session_state.messages[-1]["content"] = "..."
    display_chat()
    time.sleep(random.uniform(0.3, 1.5))
    st.session_state.messages.pop()

    # Real AI reply
    ai_response = get_ai_response(user_input)
    st.session_state.messages.append({"role": "ai", "content": ai_response, "timestamp": timestamp})

    display_chat()
