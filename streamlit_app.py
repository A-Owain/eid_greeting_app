import requests
import streamlit as st

st.title("Eid Greeting Video Generator")

name = st.text_input("Enter your name")
position = st.text_input("Enter your position (optional)")

if st.button("Generate Greeting Video"):
    if not name:
        st.warning("Please enter your name.")
        st.stop()

    with st.spinner("Sending your request..."):
        try:
            response = requests.post(
                "https://eid-video-api.onrender.com/generate-video",
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
            st.error(f"API error: Server not responding.")
