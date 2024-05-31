from flask import Flask, render_template, request, send_file, jsonify
import os
from utils import save_file, read_file, delete_file, generate_tts
from braille_translator import translate_to_braille, translate_braille_to_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSLATED_FILE = 'translated.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

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
        file_path = save_file(file, UPLOAD_FOLDER)
        text = read_file(file_path)
        return jsonify({'file_uploaded': True, 'text': text})
    return render_template('upload.html')

@app.route('/translate-file', methods=['POST'])
def translate_file():
    text = request.form['text']
    braille_text = translate_to_braille(text)
    with open(TRANSLATED_FILE, 'w', encoding='utf-8') as f:
        f.write(braille_text)
    return jsonify({'translated_file': TRANSLATED_FILE})

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    return send_file(filename, as_attachment=True)

@app.route('/delete-translated', methods=['POST'])
def delete_translated():
    delete_file(TRANSLATED_FILE)
    return '', 204

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    tts_path = generate_tts(text)
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
