# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Silas Jimmy
# Collaborators : None
# Time spent    : <total time>

import math
import random

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7
SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}
WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    
    print("Loading word list from file...")
    inFile = open(WORDLIST_FILENAME, 'r')
    wordlist = []
    
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    
    return wordlist

def get_frequency_dict(sequence):
    """
    sequence: string or list
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def get_word_score(word, n):
    """
    word: string
    n: int >= 0
    Returns the score for a word. Assumes the word is a
    valid word.
    """
    if len(word) == 0:
        return 0
    
    word = word.lower()
    first_component = 0
    
    for letter in word:
        first_component += SCRABBLE_LETTER_VALUES.get(letter, 0)
        
    points = 7 * len(word) - 3 * (n - len(word))
    second_component = points if points > 1 else 1
    word_score = first_component * second_component
    
    return word_score

def display_hand(hand):
    
    """
    hand: dictionary (string -> int)
    Displays the letters currently in the hand.
    """
    letters = []
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            letters.append(letter)
            
    return ' '.join(letters)

def deal_hand(n):
    """
    n: int >= 0
    Returns a random hand containing n lowercase letters.
    """
    hand={}
    num_vowels = int(math.ceil(n / 3))
    
    hand['*'] = 1

    for i in range(1, num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

def update_hand(hand, word):
    """
    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new_hand = {}
    word = word.lower()
    word_dict = get_frequency_dict(word)
    
    for letter in hand:
        n = hand.get(letter, 0) - word_dict.get(letter, 0)
        if n > 0:
            new_hand[letter] = n
            
    return new_hand

def is_valid_word(word, hand, word_list):
    """
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    """
    word = word.lower()
    
    if '*' in word:
        possible_words = []
        for v in VOWELS:
            l = list(word)
            l.remove('*')
            l.insert(word.index('*'), v)
            possible_words.append(''.join(l))
        matches = [w for w in word_list if w in possible_words]
        if matches:
            return True
    else:
        word_dict = get_frequency_dict(word)
        if word not in word_list:
            return False
        for letter in word_dict:
            if hand.get(letter) == None:
                return False
            elif word_dict.get(letter) > hand.get(letter, 0):
                return False
        return True

def calculate_handlen(hand):
    """ 
    hand: dictionary (string-> int)
    Returns the length (number of letters) in the current hand.
    """
    return sum(list(hand.values()))

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    total_score = 0
    
    while len(hand) > 0:
        print("Current hand:", display_hand(hand))
        user_input = input("Enter word or \'!!\' to indicate that you are finished: ")
        
        if user_input == '!!':
            break
        elif is_valid_word(user_input, hand, word_list):
            word_score = get_word_score(user_input, calculate_handlen(hand))
            total_score += word_score
            print(user_input, "earned", word_score, "points. Total:", total_score, "points")
        else:
            print("That is not a valid word. Please choose another word.")
        
        hand = update_hand(hand, user_input)
        
    if len(hand) == 0:
        print("\nRan out of letters.")
    print("Total score for this hand:", total_score)
    print("----------")
        
    return total_score

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    if letter in hand.keys():
        all_letters = list(VOWELS) + list(CONSONANTS)
        remaining_letters = [l for l in all_letters if l not in hand.keys()]
        substitute_letter = random.choice(remaining_letters)
        hand[substitute_letter] = hand.pop(letter)
    return hand
        
def play_game(word_list):
    """
    Allow the user to play a series of hands
    word_list: list of lowercase strings
    """
    total_hands_score = 0
    
    num_of_hands = int(input("Enter total number of hands: "))
    
    while num_of_hands > 0:
        hand = deal_hand(HAND_SIZE)
        print("Current hand:", display_hand(hand))
        s = input("Would you like to substitute a letter? ")
        
        if s == 'yes':
            letter = input("Which letter would you like to replace: ")
            hand = substitute_hand(hand, letter)
            
        total_hand_score = play_hand(hand, word_list)
        replay = input("Would you like to replay the hand? ")
        
        if replay == 'yes':
            total_hand_score = play_hand(hand, word_list)
            
        total_hands_score += total_hand_score
        num_of_hands -= 1
        
    print("Total score over all hands:", total_hands_score)

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
