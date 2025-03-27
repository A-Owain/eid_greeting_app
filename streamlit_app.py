
import requests
import streamlit as st

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

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter your name.")
        st.stop()

    with st.spinner("Sending your request..."):
        try:
            API_URL = "https://eid-video-api.onrender.com/generate-video"
            response = requests.post(
                API_URL,
                json={"name": name, "position": position}
            )

            if response.status_code == 200:
                video_bytes = response.content
                st.success("✅ Video generated successfully!")
                st.download_button(
                    label="Download Your Greeting Video",
                    data=video_bytes,
                    file_name=f"eid_greeting_{name.replace(' ', '_')}.mp4",
                    mime="video/mp4"
                )
            else:
                st.error(f"API error: {response.status_code}")
        except Exception as e:
            st.error("API error: Server not responding.")
