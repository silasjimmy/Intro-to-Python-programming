# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
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
	

# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
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

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    
    """
    hand: dictionary (string -> int)
    Displays the letters currently in the hand.
    """
    letters = []
    
    for letter in hand.keys():
        for j in range(hand[letter]):
            letters.append(letter)
#             print(letter, end=' ')      # print all on the same line
#    print()                              # print an empty line
    return ' '.join(letters)

#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
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

#
# Problem #2: Update a hand by removing letters
#
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

#
# Problem #3: Test word validity
#
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
        if word in word_list:
            for letter in word_dict:
                if word_dict.get(letter) > hand.get(letter, 0):
                    return False
        return True

#
# Problem #5: Playing a hand
#
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
    total_points = 0
    
    while len(hand) > 0:
        print("Current hand:", display_hand(hand))
        user_input = input("Enter word of !! to indicate that you are finished: ")
        
        if user_input == '!!':
            print("Total score:", total_points, "points")
            break
        elif is_valid_word(user_input, hand, word_list):
            word_score = get_word_score(user_input, calculate_handlen(hand))
            total_points += word_score
            print(user_input, "earned", word_score, "points. Total:", total_points, "points")
        else:
            print("That is not a valid word. Please choose another word.")
        
        hand = update_hand(hand, user_input)
        
    return total_points
        
#    if len(hand) == 0:
#        print("Ran out of letters. Total score:", total_points, "points")
    
    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    
        # Display the hand
        
        # Ask user for input
        
        # If the input is two exclamation points:
        
            # End the game (break out of the loop)

            
        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            # update the user's hand by removing the letters of their inputted word
            

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
# 


#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """ 
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.
    
    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    
    pass  # TO DO... Remove this line when you implement this function
       
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep 
      the better of the two scores for that hand.  This can only be done once 
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
#    play_game(word_list)
    hand = {'a':1, 'j':1, 'e':1, 'f':1, '*':1, 'r':1, 'x':1} #deal_hand(HAND_SIZE)
    play_hand(hand, word_list)
