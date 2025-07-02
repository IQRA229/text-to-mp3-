from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from gtts import gTTS
import speech_recognition as sr
import os

# Supported languages
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

cancel_requested = False  # Flag to control cancellation

def get_selected_language_code():
    return language_options.get(lang_var.get(), "en")

def convert_text_to_mp3():
    text = input_text.get("1.0", END).strip()
    if not text:
        messagebox.showerror("Error", "Text is empty!")
        return
    lang_code = get_selected_language_code()
    save_mp3(text, lang_code)

def record_speech_to_mp3():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Recording", "Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            messagebox.showinfo("Processing", "Converting speech to text...")
            text = recognizer.recognize_google(audio, language="en-US")
            input_text.delete("1.0", END)
            input_text.insert(END, text)
            lang_code = get_selected_language_code()
            save_mp3(text, lang_code)
        except sr.WaitTimeoutError:
            messagebox.showerror("Error", "No speech detected.")
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand the audio.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def save_mp3(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        file_path = filedialog.asksaveasfilename(defaultextension=".mp3",
                                                 filetypes=[("MP3 files", "*.mp3")],
                                                 title="Save MP3 As")
        if file_path:
            tts.save(file_path)
            messagebox.showinfo("Success", f"MP3 saved at:\n{file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save MP3:\n{str(e)}")

def cancel_batch():
    global cancel_requested
    cancel_requested = True
    progress_status.set("Cancelling...")

def batch_convert_folder():
    global cancel_requested
    cancel_requested = False

    folder_path = filedialog.askdirectory(title="Select Folder Containing .txt Files")
    if not folder_path:
        return
    output_folder = filedialog.askdirectory(title="Select Output Folder for MP3 Files")
    if not output_folder:
        return

    lang_code = get_selected_language_code()
    text_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".txt")]

    if not text_files:
        messagebox.showwarning("No Files", "No .txt files found in the selected folder.")
        return

    total_files = len(text_files)
    progress_bar["maximum"] = total_files
    progress_status.set(f"Converting 0 of {total_files}...")

    count = 0
    for i, file_name in enumerate(text_files, 1):
        if cancel_requested:
            progress_status.set("Cancelled by user.")
            break

        file_path = os.path.join(folder_path, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    tts = gTTS(text=text, lang=lang_code)
                    mp3_name = os.path.splitext(file_name)[0] + ".mp3"
                    save_path = os.path.join(output_folder, mp3_name)
                    tts.save(save_path)
                    count += 1
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {file_name}:\n{e}")
        progress_bar["value"] = i
        progress_status.set(f"Converting {i} of {total_files}...")
        root.update_idletasks()

    if not cancel_requested:
        progress_status.set(f"Completed: {count} of {total_files} files converted.")
        messagebox.showinfo("Done", f"Converted {count} files to MP3!")

# GUI Setup
root = Tk()
root.title("Text & Speech to MP3 Converter with Cancel Support")
root.geometry("570x570")
root.resizable(False, False)

Label(root, text="Enter text or record your voice:", font=("Arial", 12)).pack(pady=10)
input_text = Text(root, height=8, width=65)
input_text.pack(pady=5)

Label(root, text="Select Language:", font=("Arial", 11)).pack(pady=5)
lang_var = StringVar(root)
lang_var.set("English")
OptionMenu(root, lang_var, *language_options.keys()).pack(pady=5)

Button(root, text="Convert Text to MP3", command=convert_text_to_mp3,
       font=("Arial", 10), bg="#4CAF50", fg="white", width=30).pack(pady=10)

Button(root, text="Record Speech to MP3", command=record_speech_to_mp3,
       font=("Arial", 10), bg="#2196F3", fg="white", width=30).pack(pady=5)

Button(root, text="Batch Convert Text Files", command=batch_convert_folder,
       font=("Arial", 10), bg="#FF9800", fg="white", width=30).pack(pady=15)

# Progress and Cancel
progress_status = StringVar()
progress_status.set("Idle...")
Label(root, textvariable=progress_status, font=("Arial", 10)).pack()
progress_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
progress_bar.pack(pady=5)

Button(root, text="Cancel", command=cancel_batch,
       font=("Arial", 10), bg="#f44336", fg="white", width=20).pack(pady=10)

root.mainloop()



