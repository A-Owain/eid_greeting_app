import streamlit as st
import requests
import time
import os

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

API_URL = "https://eid-video-api.onrender.com/generate-video"

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter a name.")
        st.stop()

    with st.spinner("Waking up the video server..."):
        time.sleep(1.5)

    try:
        response = requests.post(API_URL, json={"name": name, "position": position})

        if response.status_code == 200:
            video_url = response.json().get("video_url")
            if video_url:
                st.video(video_url)
                st.markdown(f"""
                <a href="{video_url}" download>
                    <button style="margin-top: 20px; padding: 0.6em 1.2em; background-color: #1a73e8; color: white; border: none; border-radius: 8px; font-size: 16px;">Download Video</button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.error("Video URL not found in response.")
        else:
            st.error(f"API error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")
