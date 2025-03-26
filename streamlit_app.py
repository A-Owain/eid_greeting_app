import streamlit as st
import requests
import time

API_URL = "https://eid-video-api.onrender.com/generate-video"

st.set_page_config(page_title="Eid Greeting Video Generator", layout="centered")
st.title("Eid Greeting Video Generator")

st.markdown("""
<style>
    .stApp {
        background-color: #f9f9f9;
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
    .stButton>button {
        background-color: #d93025;
        color: white;
        border-radius: 6px;
        padding: 0.6em 1.2em;
    }
</style>
""", unsafe_allow_html=True)

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter a name.")
        st.stop()

    status = st.empty()
    status.info("Waking up server...")

    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.post(API_URL, json={"name": name, "position": position})
            if response.status_code == 200:
                status.success("✅ Video generated successfully!")
                video_bytes = response.content
                st.download_button(
                    label="Download Your Greeting Video",
                    data=video_bytes,
                    file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
                    mime="video/mp4"
                )
                break
            else:
                status.error(f"API error: {response.status_code}")
                break
        except requests.exceptions.RequestException:
            time.sleep(2)
            status.info("Retrying...")
    else:
        status.error("❌ Could not connect to the API. Please try again later.")
