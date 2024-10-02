import streamlit as st

def display_feedback(feedback):
    st.subheader("🔍 Detailed Feedback")
    st.write(feedback)

def display_score(score):
    st.subheader("🏆 IELTS Band Score")
    st.write(f"Your estimated band score is: {score}")
