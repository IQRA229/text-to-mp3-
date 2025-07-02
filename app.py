import streamlit as st
from gtts import gTTS
import os
from tempfile import NamedTemporaryFile

# Constants
MAX_WORDS = 10000

# App title
st.title("🗣️ Text to Speech Converter (MP3)")

# Step 1: Input text
text = st.text_area("Enter text to convert into speech (Max 10,000 words)", height=200)

# Step 2: Choose language
lang = st.selectbox("Select language", [
    ("English", "en"),
    ("Urdu", "ur"),
    ("Hindi", "hi"),
    ("Spanish", "es"),
    ("French", "fr"),
], format_func=lambda x: x[0])

# Step 3: Convert to MP3
if st.button("🎧 Convert to MP3"):
    word_count = len(text.strip().split())

    if not text.strip():
        st.warning("⚠️ Please enter some text.")
    elif word_count > MAX_WORDS:
        st.error(f"❌ Word limit exceeded. You entered {word_count} words. Limit is {MAX_WORDS}.")
    else:
        try:
            # Create TTS
            tts = gTTS(text=text, lang=lang[1])

            # Save to temporary file
            with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tts.save(tmp_file.name)
                st.success("✅ Conversion successful!")

                # Playback audio
                with open(tmp_file.name, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3")

                    # Download link
                    st.download_button("⬇️ Download MP3", audio_bytes, file_name="speech.mp3")

        except Exception as e:
            st.error(f"❌ Error during conversion: {e}")
