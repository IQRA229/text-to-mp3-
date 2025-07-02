import streamlit as st
from gtts import gTTS
from io import BytesIO
import speech_recognition as sr

# App title
st.title("🎙️ Text & Speech to MP3 Converter")

# Language options
language_options = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "Arabic": "ar",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Chinese": "zh-cn"
}

# Language selection
language = st.selectbox("🌐 Choose Language", list(language_options.keys()))
lang_code = language_options[language]

# Tabs for input modes
tab1, tab2 = st.tabs(["📝 Text Input", "🎤 Speech Input"])

# Text Input Tab
with tab1:
    text = st.text_area("Enter your text here:")
    if st.button("Convert Text to MP3"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            try:
                tts = gTTS(text=text, lang=lang_code)
                mp3_bytes = BytesIO()
                tts.write_to_fp(mp3_bytes)
                mp3_bytes.seek(0)
                st.audio(mp3_bytes, format="audio/mp3")
                st.download_button("⬇️ Download MP3", data=mp3_bytes, file_name="output.mp3", mime="audio/mpeg")
            except Exception as e:
                st.error(f"Conversion failed: {e}")

# Speech Input Tab
with tab2:
    st.info("This will use your microphone to record speech.")
    if st.button("🎤 Record and Convert"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Recording... Please speak.")
                audio = recognizer.listen(source, timeout=5)
                st.success("Recording complete. Processing...")
                text = recognizer.recognize_google(audio)
                st.write("Recognized Text:", text)

                tts = gTTS(text=text, lang=lang_code)
                mp3_bytes = BytesIO()
                tts.write_to_fp(mp3_bytes)
                mp3_bytes.seek(0)
                st.audio(mp3_bytes, format="audio/mp3")
                st.download_button("⬇️ Download MP3", data=mp3_bytes, file_name="speech_output.mp3", mime="audio/mpeg")
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition failed: {e}")
        except Exception as e:
            st.error(f"Error: {e}")



