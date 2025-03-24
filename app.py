# app.py
import streamlit as st
from utils.video_generator import generate_greeting_video

st.set_page_config(page_title="🎉 Eid Greeting Video Generator", layout="centered")
st.title("🎉 Eid Greeting Video Generator")

name = st.text_input("Enter your name (in Arabic):")

if st.button("Generate Greeting Video"):
    if name:
        with st.spinner("Generating video..."):
            video_path = generate_greeting_video(name)
            st.success("Done! Here's your greeting video:")
            st.video(video_path)
    else:
        st.warning("Please enter a name.")
