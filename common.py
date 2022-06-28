ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def get_words(length):
    with open("dictionary.txt", "r") as file:
        dictionary = filter_chars(filter_length(strip_newline(file.readlines()), length), """/'"1234567890-._()""")
    return dictionary


def strip_newline(words):
    return [word.replace('\n', '') for word in words]


def filter_length(words, length):
    real_dict = []
    for word in words:
        if len(word) == length:
            real_dict.append(word.lower())
    return real_dict


def filter_has_char(words, char):
    real_dict = []
    for word in words:
        if char in word:
            real_dict.append(word)
    return real_dict


def filter_chars(words, disallowed_chars):
    real_dict = []
    for word in words:
        ok = True
        for char in disallowed_chars:
            if char in word:
                ok = False
                break
        if ok:
            real_dict.append(word)
    return real_dict


def only_letter_pos(words, pos, char):
    real_words = []
    for word in words:
        if word[pos] == char:
            real_words.append(word)
    return real_words


def not_letter_pos(words, pos, char):
    real_words = []
    for word in words:
        if word[pos] != char:
            real_words.append(word)
    return real_words


def count_letters(words):
    d = [{char: 0 for char in ALPHABET} for _ in range(len(words[0]))]
    for word in words:
        for i, char in enumerate(word):
            d[i][char] += 1
    return d
