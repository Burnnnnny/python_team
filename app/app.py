from flask import Flask, render_template, request, send_file, jsonify
from gtts import gTTS
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
TRANSLATED_FILE = 'translated.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# English Braille (lowercase and uppercase)
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

# Number Braille
num_braille = {
    '0': '⠼⠚', '1': '⠼⠁', '2': '⠼⠃', '3': '⠼⠉', '4': '⠼⠙', '5': '⠼⠑',
    '6': '⠼⠋', '7': '⠼⠛', '8': '⠼⠓', '9': '⠼⠊'
}

# Punctuation Braille
pun_mark = {
    '.': '⠲', ',': '⠂', ';': '⠆', ':': '⠐⠂', '?': '⠦', '!': '⠖',
    '(': '⠦⠄', ')': '⠠⠴', "'": '⠄', '"': '⠶', '-': '⠤', '/': '⠌',
    '&': '⠯', '*': '⠔', '+': '⠖', '=': '⠶', '@': '⠈⠁', '#': '⠼',
    ' ': '⠀'
}

# Korean Braille Dictionaries
han_con_ini = {
    'ㄱ': '⠈', 'ㄴ': '⠉', 'ㄷ': '⠊', 'ㄹ': '⠐', 'ㅁ': '⠑',
    'ㅂ': '⠘', 'ㅅ': '⠠', 'ㅈ': '⠨', 'ㅊ': '⠰', 'ㅋ': '⠋',
    'ㅌ': '⠓', 'ㅍ': '⠙', 'ㅎ': '⠚', 'ㄲ': '⠠⠈', 'ㄸ': '⠠⠊',
    'ㅃ': '⠠⠘', 'ㅆ': '⠠⠠', 'ㅉ': '⠠⠨'
}

han_con_fin = {
    'ㄱ': '⠁', 'ㄴ': '⠒', 'ㄷ': '⠔', 'ㄹ': '⠂', 'ㅁ': '⠢', 'ㅂ': '⠃',
    'ㅅ': '⠄', 'ㅇ': '⠶', 'ㅈ': '⠅', 'ㅊ': '⠆', 'ㅋ': '⠖', 'ㅍ': '⠲',
    'ㅎ': '⠴', 'ㄲ': '⠠⠁', 'ㄸ': '⠠⠔', 'ㅃ': '⠠⠃', 'ㅆ': '⠌', 'ㅉ': '⠠⠅'
}

han_gat = {
    'ㅏ': '⠣', 'ㅑ': '⠜', 'ㅓ': '⠎', 'ㅕ': '⠱', 'ㅗ': '⠥', 'ㅛ': '⠬',
    'ㅜ': '⠍', 'ㅠ': '⠩', 'ㅡ': '⠪', 'ㅣ': '⠕', 'ㅐ': '⠗', 'ㅔ': '⠝',
    'ㅚ': '⠽', 'ㅝ': '⠏', 'ㅢ': '⠺', 'ㅖ': '⠌', 'ㅟ': '⠍⠗', 'ㅒ': '⠜⠗',
    'ㅙ': '⠧⠗', 'ㅞ': '⠏⠗'
}

# Function to decompose Hangul syllables into its components
def decompose_hangul(c):
    if '가' <= c <= '힣':
        base = ord('가')
        cho_base = 588
        jung_base = 28

        cho = (ord(c) - base) // cho_base
        jung = ((ord(c) - base) - (cho * cho_base)) // jung_base
        jong = (ord(c) - base) - (cho * cho_base) - (jung * jung_base)

        return _cho[cho], _jung[jung], _jong[jong]
    else:
        return c, '', ''

_cho  = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_jung = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
_jong = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

def translate_korean_to_braille(text):
    braille_text = []
    for char in text:
        if char in han_gat:
            braille_text.append(han_gat[char])
        else:
            cho, jung, jong = decompose_hangul(char)
            if cho in han_con_ini:
                braille_text.append(han_con_ini[cho])
            if jung in han_gat:
                braille_text.append(han_gat[jung])
            if jong.strip() in han_con_fin:
                braille_text.append(han_con_fin[jong.strip()])
    return ''.join(braille_text)

def translate_english_to_braille(text):
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

def translate_to_braille(text):
    if all('가' <= char <= '힣' for char in text if char.isalpha()):
        return translate_korean_to_braille(text)
    else:
        return translate_english_to_braille(text)

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
