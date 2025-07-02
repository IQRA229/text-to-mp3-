import streamlit as st
from gtts import gTTS
import os
import base64

# Supported languages
languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn"
}

# App UI
st.set_page_config(page_title="Text to MP3 Converter", layout="centered")
st.title("🎙️ Text to MP3 Converter")

text_input = st.text_area("Enter text here:", height=200)

language = st.selectbox("Choose language:", list(languages.keys()))
lang_code = languages[language]

if st.button("Convert to MP3"):
    if text_input.strip() == "":
        st.error("❌ Text field is empty.")
    else:
        try:
            tts = gTTS(text=text_input.strip(), lang=lang_code)
            filename = "output.mp3"
            tts.save(filename)

            with open(filename, "rb") as f:
                mp3_data = f.read()
                b64 = base64.b64encode(mp3_data).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">🎧 Download MP3</a>'
                st.success("✅ Conversion successful!")
                st.markdown(href, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")
