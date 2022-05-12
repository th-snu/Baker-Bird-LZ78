import sys


def char_to_idx(char):
    if ord('a') <= ord(char) <= ord('z'):
        return ord(char) - ord('a')
    elif ord('A') <= ord(char) <= ord('Z'):
        return ord(char) - ord('A') + 26
    else: return ord(char) - ord('0') + 52


def precompute_aho_corasick(pattern):
    # State will be added one by one
    # List is enough for implementing these functions
    empty_row = [0] * 62

    def get_new_row():
        return empty_row.copy()

    # "Functions" are implemented as lists
    transition_f = [get_new_row()]
    failure_f = [0]
    output_f = [[]]

    # Variable to use for building failure function
    states_in_depth = [[] for _ in range(max(list(map(len, pattern))) + 1)]
    states_in_depth[0].append(0)
    link_info = [0]

    # Store unique rows as keywords, and mapping from rows to keywords
    # Keywords correspond to an alphabet for KMP algorithm
    keywords = []
    row_map = []

    # With double for loop, complexity ofthist is O(m^2)
    for word in pattern:
        # Read each line to build tree
        state = 0
        is_already_key = True
        depth = 0

        for char in word:
            # Follow transition table to find corresponding state
            dest = transition_f[state][char_to_idx(char)]
            depth += 1

            if dest != 0:
                state = dest

            else:
                # Create new state if corresponding one doesn't exist
                transition_f.append(get_new_row())
                output_f.append([])
                failure_f.append(0)
                link_info.append((state, char_to_idx(char)))

                transition_f[state][char_to_idx(char)] = len(transition_f) - 1
                state = len(transition_f) - 1
                is_already_key = False

                states_in_depth[depth].append(len(transition_f) - 1)

        # Add keywords and update mapping from rows to keywords
        if not is_already_key:
            keywords.append(word)

            # Current state is the last state of the pattern
            output_f[state].append(len(keywords) - 1)

        row_map.append(output_f[state][0])

    # Compute failure function and update output function
    for i, states in enumerate(states_in_depth):
        # For depth upto 1, failure function value is 0
        if i <= 1:
            continue
        for state in states:
            prev_state, char = link_info[state]
            
            while prev_state != 0:
                r_prime = failure_f[prev_state]
                r = transition_f[r_prime][char]

                if r != 0:
                    failure_f[state] = r
                    output_f[state].extend(output_f[r])
                    break

                else:
                    if r_prime == 0:
                        break
                    else:
                        prev_state = r_prime

    # Remove duplicate from output function, worst case
    for i in range(len(output_f)):
        output_f[i] = list(set(output_f[i]))

    return failure_f, transition_f, output_f, keywords, row_map


def get_kmp_fail_f(row_map):
    # row_map conrresponds to pattern, keywords corresponds to alphabets
    f = [-1] * len(row_map)
    k = -1

    # k is last index of current match
    for q in range(1, len(row_map)):
        while k >= 0 and row_map[k + 1] != row_map[q]:
            k = f[k]
        
        if row_map[k + 1] == row_map[q]:
            k += 1
        
        f[q] = k

    return f

def aho_corasick(row, failure_f, transition_f, output_f):
    s = 0
    i = 0
    r = [[] for _ in range(len(row))]

    while i < len(row):
        match = transition_f[s][char_to_idx(row[i])]
        if match != 0:
            s = match
            r[i] = output_f[s]
            i += 1
        else:
            if s == 0:
                i += 1
            else:
                s = failure_f[s]

    return r


def baker_bird(text, pattern):
    # Pre-compute data structure for Aho-Corasick
    # During the process, also find unique rows in pattern
    failure_f, transition_f, output_f, keywords, row_map = precompute_aho_corasick(pattern)

    # Pre-compute fail function for KMP
    f = get_kmp_fail_f(row_map)
    kmp_state = [-1] * len(text[0])

    result = []
    invalid_char = len(keywords)

    for y, row in enumerate(text):
        # Run Aho-Corasick per row
        r = aho_corasick(row, failure_f, transition_f, output_f)

        # Case of multiple output doesn't happen since all patterns have the same length and are unique
        # So for baker bird result will be one dimensional array with length of a row
        r = list(map(lambda x: x[0] if len(x) > 0 else invalid_char, r))

        # Run n way KMP
        for col in range(len(row)):
            q = kmp_state[col]
            while q >= 0 and row_map[q + 1] != r[col]:
                q = f[q]
            if row_map[q + 1] == r[col]:
                q += 1
            if q == len(pattern) - 1:
                result.append((y, col))
                q = f[q]

            kmp_state[col] = q

    return result


def read_input(inputfile):
    pattern = []
    text = []

    # Read input file and parse it
    with open(inputfile, mode="r") as f:
        line = f.readline().strip()
        mn = list(map(int, line.split()))
        m, n = mn[0], mn[1]

        # Read pattern
        for _ in range(m):
            line = f.readline().strip()
            pattern.append(line)
        pattern = list(map(list, pattern))

        # Read text
        for _ in range(n):
            line = f.readline().strip()
            text.append(line)
        text = list(map(list, text))

    return text, pattern


def write_output(outputfile, result):
    # Write result on output file
    with open(outputfile, mode="w") as f:
        for i, occur in enumerate(result):
            f.write("{} {}".format(occur[0], occur[1]))
            if i != len(result) - 1:
                f.write("\n")


def main(inputfile, outputfile):
    text, pattern = read_input(inputfile)
    result = baker_bird(text, pattern)
    write_output(outputfile, result)


if __name__ == "__main__":
    # Get commandline arguments
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    main(inputfile, outputfile)
