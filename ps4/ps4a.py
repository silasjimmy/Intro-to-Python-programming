# Problem Set 4A
# Name: Silas Jimmy
# Collaborators: None
# Time Spent: Couple of years (Took me sometime to figure out the implementation)

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string
    sequence (string): an arbitrary string to permute. Assume that it is a non-empty string.
    Returns: a list of all permutations of sequence
    '''

    if len(sequence) == 1:
        return [sequence]
    
    sequence_permutations = []
    
    permutated_sequences = get_permutations(sequence[1:])
    
    for ps in permutated_sequences:
        sequence_list = list(ps)
        for i in range(len(sequence)):
            sequence_list_copy = sequence_list[:]
            sequence_list_copy.insert(i, sequence[0])
            sequence_permutations.append(''.join(sequence_list_copy))
    
    return sequence_permutations

if __name__ == '__main__':
    print(get_permutations('abc'))

