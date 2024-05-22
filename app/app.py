from flask import Flask, render_template, request

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

@app.route('/', methods=['GET', 'POST'])
def index():
    braille_text = ''
    if request.method == 'POST':
        text = request.form['text']
        braille_text = translate_to_braille(text)
    return render_template('index.html', braille_text=braille_text)

if __name__ == '__main__':
    app.run(debug=True)
