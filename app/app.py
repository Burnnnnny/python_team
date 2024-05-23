from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSLATED_FILE = 'translated.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 영어 점자 (소문자, 대문자 구분)
eng_braille = {
    'a': '⠁', 'b': '⠃', 'c': '⠉', 'd': '⠙', 'e': '⠑', 'f': '⠋', 'g': '⠛',
    'h': '⠓', 'i': '⠊', 'j': '⠚', 'k': '⠅', 'l': '⠇', 'm': '⠍', 'n': '⠝',
    'o': '⠕', 'p': '⠏', 'q': '⠟', 'r': '⠗', 's': '⠎', 't': '⠞', 'u': '⠥',
    'v': '⠧', 'w': '⠺', 'x': '⠭', 'y': '⠽', 'z': '⠵',
    'A': '⠠⠁', 'B': '⠠⠃', 'C': '⠠⠉', 'D': '⠠⠙', 'E': '⠠⠑', 'F': '⠠⠋',
    'G': '⠠⠛', 'H': '⠠⠓', 'I': '⠠⠊', 'J': '⠠⠚', 'K': '⠠⠅', 'L': '⠠⠇',
    'M': '⠠⠍', 'N': '⠠⠝', 'O': '⠠⠕', 'P': '⠠⠏', 'Q': '⠠⠟', 'R': '⠠⠗',
    'S': '⠠⠎', 'T': '⠠⠞', 'U': '⠠⠥', 'V': '⠠⠧', 'W': '⠠⠺', 'X': '⠠⠭',
    'Y': '⠠⠽', 'Z': '⠠⠵'
}

# 숫자 점자
num_braille = {
    '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
    '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊'
}

# 문장 부호
pun_mark = {
    '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠐⠂', '?': '⠦', '!': '⠖',
    '(': '⠦⠄', ')': '⠠⠴', "'": '⠄', '"': '⠶', '-': '⠤', '/': '⠌',
    '&': '⠯', '*': '⠔', '+': '⠖', '=': '⠶', '@': '⠈⠁', '#': '⠼',
    ' ': '⠀'
}

def translate_to_braille(text):
    braille_text = []
    for char in text:
        if char in eng_braille:
            braille_text.append(eng_braille[char])
        elif char in num_braille:
            braille_text.append(num_braille[char])
        elif char in pun_mark:
            braille_text.append(pun_mark[char])
        else:
            braille_text.append(char)
    return ''.join(braille_text)

def translate_to_text(braille):
    text = []
    braille_dict = {v: k for k, v in {**eng_braille, **num_braille, **pun_mark}.items()}
    i = 0
    while i < len(braille):
        if braille[i:i+2] in braille_dict:
            text.append(braille_dict[braille[i:i+2]])
            i += 2
        elif braille[i] in braille_dict:
            text.append(braille_dict[braille[i]])
            i += 1
        else:
            text.append(braille[i])
            i += 1
    return ''.join(text)

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
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
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
    if os.path.exists(TRANSLATED_FILE):
        os.remove(TRANSLATED_FILE)
    return '', 204

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    tts = gTTS(text)
    tts.save("speech.mp3")
    return send_file("speech.mp3", as_attachment=True)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.form['text']
    direction = request.form['direction']
    if direction == 'left-to-right':
        translated_text = translate_to_braille(text)
    elif direction == 'right-to-left':
        translated_text = translate_to_text(text)
    else:
        translated_text = text
    return translated_text

if __name__ == '__main__':
    app.run(debug=True)
