from common import *


def get_best_to_solve(solved, known, dictionary):
    best_option = 0
    best_score = 100000000
    for i, is_solved in enumerate(solved):
        possible_words = len(dictionary[i])
        if possible_words < best_score and not is_solved:
            best_option = i
            best_score = possible_words
    return best_option


def best_word(word_sets, known, currently_solving):
    words = word_sets[currently_solving]
    ltr_count = count_letters(words)
    best = ''
    best_score = 0
    for word in words:
        scores = {}
        occurrences = {}
        for i, char in enumerate(word):
            ltr_score = 0
            if char in occurrences:
                ltr_score += ltr_count[i][char] / (occurrences[char] + 3)
                scores[char] = min(scores[char], scores[char] / (occurrences[char] + 3))
                occurrences[char] += 1
            else:
                ltr_score += ltr_count[i][char]
                occurrences[char] = 1
            known_char = known[currently_solving][char][i]
            if known_char == 'y':
                ltr_score *= 20
            elif known_char == 'n':
                ltr_score = -1000000000
            elif known_char == 'm':
                ltr_score *= 5
            scores[char] = ltr_score
        score = sum(scores.values())
        if score > best_score:
            best = word
            best_score = score
    return best


def help_solve(simultaneous, length):
    dictionary = [get_words(length) for _ in range(simultaneous)]
    known = [{char: 'u' * length for char in ALPHABET} for _ in range(simultaneous)]
    solved = [False for _ in range(simultaneous)]
    currently_solving = 0
    while True:
        print(f'Currently solving {currently_solving}')
        best_choice = best_word(dictionary, known, currently_solving)
        if not best_choice:
            print("Couldn't find a word that fits. Sorry")
            return
        print(f"Best choice: {best_choice}")
        print("Enter responses, separated by a space. n: letter not in word, m: letter in word, wrong place, "
              "y: letter in right place")
        print("Enter 'help' for help, or just hit enter to exit.")
        answer = input("Response: ").lower()
        if answer == 'again':
            print(f"Restarting with {simultaneous} wordles with {length} letters")
            print()
            help_solve(simultaneous, length)
            return
        if answer == 'known':
            print(known, sep='\n')
            continue
        if answer == 'words':
            print(*dictionary, sep='\n')
            continue
        if answer == 'help':
            print("Enter 'again' to go again with the same number of letters")
            print("Enter 'known' to see what the program knows about what letters go where")
            print("Enter 'words' to see the list of valid words given what the program knows")
            print()
            continue
        if len(answer) == 0:
            print("exiting")
            return
        for wordle_i, word_answer in enumerate(answer.split(' ')):
            not_chars = ''
            for i, char in enumerate(best_choice):
                if word_answer[i] == 'n':
                    if 'y' in known[wordle_i][char]:
                        known[wordle_i][char] = known[wordle_i][char].replace('u', 'n').replace('m', 'n')
                    elif 'm' in known[wordle_i][char]:
                        known[wordle_i][char] = known[wordle_i][char][:i] + "n" + known[wordle_i][char][i + 1:]
                    else:
                        known[wordle_i][char] = 'n' * length
                        not_chars += char
                elif word_answer[i] == 'm':
                    known[wordle_i][char] = known[wordle_i][char].replace('u', 'm')
                    # if it's m, it's not in the right place so we know i is n for char
                    known[wordle_i][char] = known[wordle_i][char][:i] + "n" + known[wordle_i][char][i + 1:]
                    not_chars.replace(char, '')
                    # if it's m and all but one index is n, the last m needs to be y
                    if known[wordle_i][char].count('n') == length - 1:
                        known[wordle_i][char] = known[wordle_i][char].replace('m', 'y')
                        print(f'Know {char} is at pos {known[wordle_i][char].find("y")}')
                        dictionary[wordle_i] = only_letter_pos(dictionary[wordle_i],
                                                               known[wordle_i][char].find('y'), char)
                    else:
                        dictionary[wordle_i] = not_letter_pos(dictionary[wordle_i], i, char)
                    dictionary[wordle_i] = filter_has_char(dictionary[wordle_i], char)
                elif word_answer[i] == 'y':
                    known[wordle_i][char] = known[wordle_i][char][:i] + "y" + known[wordle_i][char][i + 1:]
                    not_chars.replace(char, '')
                    # if the letter at i is char, no other letter can be there so set known[all chars but char][i] to n
                    for ch in ALPHABET.replace(char, ''):
                        known[wordle_i][ch] = known[wordle_i][ch][:i] + "n" + known[wordle_i][ch][i + 1:]
                    dictionary[wordle_i] = only_letter_pos(dictionary[wordle_i], i, char)
            dictionary[wordle_i] = filter_chars(dictionary[wordle_i], not_chars)
            if wordle_i == currently_solving and word_answer == "y"*length:
                solved[wordle_i] = True
        currently_solving = get_best_to_solve(solved, known, dictionary)


def main():
    simultaneous = int(input("How many simultaneous wordles?: "))
    length = int(input("What word length?: "))
    help_solve(simultaneous, length)
