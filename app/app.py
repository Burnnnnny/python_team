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
    ' ': '⠀', '\n': '\n'
}

# Korean Braille Dictionaries
_cho  = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_jung = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
_jong = " ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"

han_con_ini = {
    'ㄱ': '⠈', 'ㄴ': '⠉', 'ㄷ': '⠊', 'ㄹ': '⠐', 'ㅁ': '⠑',
    'ㅂ': '⠘', 'ㅅ': '⠠', 'ㅇ': '⠁', 'ㅈ': '⠨', 'ㅊ': '⠰', 'ㅋ': '⠋',
    'ㅌ': '⠓', 'ㅍ': '⠙', 'ㅎ': '⠚', 'ㄲ': '⠠⠈', 'ㄸ': '⠠⠊',
    'ㅃ': '⠠⠘', 'ㅆ': '⠠⠠', 'ㅉ': '⠠⠨'
}

han_con_fin = {
    'ㄱ': '⠁', 'ㄴ': '⠒', 'ㄷ': '⠔', 'ㄹ': '⠂', 'ㅁ': '⠢', 'ㅂ': '⠃',
    'ㅅ': '⠄', 'ㅇ': '⠶', 'ㅈ': '⠅', 'ㅊ': '⠆', 'ㅋ': '⠖', 'ㅌ': '⠲',
    'ㅍ': '⠴', 'ㅎ': '⠶', 'ㄲ': '⠠⠁', 'ㄸ': '⠠⠔', 'ㅃ': '⠠⠃', 'ㅆ': '⠌', 'ㅉ': '⠠⠅'
}

han_gat = {
    'ㅏ': '⠣', 'ㅑ': '⠜', 'ㅓ': '⠎', 'ㅕ': '⠱', 'ㅗ': '⠥', 'ㅛ': '⠬',
    'ㅜ': '⠍', 'ㅠ': '⠩', 'ㅡ': '⠪', 'ㅣ': '⠕', 'ㅐ': '⠗', 'ㅔ': '⠝',
    'ㅚ': '⠽', 'ㅝ': '⠏', 'ㅢ': '⠺', 'ㅖ': '⠌', 'ㅟ': '⠍⠗', 'ㅒ': '⠜⠗',
    'ㅙ': '⠧⠗', 'ㅞ': '⠏⠗'
}

han_abb = {
    '가': '⠫', '나': '⠉', '다': '⠊', '마': '⠑', '바': '⠘', '사': '⠇',
    '자': '⠨', '카': '⠋', '타': '⠓', '파': '⠙', '하': '⠚', '것': '⠸⠎',
    '억': '⠹', '언': '⠾', '얼': '⠞', '연': '⠡', '열': '⠳', '영': '⠻',
    '옥': '⠭', '온': '⠷', '옹': '⠿', '운': '⠛', '울': '⠯', '은': '⠵',
    '을': '⠮', '인': '⠟', '그래서': '⠁⠎', '그러나': '⠁⠉', '그러면': '⠁⠒',
    '그러므로': '⠁⠢', '그런데': '⠁⠝', '그리고': '⠁⠥', '그리하여': '⠁⠱'
}

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

def translate_korean_to_braille(text):
    braille_text = []
    for char in text:
        if char in han_abb:
            braille_text.append(han_abb[char])
        else:
            cho, jung, jong = decompose_hangul(char)
            if cho in han_con_ini:
                braille_text.append(han_con_ini[cho])
            if jung in han_gat:
                braille_text.append(han_gat[jung])
            if jong.strip() in han_con_fin:
                braille_text.append(han_con_fin[jong.strip()])
        if char in pun_mark:
            braille_text.append(pun_mark[char])
        elif char == ' ':
            braille_text.append('⠀')
        elif char == '\n':
            braille_text.append('\n')
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
    if all('가' <= char <= '힣' or char.isspace() or char in pun_mark for char in text):
        return translate_korean_to_braille(text)
    else:
        return translate_english_to_braille(text)

def compose_hangul(decomposed):
    cho, jung, jong = decomposed
    cho_idx = _cho.index(cho)
    jung_idx = _jung.index(jung)
    jong_idx = _jong.index(jong)
    return chr(0xAC00 + (cho_idx * 21 + jung_idx) * 28 + jong_idx)

def translate_braille_to_korean(braille):
    reverse_han_con_ini = {v: k for k, v in han_con_ini.items()}
    reverse_han_gat = {v: k for k, v in han_gat.items()}
    reverse_han_con_fin = {v: k for k, v in han_con_fin.items()}
    reverse_han_abb = {v: k for k, v in han_abb.items()}
    reverse_pun_mark = {v: k for k, v in pun_mark.items()}

    text = []
    i = 0
    while i < len(braille):
        if braille[i:i+2] in reverse_han_abb:
            text.append(reverse_han_abb[braille[i:i+2]])
            i += 2
        elif braille[i] in reverse_han_con_ini:
            cho = reverse_han_con_ini[braille[i]]
            i += 1
            jung = ''
            jong = ''
            if i < len(braille) and braille[i] in reverse_han_gat:
                jung = reverse_han_gat[braille[i]]
                i += 1
            if i < len(braille) and braille[i] in reverse_han_con_fin:
                jong = reverse_han_con_fin[braille[i]]
                i += 1
            if jung:
                text.append(compose_hangul([cho, jung, jong]))
            else:
                text.append(cho)
        elif braille[i] in reverse_pun_mark:
            text.append(reverse_pun_mark[braille[i]])
            i += 1
        else:
            text.append(braille[i])
            i += 1
    return ''.join(text)

def translate_braille_to_english(braille):
    reverse_eng_braille = {v: k for k, v in eng_braille.items()}
    reverse_num_braille = {v: k for k, v in num_braille.items()}
    reverse_pun_mark = {v: k for k, v in pun_mark.items()}

    text = []
    i = 0
    while i < len(braille):
        if braille[i:i+2] in reverse_eng_braille:
            text.append(reverse_eng_braille[braille[i:i+2]])
            i += 2
        elif braille[i] in reverse_eng_braille:
            text.append(reverse_eng_braille[braille[i]])
            i += 1
        elif braille[i] in reverse_num_braille:
            text.append(reverse_num_braille[braille[i]])
            i += 1
        elif braille[i] in reverse_pun_mark:
            text.append(reverse_pun_mark[braille[i]])
            i += 1
        else:
            text.append(braille[i])
            i += 1
    return ''.join(text)

def translate_braille_to_text(braille, language):
    if language == 'korean':
        return translate_braille_to_korean(braille)
    elif language == 'english':
        return translate_braille_to_english(braille)
    else:
        return braille

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
    language = request.form.get('language', 'english')  # Default to 'english' if not provided
    if direction == 'left-to-right':
        translated_text = translate_to_braille(text)
    elif direction == 'right-to-left':
        translated_text = translate_braille_to_text(text, language)
    else:
        translated_text = text
    return translated_text

if __name__ == '__main__':
    app.run(debug=True, port=30000)
