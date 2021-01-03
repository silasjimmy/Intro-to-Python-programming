# Problem Set 2, hangman.py
# Name: Silas Jimmy
# Collaborators: None
# Time spent: A couple of days

# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    line = inFile.readline()
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    formed_word = []
    letters_guessed_copy = letters_guessed[:]
    for letter in secret_word:
        if letter in letters_guessed_copy:
            formed_word.extend(letter)
            letters_guessed_copy.remove(letter)
        else:
            formed_word.extend('_ ')
    if formed_word[-1] == ' ':
        formed_word.pop()
    formed_word = ''.join(formed_word)
    if secret_word == formed_word:
        return True
    return False

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = []
    letters_guessed_copy = letters_guessed[:]
    for letter in secret_word:
        if letter in letters_guessed_copy:
            guessed_word.append(letter)
        else:
            guessed_word.append('_')
            guessed_word.append(' ')
    if guessed_word[-1] == ' ':
        guessed_word.pop()
    guessed_word = ''.join(guessed_word)
    return guessed_word

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    lowercase_letters = string.ascii_lowercase
    lowercase_letters_list = list(string.ascii_lowercase)
    for letter in lowercase_letters:
        if letter in letters_guessed:
            lowercase_letters_list.remove(letter)
    available_letters = ''.join(lowercase_letters_list)
    return available_letters

def is_valid_guess(guess, letters_guessed):
    '''
    guess (character): user's guess
    letters_guessed (list): letters guessed so far
    Returns True if guess is an alphabet and of length 1, False otherwise
    '''
    if str.isalpha(guess) and len(guess) == 1:
        if guess not in letters_guessed:
            return True
    return False

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    '''
    number_of_guesses = 6
    warnings = 3
    letters_guessed = []
    available_letters = get_available_letters(letters_guessed)
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    
    print ("Welcome to the game Hangman!")
    print ("I am thinking of a word that is", len(secret_word), "letters long.")
    print ("You have",  warnings, "warnings left.")
    
    while number_of_guesses > 0:
        print ("----------------------")        
        print ("You have", number_of_guesses, "guesses left.")
        print ("Available letters:", available_letters)
        guess = str.lower(input("Please guess a letter: "))
        if is_valid_guess(guess, letters_guessed):
            letters_guessed.append(guess)
            guessed_word = get_guessed_word(secret_word, letters_guessed)
            available_letters = get_available_letters(letters_guessed)
            if guess in secret_word:
                print ("Good guess:", guessed_word)
            else:
                print ("Oops! That letter is not in my word:", guessed_word)
                if guess in list("aeiou"):
                    number_of_guesses -= 2
                else:
                    number_of_guesses -= 1
        else:
            if warnings > 0:
                warnings -= 1
            else:
                number_of_guesses -= 1
            if guess in letters_guessed:
                print ("Oops! You've already guessed that letter. You now have", warnings, "warnings:", guessed_word)
            else:
                print ("Oops! That is not a valid letter. You have", warnings, "warnings left:", guessed_word)
        if is_word_guessed(secret_word, [l for l in guessed_word]):
            print ("----------------------")
            print ("Congratulations, you won!")
            print ("Your total score for this game is:", number_of_guesses * len(secret_word))
            break
    if not is_word_guessed(secret_word, [l for l in guessed_word]):
        print ("----------------------")
        print ("Sorry, you ran out of guesses. The word was", secret_word)

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_list = [l for l in my_word if l != ' ']
    other_word_list = list(other_word)    
    if len(my_word_list) != len(other_word_list):
        return False
    for index, letter in enumerate(my_word_list):
        if letter == '_':
            continue
        elif letter != other_word_list[index]:
            return False
    return True

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    possible_matches = ' '.join(possible_matches)
    if len(possible_matches) > 0:
        print (possible_matches)
    else:
        print ('No matches found')

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    Starts up an interactive game of Hangman.
    '''
    number_of_guesses = 6
    warnings = 3
    letters_guessed = []
    available_letters = get_available_letters(letters_guessed)
    guessed_word = get_guessed_word(secret_word, letters_guessed)
    
    print ("Welcome to the game Hangman!")
    print ("I am thinking of a word that is", len(secret_word), "letters long.")
    print ("You have",  warnings, "warnings left.")
    
    while number_of_guesses > 0:
        print ("----------------------")        
        print ("You have", number_of_guesses, "guesses left.")
        print ("Available letters:", available_letters)
        guess = str.lower(input("Please guess a letter: "))
        if guess == '*':
            show_possible_matches(guessed_word)
        else:
            if is_valid_guess(guess, letters_guessed):
                letters_guessed.append(guess)
                guessed_word = get_guessed_word(secret_word, letters_guessed)
                available_letters = get_available_letters(letters_guessed)
                if guess in secret_word:
                    print ("Good guess:", guessed_word)
                else:
                    print ("Oops! That letter is not in my word:", guessed_word)
                    if guess in list("aeiou"):
                        number_of_guesses -= 2
                    else:
                        number_of_guesses -= 1
            else:
                if warnings > 0:
                    warnings -= 1
                else:
                    number_of_guesses -= 1
                if guess in letters_guessed:
                    print ("Oops! You've already guessed that letter. You now have", warnings, "warnings:", guessed_word)
                else:
                    print ("Oops! That is not a valid letter. You have", warnings, "warnings left:", guessed_word)
        if is_word_guessed(secret_word, [l for l in guessed_word]):
            print ("----------------------")
            print ("Congratulations, you won!")
            print ("Your total score for this game is:", number_of_guesses * len(secret_word))
            break
    if not is_word_guessed(secret_word, [l for l in guessed_word]):
        print ("----------------------")
        print ("Sorry, you ran out of guesses. The word was", secret_word)

if __name__ == "__main__":
#    Hangman
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###########################################
    
##    Hangman with hints
#    secret_word = choose_word(wordlist)
#    hangman_with_hints(secret_word)
