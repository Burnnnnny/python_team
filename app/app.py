from flask import Flask, render_template, request, send_file
from gtts import gTTS
import os

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    braille_text = ''
    plain_text = ''
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
            braille_text = translate_to_braille(text)
        elif 'braille' in request.form:
            braille = request.form['braille']
            plain_text = translate_to_text(braille)
    return render_template('index.html', braille_text=braille_text, plain_text=plain_text)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        text = file.read().decode('utf-8')
        braille_text = translate_to_braille(text)
        with open('translated.txt', 'w', encoding='utf-8') as f:
            f.write(braille_text)
        return send_file('translated.txt', as_attachment=True)

@app.route('/tts', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    tts = gTTS(text)
    tts.save("speech.mp3")
    return send_file("speech.mp3", as_attachment=True)

@app.route('/copy', methods=['POST'])
def copy_text():
    return 'Text copied to clipboard!', 200

if __name__ == '__main__':
    app.run(debug=True)
