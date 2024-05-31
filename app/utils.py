import os
from gtts import gTTS

def save_file(file, upload_folder):
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def generate_tts(text):
    tts = gTTS(text)
    tts_path = "speech.mp3"
    tts.save(tts_path)
    return tts_path
