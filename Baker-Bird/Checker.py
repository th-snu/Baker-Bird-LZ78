import sys


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


def read_output(outputfile):
    result = []

    # Write result on output file
    with open(outputfile, mode="r") as f:
        for line in f:
            try:
                xy = list(map(int, line.strip().split()))
            except:
                return None
            if len(xy) != 2:
                return None
            x, y = xy[0], xy[1]
            result.append((x, y))

    return result


def check_result(text, pattern, res):
    # Use naive algorithm to check results
    # Worst time complexity is O(n^2 * m^2), from simple loop

    # Average time complexity is O(n^2)
    # Assuming that probability of one character each from text and pattern matching is 1 / size(alphabet),
    # Each loop to match a part of text to the pattern takes constant time on average
    x_len = len(text[0]) - len(pattern[0]) + 1
    y_len = len(text) - len(pattern) + 1

    x_p_len = len(pattern[0])
    y_p_len = len(pattern)

    checker_res = []

    for x in range(x_len):
        for y in range(y_len):
            for x_p in range(x_p_len):
                match = True
                for y_p in range(y_p_len):
                    if text[x + x_p][y + y_p] != pattern[x_p][y_p]:
                        match = False
                        break
                
                if not match:
                    break
                
                if x_p == x_p_len - 1:
                    checker_res.append((x + x_p, y + y_p))

    for ele in res:
        try:
            checker_res.remove(ele)
        except:
            return False
    
    if len(checker_res) != 0:
        return False
    
    return True


def main(inputfile, outputfile, checker_outputfile):
    pattern = []
    text = []

    text, pattern = read_input(inputfile)
    res = read_output(outputfile)
   
    is_correct = check_result(text, pattern, res) if res is not None else False

    with open(checker_outputfile, mode="w") as f:
        f.write("yes") if is_correct else f.write("no")


if __name__ == "__main__":
    # Get commandline arguments
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]

    checker_outputfile = sys.argv[3]

    main(inputfile, outputfile, checker_outputfile)
