# Problem Set 4C
# Name: Silas Jimmy
# Collaborators: None
# Time Spent: 3hrs

from ps4a import get_permutations

### HELPER CODE ###
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

WORDLIST_FILENAME = 'words.txt'

VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'

class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object
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
        Returns: a COPY of self.valid_words
        '''
        valid_words = self.valid_words[:]
        return valid_words
                
    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)
        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
        lower = [(VOWELS_LOWER[i], v) for i, v in enumerate(vowels_permutation.lower())]
        upper = [(VOWELS_UPPER[i], v) for i, v in enumerate(vowels_permutation.upper())]
        
        return dict(lower + upper)
    
    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary
        Returns: an encrypted version of the message text, based 
        on the dictionary
        '''
        new_message_text = []
        
        for letter in self.message_text:
            if letter in transpose_dict.keys():
                new_message_text.append(transpose_dict.get(letter))
            else:
                new_message_text.append(letter)
                
        return ''.join(new_message_text)
        
class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object
        text (string): the encrypted message text
        '''
        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def decrypt_message(self):
        '''
        Attempts to decrypt the encrypted message
        Returns: the best decrypted message
        '''
        permutations = get_permutations(VOWELS_LOWER)
        max_valid_words = 0
        decrypted_message = self.message_text
        
        for permutation in permutations:
            transpose_dict = self.build_transpose_dict(permutation)
            message = self.apply_transpose(transpose_dict)
            split_message = message.split(sep=' ')
            valid_words = 0
            
            for word in split_message:
                if is_word(self.valid_words, word):
                    valid_words += 1
                    
            if valid_words > max_valid_words:
                max_valid_words = valid_words
                decrypted_message = message
        
        return decrypted_message
    

if __name__ == '__main__':

    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())
