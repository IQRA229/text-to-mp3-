import streamlit as st
from gtts import gTTS
from io import BytesIO

# 🌐 Language Options
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

# 🎯 Page Configuration
st.set_page_config(page_title="Text-to-MP3 Converter", page_icon="🔊", layout="centered")

st.title("🔊 Text-to-MP3 Converter")
st.markdown("Convert **your text** into speech in multiple languages and download it as an MP3 file.")

# 🔠 Input Text Area
text_input = st.text_area("📝 Enter your text here:", height=300)

# 🌍 Language Selector
language = st.selectbox("🌐 Select a language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[language]

# ▶️ Sample Voice
with st.expander("▶️ Hear Sample Voice (English)"):
    sample_text = "This is a sample text-to-speech conversion using gTTS."
    sample_tts = gTTS(text=sample_text, lang="en")
    sample_audio = BytesIO()
    sample_tts.write_to_fp(sample_audio)
    sample_audio.seek(0)
    st.audio(sample_audio, format="audio/mp3")

# 🎧 Convert Button
if st.button("🎧 Convert to MP3"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text to convert.")
    else:
        try:
            tts = gTTS(text=text_input.strip(), lang=lang_code)
            mp3_fp = BytesIO()
            tts.write_to_fp(mp3_fp)
            mp3_fp.seek(0)

            st.success("✅ MP3 is ready!")
            st.audio(mp3_fp, format="audio/mp3")
            st.download_button("📥 Download MP3", mp3_fp, file_name="converted.mp3", mime="audio/mpeg")
        except Exception as e:
            st.error(f"❌ Conversion failed: {e}")
