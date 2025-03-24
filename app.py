
import streamlit as st
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import arabic_reshaper
from bidi.algorithm import get_display
import tempfile
import os

# === UI Setup ===
st.set_page_config(page_title="🎥 Eid Greeting Video Generator", layout="centered")
st.title("🎉 Eid Greeting Video Generator")

# === User Input ===
name = st.text_input("Enter Your Name | ادخل اسمك", max_chars=30)
position = st.text_input("Position (Optional) | المسمى الوظيفي (اختياري)", max_chars=30)

# === Font Path ===
FONT_PATH = "IBMPlexSansArabic-Bold.ttf"  # Must be in the same folder
VIDEO_PATH = "eid-background.mp4"         # Background video (10s)

if name:
    reshaped_name = arabic_reshaper.reshape(name)
    bidi_name = get_display(reshaped_name)

    bidi_position = ""
    if position.strip():
        reshaped_pos = arabic_reshaper.reshape(position)
        bidi_position = get_display(reshaped_pos)

    # === Load Base Video ===
    base_clip = VideoFileClip(VIDEO_PATH)

    # === Create Name Clip ===
    name_clip = (
        TextClip(bidi_name, font=FONT_PATH, fontsize=90, color="red",
                 method="caption", align="center", size=(base_clip.w, None))
        .set_start(1.5)
        .set_duration(base_clip.duration - 1.5)
        .fadein(1.5)
        .set_position(("center", base_clip.h * 0.78))
    )

    clips = [base_clip, name_clip]

    # === Add Position If Provided ===
    if bidi_position:
        pos_clip = (
            TextClip(bidi_position, font=FONT_PATH, fontsize=60, color="red",
                     method="caption", align="center", size=(base_clip.w, None))
            .set_start(1.7)
            .set_duration(base_clip.duration - 1.7)
            .fadein(1.5)
            .set_position(("center", base_clip.h * 0.83))
        )
        clips.append(pos_clip)

    final = CompositeVideoClip(clips, size=base_clip.size).set_duration(base_clip.duration)

    # === Save to Temp File ===
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
        output_path = tmp_file.name
        final.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            bitrate="5000k",
            threads=4,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )

    # === Show Video and Download ===
    st.video(output_path)
    with open(output_path, "rb") as f:
        st.download_button(
            label="⬇️ Download Your Eid Greeting Video",
            data=f,
            file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
            mime="video/mp4"
        )

    # Clean up temp
    os.unlink(output_path)
