from flask import Flask, render_template, request, send_file, jsonify
import os
import threading
import time
from utils import save_file, read_file, generate_tts
from braille_translator import translate_to_braille, translate_braille_to_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSLATED_FOLDER = 'translated'
DELETE_DELAY = 300  # 5 minutes in seconds

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(TRANSLATED_FOLDER):
    os.makedirs(TRANSLATED_FOLDER)

def schedule_delete_file(filepath, delay):
    def delete_file_later(filepath, delay):
        time.sleep(delay)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted file: {filepath}")

    threading.Thread(target=delete_file_later, args=(filepath, delay)).start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'file_uploaded': False, 'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'file_uploaded': False, 'error': 'No selected file'}), 400
        if not file.filename.endswith('.txt'):
            return jsonify({'file_uploaded': False, 'error': 'Unsupported file type'}), 400
        if file.content_length > 10 * 1024 * 1024:
            return jsonify({'file_uploaded': False, 'error': 'File size exceeds limit'}), 400
        file_path = save_file(file, UPLOAD_FOLDER)
        text = read_file(file_path)
        schedule_delete_file(file_path, DELETE_DELAY)
        return jsonify({'file_uploaded': True, 'text': text, 'filename': file.filename})
    return render_template('upload.html')

@app.route('/translate-file', methods=['POST'])
def translate_file():
    text = request.form['text']
    original_filename = request.form['filename']
    braille_text = translate_to_braille(text)
    translated_filename = os.path.splitext(original_filename)[0] + '_번역본.txt'
    translated_filepath = os.path.join(TRANSLATED_FOLDER, translated_filename)
    with open(translated_filepath, 'w', encoding='utf-8') as f:
        f.write(braille_text)
    schedule_delete_file(translated_filepath, DELETE_DELAY)
    return jsonify({'translated_file': translated_filepath})

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    tts_path = generate_tts(text)
    schedule_delete_file(tts_path, DELETE_DELAY)
    return send_file(tts_path, as_attachment=True)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    direction = request.form['direction']
    language = request.form.get('language', 'english')
    if direction == 'left-to-right':
        translated_text = translate_to_braille(text)
    elif direction == 'right-to-left':
        translated_text = translate_braille_to_text(text, language)
    else:
        translated_text = text
    return translated_text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=30000)
