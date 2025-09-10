import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, date

# ----------------------------
# Load or create mood log
# ----------------------------
try:
    df = pd.read_csv("mood_log.csv")
except:
    df = pd.DataFrame(columns=["Date","Mood","Notes"])

# ----------------------------
# Mood options
# ----------------------------
moods = ['Happy', 'Sad', 'Anxious', 'Calm', 'Angry']

st.title("Mood Tracker App")

user_mood = st.selectbox("How are you feeling today?", moods)
notes = st.text_area("Write about your day")

if st.button("Submit"):
    today_str = date.today().strftime("%Y-%m-%d")
    new_entry = pd.DataFrame({'Date':[today_str], 'Mood':[user_mood], 'Notes':[notes]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv("mood_log.csv", index=False)
    st.success("Mood saved!")

# ----------------------------
# Show mood history
# ----------------------------
if not df.empty:
    st.subheader("Mood History")
    st.dataframe(df.sort_values('Date', ascending=False))

    mood_count = df['Mood'].value_counts().reset_index()
    mood_count.columns = ['Mood','Count']
    fig_pie = px.pie(mood_count, names='Mood', values='Count', title="Mood Distribution")
    st.plotly_chart(fig_pie)
