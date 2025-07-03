import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment, silence
import os
import tempfile
import time

MAX_WORDS = 10000

st.title("🎙️ MP3/WAV to Text Converter ")

lang_code = st.selectbox("Choose Language", [
    ("English", "en-US"),
    ("Urdu", "ur-PK")
], format_func=lambda x: x[0])[1]

uploaded_file = st.file_uploader("Upload an audio file (MP3 or WAV)", type=["mp3", "wav"])

if uploaded_file:
    st.audio(uploaded_file)

    input_path = None
    wav_path = None
    full_text = ""

    try:
        # Create a temp file path for the uploaded file
        fd_input, input_path = tempfile.mkstemp(suffix="." + uploaded_file.name.split(".")[-1])
        os.close(fd_input)  # Close file descriptor
        with open(input_path, "wb") as f:
            f.write(uploaded_file.read())

        # Convert to WAV using pydub
        audio = AudioSegment.from_file(input_path)
        fd_wav, wav_path = tempfile.mkstemp(suffix=".wav")
        os.close(fd_wav)
        audio.export(wav_path, format="wav")

        recognizer = sr.Recognizer()
        processed_audio = AudioSegment.from_wav(wav_path)

        st.info("Splitting audio by silence (simulated speaker separation)...")
        chunks = silence.split_on_silence(processed_audio, min_silence_len=700, silence_thresh=-40)

        for i, chunk in enumerate(chunks):
            fd_chunk, chunk_path = tempfile.mkstemp(suffix=".wav")
            os.close(fd_chunk)
            chunk.export(chunk_path, format="wav")

            with sr.AudioFile(chunk_path) as source:
                audio_data = recognizer.record(source)
                try:
                    part_text = recognizer.recognize_google(audio_data, language=lang_code)
                    full_text += f"Speaker {i+1}: {part_text}\n"
                except sr.UnknownValueError:
                    full_text += f"Speaker {i+1}: [Unclear]\n"

            os.remove(chunk_path)

        word_count = len(full_text.split())
        if word_count > MAX_WORDS:
            st.warning(f"Text exceeds {MAX_WORDS} words. Showing first {MAX_WORDS}.")
            full_text = ' '.join(full_text.split()[:MAX_WORDS])

        st.success("Transcription complete!")
        st.text_area("Transcribed Text", full_text, height=400)

        st.download_button(
            label="📥 Download Transcription as .txt",
            data=full_text,
            file_name="transcription.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

    finally:
        time.sleep(0.5)
        if input_path and os.path.exists(input_path):
            try: os.remove(input_path)
            except: pass
        if wav_path and os.path.exists(wav_path):
            try: os.remove(wav_path)
            except: pass

