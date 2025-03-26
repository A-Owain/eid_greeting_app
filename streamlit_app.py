
import streamlit as st
import requests
import time

API_URL = "https://eid-video-api.onrender.com/generate-video"

st.set_page_config(page_title="Eid Greeting Video Generator", layout="centered")
st.title("Eid Greeting Video Generator")

st.markdown(
    '''
    <style>
    .stApp {background-color: #f9f9f9;}
    .stTextInput > div > div > input {font-size: 18px;}
    .stDownloadButton > button {
        background-color: #1a73e8;
        color: white;
        font-size: 16px;
        padding: 0.6em 1.5em;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #d93025;
        color: white;
        font-size: 16px;
        padding: 0.5em 1.2em;
        border-radius: 8px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter a name.")
        st.stop()

    with st.spinner("Generating your video... please wait"):
        try:
            for attempt in range(3):
                response = requests.post(API_URL, json={"name": name, "position": position})
                if response.status_code == 200:
                    break
                time.sleep(2)

            if response.status_code == 200:
                video_data = response.content
                st.success("✅ Video generated successfully!")
                st.download_button(
                    label="Download Your Greeting Video",
                    data=video_data,
                    file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
                    mime="video/mp4"
                )
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error("API error: Server not responding.")
