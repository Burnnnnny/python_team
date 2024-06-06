import re

# Configuration constants and dictionaries

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
    'ㅙ': '⠧⠗', 'ㅞ': '⠏⠗', 'ㅘ': '⠧'
}

han_abb = {
    '가': '⠫', '나': '⠉', '다': '⠊', '마': '⠑', '바': '⠘', '사': '⠇',
    '자': '⠨', '카': '⠋', '타': '⠓', '파': '⠙', '하': '⠚', '것': '⠸⠎',
    '억': '⠹', '언': '⠾', '얼': '⠞', '연': '⠡', '열': '⠳', '영': '⠻',
    '옥': '⠭', '온': '⠷', '옹': '⠿', '운': '⠛', '울': '⠯', '은': '⠵',
    '을': '⠮', '인': '⠟', '그래서': '⠁⠎', '그러나': '⠁⠉', '그러면': '⠁⠒',
    '그러므로': '⠁⠢', '그런데': '⠁⠝', '그리고': '⠁⠥', '그리하여': '⠁⠱'
}

# Functions for Braille translation

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
                if cho == 'ㅇ' and jung != 'ㅏ' and jung != 'ㅐ':
                    braille_text.append(han_gat.get(jung, '?'))
                else:
                    braille_text.append(han_con_ini[cho])
            if jung in han_gat and (cho != 'ㅇ' or jung in ['ㅏ', 'ㅐ']):
                braille_text.append(han_gat.get(jung, '?'))
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
    is_english = False
    for char in text:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            if not is_english:
                braille_text.append('⠠')  # English start marker
                is_english = True
            braille_text.append(eng_braille.get(char, char))
        elif '0' <= char <= '9':
            braille_text.append(num_braille.get(char, char))
        elif char in pun_mark:
            braille_text.append(pun_mark[char])
        else:
            if is_english:
                braille_text.append('⠼')  # English end marker
                is_english = False
            braille_text.append(char)
    if is_english:
        braille_text.append('⠼')  # Close English block if still open
    return ''.join(braille_text)

def translate_mixed_to_braille(text):
    braille_text = []
    i = 0
    while i < len(text):
        char = text[i]
        if '가' <= char <= '힣':
            braille_text.append(translate_korean_to_braille(char))
        elif 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            eng_text = []
            while i < len(text) and ('a' <= text[i] <= 'z' or 'A' <= text[i] <= 'Z'):
                eng_text.append(text[i])
                i += 1
            braille_text.append(translate_english_to_braille(''.join(eng_text)))
            continue
        elif '0' <= char <= '9':
            braille_text.append(num_braille.get(char, char))
        elif char in pun_mark:
            braille_text.append(pun_mark[char])
        else:
            braille_text.append(char)
        i += 1
    return ''.join(braille_text)

def translate_braille_to_english(braille):
    reverse_eng_braille = {v: k for k, v in eng_braille.items()}
    reverse_num_braille = {v: k for k, v in num_braille.items()}
    reverse_pun_mark = {v: k for k, v in pun_mark.items()}

    text = []
    i = 0
    is_english = False
    while i < len(braille):
        if braille[i:i+2] == '⠠':
            is_english = True
            i += 1
        elif braille[i:i+2] == '⠼':
            is_english = False
            i += 1
        elif is_english:
            if braille[i:i+2] in reverse_eng_braille:
                text.append(reverse_eng_braille[braille[i:i+2]])
                i += 2
            elif braille[i] in reverse_eng_braille:
                text.append(reverse_eng_braille[braille[i]])
                i += 1
            else:
                text.append(braille[i])
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
    if language == 'english':
        return translate_braille_to_english(braille)
    else:
        return braille

# Sample text for testing
text = "안녕하세요 hello 1234."
braille = translate_mixed_to_braille(text)
print("Original Text:", text)
print("Braille:", braille)
print("Back to Text:", translate_braille_to_text(braille, 'english'))

