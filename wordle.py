import random
import quordle
from common import *


# known: {char: [muynn]} / m = maybe, u = unknown, y = yes, n = no
def best_word(words, known):
    ltr_count = count_letters(words)
    # print(*ltr_count, sep='\n')
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
            known_char = known[char][i]
            if known_char == 'y':
                ltr_score *= 20
            elif known_char == 'n':
                ltr_score = -1000000000000
            elif known_char == 'm':
                ltr_score *= 5
            scores[char] = ltr_score
        score = sum(scores.values())
        if score > best_score:
            best = word
            best_score = score
    return best


def run_round(real_word, dictionary, known, length):
    guess = best_word(dictionary, known)
    print(guess)
    if guess == real_word:
        return dictionary, True
    not_chars = ''
    for i, char in enumerate(guess):
        if char not in real_word:
            known[char] = 'n' * length
            print('n', end='')
            not_chars += char
        elif real_word[i] == char:
            known[char] = known[char][:i] + "y" + known[char][i + 1:]
            print('y', end='')
        else:
            known[char] = known[char].replace('u', 'm')
            known[char] = known[char][:i] + "n" + known[char][i + 1:]
            print('m', end='')
    print()
    return filter_chars(dictionary, not_chars), False


def solve_word():
    real_word = input("Enter a word to solve: ").lower()
    length = len(real_word)
    dictionary = get_words(length)
    # real_word = 'apply'  # random.choice(dictionary)
    known = {char: 'u' * length for char in ALPHABET}
    round_count = 0
    won = False
    while not won:
        round_count += 1
        print(f'Round {round_count}:')
        dictionary, won = run_round(real_word, dictionary, known, length)
        if round_count > 20:
            print("Couldn't solve word :( exiting")
            break
    else:
        print(f"Correct, the word was {real_word}")
        print(f"Success in {round_count} rounds")
        return


def help_solve(length):
    dictionary = get_words(length)
    known = {char: 'u' * length for char in ALPHABET}
    while True:
        best_choice = best_word(dictionary, known)
        if not best_choice:
            print("Couldn't find a word that fits. Sorry")
            return
        print(f"Best choice: {best_choice}")
        print("Enter response. n: letter not in word, m: letter in word, wrong place, y: letter in right place")
        print("Enter 'help' for help, or just hit enter to exit")
        answer = input("Response: ").lower()
        if answer == 'again':
            print(f"Restarting with {length} letters")
            print()
            help_solve(length)
            return
        if answer == 'known':
            print(known, sep='\n')
            continue
        if answer == 'words':
            print(dictionary)
            continue
        if answer == 'help':
            print("Enter 'again' to go again with the same number of letters")
            print("Enter 'known' to see what the program knows about what letters go where")
            print("Enter 'words' to see the list of valid words given what the program knows")
            print()
            continue
        if len(answer) != length:
            print("exiting")
            return
        not_chars = ''
        for i, char in enumerate(best_choice):
            if answer[i] == 'n':
                if 'y' in known[char]:
                    known[char] = known[char].replace('u', 'n').replace('m', 'n')
                elif 'm' in known[char]:
                    known[char] = known[char][:i] + "n" + known[char][i + 1:]
                else:
                    known[char] = 'n' * length
                    not_chars += char
            elif answer[i] == 'm':
                known[char] = known[char].replace('u', 'm')
                # if it's m, it's not in the right place so we know i is n for char
                known[char] = known[char][:i] + "n" + known[char][i + 1:]
                not_chars.replace(char, '')
                # if it's m and all but one index is n, the last m needs to be y
                if known[char].count('n') == length - 1:
                    known[char] = known[char].replace('m', 'y')
                    print(f'Know {char} is at pos {known[char].find("y")}')
                    dictionary = only_letter_pos(dictionary, known[char].find('y'), char)
                else:
                    dictionary = not_letter_pos(dictionary, i, char)
                dictionary = filter_has_char(dictionary, char)
            elif answer[i] == 'y':
                known[char] = known[char][:i] + "y" + known[char][i + 1:]
                not_chars.replace(char, '')
                # if the letter at i is char, no other letter can be there so set known[all chars but char][i] to n
                for ch in ALPHABET.replace(char, ''):
                    known[ch] = known[ch][:i] + "n" + known[ch][i + 1:]
                dictionary = only_letter_pos(dictionary, i, char)
        dictionary = filter_chars(dictionary, not_chars)


def save_me(length):
    dictionary = get_words(length)
    known = {char: 'u' * length for char in ALPHABET}
    while True:
        word = input("Your next guess: ")
        print("Enter response. n: letter not in word, m: letter in word, wrong place, y: letter in right place")
        print("Enter 'help' for help, or just hit enter to exit")
        answer = input("Response: ").lower()
        if answer == 'again':
            print(f"Restarting with {length} letters")
            print()
            help_solve(length)
            return
        if answer == "best":
            print(best_word(dictionary, known))
            continue
        if answer == 'known':
            print(known, sep='\n')
            continue
        if answer == 'words':
            print(dictionary)
            continue
        if answer == 'help':
            print("Enter 'again' to go again with the same number of letters")
            print("Enter 'known' to see what the program knows about what letters go where")
            print("Enter 'words' to see the list of valid words given what the program knows")
            print()
            continue
        if len(answer) != length:
            print("exiting")
            return
        not_chars = ''
        for i, char in enumerate(word):
            if answer[i] == 'n':
                if 'y' in known[char]:
                    known[char] = known[char].replace('u', 'n').replace('m', 'n')
                elif 'm' in known[char]:
                    known[char] = known[char][:i] + "n" + known[char][i + 1:]
                else:
                    known[char] = 'n' * length
                    not_chars += char
            elif answer[i] == 'm':
                known[char] = known[char].replace('u', 'm')
                # if it's m, it's not in the right place so we know i is n for char
                known[char] = known[char][:i] + "n" + known[char][i + 1:]
                not_chars.replace(char, '')
                # if it's m and all but one index is n, the last m needs to be y
                if known[char].count('n') == length - 1:
                    known[char] = known[char].replace('m', 'y')
                    print(f'Know {char} is at pos {known[char].find("y")}')
                    dictionary = only_letter_pos(dictionary, known[char].find('y'), char)
                else:
                    dictionary = not_letter_pos(dictionary, i, char)
                dictionary = filter_has_char(dictionary, char)
            elif answer[i] == 'y':
                known[char] = known[char][:i] + "y" + known[char][i + 1:]
                not_chars.replace(char, '')
                # if the letter at i is char, no other letter can be there so set known[all chars but char][i] to n
                for ch in ALPHABET.replace(char, ''):
                    known[ch] = known[ch][:i] + "n" + known[ch][i + 1:]
                dictionary = only_letter_pos(dictionary, i, char)
        dictionary = filter_chars(dictionary, not_chars)


def main():
    print("Enter 'solve' to enter a word and have the program solve")
    print("Enter 'help' to have the program help you solve the wordle")
    print("Enter 'quordle' to have the program help you solve a multiple simultaneous wordle")
    print("Enter 'saveme' to have the program help you with an in-progress wordle")
    choice = input("Choice: ").lower()
    if choice == 'solve':
        solve_word()
    elif choice == 'help':
        print("What word length?")
        length = int(input("Length: "))
        help_solve(length)
    elif choice == 'quordle':
        quordle.main()
    elif choice == 'saveme':
        print("What word length?")
        length = int(input("Length: "))
        save_me(length)
    else:
        print("didn't recognize choice, exiting")


if __name__ == "__main__":
    main()
