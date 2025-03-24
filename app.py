import streamlit as st
from utils.video_generator import generate_greeting_video
import os

st.set_page_config(page_title="Eid Greeting Video Generator")
st.title("🎉 Eid Greeting Video Generator")

name = st.text_input("Enter your name:")
if st.button("Generate Greeting Video") and name:
    st.info("Generating your video...")
    output_path = generate_greeting_video(
        name=name,
        background_path="assets/eid-background.mp4",
        font_path="fonts/NotoSansArabic-SemiBold.ttf",
    )

    st.success("✅ Your video is ready!")
    st.video(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 Download Video", data=f, file_name=f"eid_greeting_{name}.mp4")
