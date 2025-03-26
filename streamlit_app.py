import streamlit as st
import requests
import time

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

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

API_URL = "https://eid-video-api.onrender.com/generate-video"

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter your name.")
        st.stop()

    with st.spinner("Waking up the server... please wait!"):
        success = False
        for attempt in range(3):
            try:
                response = requests.post(API_URL, json={"name": name, "position": position})
                if response.status_code == 200:
                    success = True
                    break
            except Exception:
                time.sleep(2)

    if not success:
        st.error("API error: Server not responding.")
    else:
        with open("output.mp4", "wb") as f:
            f.write(response.content)

        st.success("\u2705 Video generated successfully!")
        with open("output.mp4", "rb") as video_file:
            st.download_button(
                label="Download Your Greeting Video",
                data=video_file,
                file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
                mime="video/mp4"
            )
