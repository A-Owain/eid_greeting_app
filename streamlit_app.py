import streamlit as st
import requests

st.set_page_config(page_title="Eid Greeting Video Generator", layout="centered")
st.title("Eid Greeting Video Generator")

st.markdown("""
<style>
    .stApp { background-color: #f7f7f7; font-family: 'Segoe UI', sans-serif; }
    .stTextInput>div>div>input { font-size: 16px; }
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
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

API_URL = "https://eid-video-api.onrender.com/generate-video"

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter a name.")
        st.stop()

    with st.spinner("Generating video..."):
        try:
            response = requests.post(API_URL, json={"name": name, "position": position}, timeout=60)
            if response.status_code == 200:
                st.success("✅ Video generated successfully!")
                st.download_button(
                    label="Download Your Greeting Video",
                    data=response.content,
                    file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
                    mime="video/mp4"
                )
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error(f"API error: Server not responding.")
