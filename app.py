import streamlit as st
from utils.video_generator import generate_greeting_video
import tempfile
import os

# Page config
st.set_page_config(page_title="🎥 Eid Greeting Generator", layout="centered")

# UI
st.title("🎉 Eid Greeting Video Generator")

name = st.text_input("Employee Name")
position = st.text_input("Employee Position")
generate = st.button("Generate Greeting Video")

if generate and name and position:
    with st.spinner("Generating video..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
            output_path = tmpfile.name
            generate_greeting_video(
                name="عيد سعيد 🎉",
                output_path="greeting.mp4",
                font_path="fonts/NotoSansArabic-SemiBold.ttf",
                video_path="assets/eid-background.mp4"
            )

            st.success("✅ Video generated successfully!")
            st.video(output_path)
