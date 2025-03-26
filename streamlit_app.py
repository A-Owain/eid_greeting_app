import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import os
import uuid

# Page config
st.set_page_config(page_title="Eid Greeting Video Generator", layout="centered")
st.title("Eid Greeting Video Generator")
st.markdown("""
<style>
    .stApp {
        background-color: #f7f7f7;
        font-family: 'Segoe UI', sans-serif;
    }
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .stDownloadButton>button {
        background-color: #1a73e8;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.6em 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# Form Inputs
name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

# Run on button click
if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter a name.")
        st.stop()

    # Reshape Arabic
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    bidi_position = ""
    if position.strip():
        reshaped_pos = arabic_reshaper.reshape(position)
        bidi_position = get_display(reshaped_pos)

    # Load video
    VIDEO_PATH = "eid-background.mp4"
    FONT_PATH = "IBMPlexSansArabic-Bold.ttf"
    OUTPUT_FILE = f"output_{uuid.uuid4().hex[:8]}.mp4"

    clip = VideoFileClip(VIDEO_PATH, audio=False)

    # Name clip
    name_clip = (
        TextClip(bidi_name, font=FONT_PATH, fontsize=90, color='red', method='label')
        .set_duration(clip.duration - 1.46)
        .set_start(1.46)
        .crossfadein(1.5)
        .set_position(("center", clip.h * 0.78))
    )

    clips = [clip, name_clip]

    if bidi_position:
        pos_clip = (
            TextClip(bidi_position, font=FONT_PATH, fontsize=60, color='red', method='label')
            .set_duration(clip.duration - 1.60)
            .set_start(1.60)
            .crossfadein(1.5)
            .set_position(("center", clip.h * 0.83))
        )
        clips.append(pos_clip)

    final = CompositeVideoClip(clips).set_duration(clip.duration)
    final.write_videofile(OUTPUT_FILE, codec='libx264')

    # Serve for download
    with open(OUTPUT_FILE, "rb") as file:
        st.download_button(
            label="Download Your Greeting Video",
            data=file,
            file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
            mime="video/mp4"
        )

    os.remove(OUTPUT_FILE)
