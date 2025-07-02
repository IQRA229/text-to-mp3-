import streamlit as st
from gtts import gTTS
from io import BytesIO
import textwrap

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

# 🎯 Streamlit Page Config
st.set_page_config(page_title="Text-to-MP3 Converter", page_icon="🔊", layout="wide")
st.title("🔊 Text-to-MP3 Converter")
st.markdown("Convert **long text (up to 100,000 words)** to speech in multiple languages and download the MP3 file.")

# 🔠 Input Field
text_input = st.text_area("Paste your text here (max 100,000 words):", height=400)

# 🌍 Language Selection
language = st.selectbox("Select language:", list(LANGUAGES.keys()))
lang_code = LANGUAGES[language]

# 🧪 Sample
with st.expander("▶️ Hear Sample Voice (English)"):
    sample_text = "This is a sample text-to-speech conversion using gTTS."
    sample_tts = gTTS(sample_text, lang="en")
    sample_audio = BytesIO()
    sample_tts.save(sample_audio)
    sample_audio.seek(0)
    st.audio(sample_audio, format="audio/mp3")

# 🚀 Convert and Download
if st.button("🎧 Convert to MP3"):
    word_count = len(text_input.split())
    if not text_input.strip():
        st.warning("Please enter some text first.")
    elif word_count > 100000:
        st.error(f"Too many words! You entered {word_count}. Limit is 100,000.")
    else:
        try:
            tts = gTTS(text=text_input, lang=lang_code, slow=False)
            mp3_fp = BytesIO()
            tts.save(mp3_fp)
            mp3_fp.seek(0)
            st.success("✅ MP3 file is ready!")
            st.audio(mp3_fp, format="audio/mp3")
            st.download_button("📥 Download MP3", mp3_fp, file_name="converted.mp3", mime="audio/mpeg")
        except Exception as e:
            st.error(f"Conversion failed: {e}")




