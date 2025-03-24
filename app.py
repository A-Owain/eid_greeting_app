import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
import os

# === Settings ===
FONT_PATH = "NotoSansArabic-SemiBold.ttf"
VIDEO_PATH = "eid-background.mp4"
OUTPUT_PATH = "output.mp4"

# === Inputs ===
name = st.text_input("Enter name", "Paul Melotto")
position = st.text_input("Enter position", "CEO")

if st.button("Generate Greeting Video"):
    reshaped_name = get_display(arabic_reshaper.reshape(name))
    reshaped_position = get_display(arabic_reshaper.reshape(position))

    clip = VideoFileClip(VIDEO_PATH)

    name_clip = (
        TextClip(reshaped_name, fontsize=90, color="red", font=FONT_PATH)
        .set_start(1.5)
        .set_duration(clip.duration - 1.5)
        .fadein(1.5)
        .set_position(("center", clip.h * 0.78))
    )

    pos_clip = (
        TextClip(reshaped_position, fontsize=60, color="red", font=FONT_PATH)
        .set_start(2.0)
        .set_duration(clip.duration - 2.0)
        .fadein(1.0)
        .set_position(("center", clip.h * 0.83))
    )

    final = CompositeVideoClip([clip, name_clip, pos_clip])
    final = final.set_audio(clip.audio)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
        final.write_videofile(tmpfile.name, codec="libx264", audio_codec="aac")
        st.video(tmpfile.name)
