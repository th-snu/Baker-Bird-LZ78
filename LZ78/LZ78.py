def encode(text):
    # Convert text to pair of numbers and characters

    # States are trie, represented as a list
    # Each state holds list of edges, represented with dictionary
    # Dictionary uses alphabet as a key, and a pair of destination state
    states = [{}]
    result = []

    curr_state = 0
    for index in range(len(text)):
        curr_char = text[index]

        if curr_char not in states[curr_state]:
            states[curr_state][curr_char] = len(states)
            states.append({})
            result.append((curr_state, curr_char))
            curr_state = 0
        else:
            curr_state = states[curr_state][curr_char]

    return result


def decode(ciphertext):
    phrases = ['']
    for pointer, char in ciphertext:
        phrases.append(phrases[pointer] + str(char))

    return ''.join(phrases)
