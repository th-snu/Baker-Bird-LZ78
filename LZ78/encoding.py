import time
import sys
import os
import LZ78
import Huffman


def load_text(file_name):
    with open(file_name, "r", newline='') as f:
        return f.read()


if __name__ == '__main__':
    input_name = str(sys.argv[1])
    encoded_name = str(sys.argv[2])

    text = load_text(input_name)

    # asterisk is indicator of the end of the text
    text += '*'

    # Start of encoding process
    before_encode = time.time()

    ciphertext = LZ78.encode(text)
    Huffman.save_ciphertext(ciphertext, encoded_name)

    # End of encoding process
    after_encode = time.time()
    print("Encoding Time: {} seconds, Size: {} bytes".format(
        after_encode - before_encode, os.path.getsize(encoded_name)))
