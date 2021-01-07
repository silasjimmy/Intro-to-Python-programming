# Problem Set 4B
# Name: Silas Jimmy
# Collaborators: None
# Time Spent: 3 hrs

import string

def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    Returns: a list of valid words. Words are strings of lowercase letters.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation
    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    Returns: True if word is in word_list, False otherwise
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object
        text (string): the message's text
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words[:]
        return valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.
        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        uppercase_letters = list(string.ascii_uppercase)
        lowercase_letters = list(string.ascii_lowercase)
        max_index = len(uppercase_letters) - shift
        shift_dict = {}
        
        for letter in uppercase_letters:
            letter_index = uppercase_letters.index(letter)
            if letter_index < max_index:
                shift_dict[letter] = uppercase_letters[letter_index + shift]
            else:
                rem = shift - (len(uppercase_letters) - uppercase_letters.index(letter))
                shift_dict[letter] = uppercase_letters[rem]
                
        for letter in lowercase_letters:
            letter_index = lowercase_letters.index(letter)
            if letter_index < max_index:
                shift_dict[letter] = lowercase_letters[letter_index + shift]
            else:
                rem = shift - (len(lowercase_letters) - lowercase_letters.index(letter))
                shift_dict[letter] = lowercase_letters[rem]
                
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift.
        Returns: the message text (string) in which every character is shifted
        down the alphabet by the input shift
        '''
        shift_dict = self.build_shift_dict(shift)
        new_message_text = []
        
        for letter in self.message_text:
            if letter in string.ascii_letters:
                new_message_text.append(shift_dict.get(letter))
            else:
                new_message_text.append(letter)
                
        return ''.join(new_message_text)

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        text (string): the message's text
        shift (integer): the shift associated with this message

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict = self.encryption_dict.copy()
        return encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
        text (string): the message's text
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        best_shift_value = None
        decrypted_message = None
        max_valid_words = 0
        
        for shift_value in range(26):
            message = self.apply_shift(shift_value)
            split_message = message.split(sep=' ')
            valid_words = 0
            
            for word in split_message:
                if is_word(self.valid_words, word):
                    valid_words += 1
                    
            if valid_words > max_valid_words:
                max_valid_words = valid_words
                best_shift_value = 26 - shift_value
                decrypted_message = message
                
        return best_shift_value, decrypted_message

if __name__ == '__main__':

#    # Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#    plaintext.change_shift(5)
#    print('Expected Output: mjqqt')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    # Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('mjqqt, BTWQI !!')
#    print('Expected Output:', (5, 'hello, WORLD !!'))
#    print('Actual Output:', ciphertext.decrypt_message())
    
    # Decrypting the story
    story = get_story_string()
    encrypted_text = CiphertextMessage(story)
    print(encrypted_text.decrypt_message())
