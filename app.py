import streamlit as st
from gtts import gTTS
from io import BytesIO

# Supported languages
LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn"
}

# UI Setup
st.set_page_config(page_title="Text to MP3 Converter", layout="centered")
st.title("🎙️ Text to MP3 Converter")

text_input = st.text_area("Enter text here:", height=200)
language = st.selectbox("Choose language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[language]

if st.button("Convert to MP3"):
    if not text_input.strip():
        st.error("❌ Text field is empty.")
    else:
        try:
            tts = gTTS(text_input.strip(), lang=lang_code)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)        # Write into memory
            mp3_fp.seek(0)                # Rewind pointer

            st.success("✅ MP3 is ready!")
            st.audio(mp3_fp, format="audio/mp3")
            st.download_button(
                label="🎧 Download MP3",
                data=mp3_fp,
                file_name="converted.mp3",
                mime="audio/mpeg"
            )
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
