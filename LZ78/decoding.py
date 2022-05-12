import time
import sys
import LZ78
import Huffman


def save_text(content, file_name):
    with open(file_name, "w", newline='') as f:
        return f.write(content)


if __name__ == '__main__':
    encoded_name = str(sys.argv[1])
    output_name = str(sys.argv[2])

    # Start of decoding process
    before_decode = time.time()

    ciphertext = Huffman.load_ciphertext(encoded_name)
    text = LZ78.decode(ciphertext)[:-1]

    # End of decoding process
    after_decode = time.time()
    print("Decoding Time: {} seconds".format(
        after_decode - before_decode))

    save_text(text, output_name)
