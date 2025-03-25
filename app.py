import streamlit as st
import tempfile
import os
from utils.video_generator import generate_greeting_video

# === Paths ===
FONT_PATH = "fonts/NotoSansArabic-Bold.ttf"
BACKGROUND_PATH = "assets/eid-background.mp4"

# === Verify Assets Exist ===
assert os.path.exists(FONT_PATH), f"Font file not found at {FONT_PATH}"
assert os.path.exists(BACKGROUND_PATH), f"Background video not found at {BACKGROUND_PATH}"

# === Streamlit UI ===
st.set_page_config(page_title="TRAY Eid Greeting Video Generator", layout="centered")
st.title("Eid Greeting Video Maker")

name = st.text_input("Enter Name", value="Paul Melotto")
position = st.text_input("Enter Position", value="CEO")

if st.button("Generate Greeting Video"):
    if not name.strip() or not position.strip():
        st.warning("Please enter both name and position.")
    else:
        with st.spinner("Generating video..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmpfile:
                output_path = tmpfile.name

            generate_greeting_video(
                name=name,
                position=position,
                background_path=BACKGROUND_PATH,
                output_path=output_path,
                font_path=FONT_PATH
            )

            st.success("✅ Done!")
            st.video(output_path)

            with open(output_path, "rb") as f:
                st.download_button("📥 Download Video", f, file_name="eid_greeting.mp4", mime="video/mp4")
