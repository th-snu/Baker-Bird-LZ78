import heapq
import itertools


def bits_to_bytes(li):
    bytes_li = []
    cnt = 0
    curr = 0
    for val in li:
        if cnt < 8:
            curr *= 2
        else:
            cnt = 0
            bytes_li.append(curr)
            curr = 0
        if val:
            curr += 1
        cnt += 1

    while cnt < 8:
        curr *= 2
        cnt += 1

    bytes_li.append(curr)

    return bytes(bytes_li)


def bytes_to_bits(bytes_li):
    li = []
    for byte in bytes_li:
        bit_li = []
        for i in range(8):
            bit_li.append(byte % 2 == 1)
            byte //= 2

        li.extend(reversed(bit_li))

    return li


def integer_to_bits(val):
    if val == 0:
        return [False]

    res = []
    while val > 0:
        res.append(val % 2 == 1)
        val //= 2
    return res


def encode_integer(val):
    # Use base 3, little endian encoding to encode arbitrary integer
    # 2b'11 indicates end of integer
    if val == 0:
        return [True, True]
    else:
        res = []
        while val != 0:
            remainder = val % 3
            val //= 3
            res.append(remainder % 2 == 1)
            res.append(remainder // 2 == 1)
        res.extend([True, True])

        return res


def encode_integers(li):
    res = []
    for val in li:
        res.append(encode_integer(val))

    res = list(itertools.chain.from_iterable(res))
    return res


def decode_integer(data, offset):
    res = 0
    end_offset = offset

    # Find the end of current integer
    while not data[end_offset] or not data[end_offset + 1]:
        end_offset += 2
    next_offset = end_offset + 2
    end_offset -= 2

    while offset <= end_offset:
        res *= 3
        if data[end_offset] and data[end_offset + 1]:
            break
        res += 2 if data[end_offset + 1] else 0 + 1 if data[end_offset] else 0
        end_offset -= 2

    return res, next_offset


def decode_integers(data, offset, count):
    res = []
    for i in range(count):
        val, offset = decode_integer(data, offset)
        res.append(val)

    return res


def encode_tree(tree):
    if tree[1] is None:
        res = [False]
        chars = tree[0]
        return chars, res

    else:
        res = [True]
        l_chars, l_res = encode_tree(tree[0])
        r_chars, r_res = encode_tree(tree[1])
        return l_chars + r_chars, res + l_res + r_res


def code_dictionary_as_bits(tree):
    # Encode huffman tree structure as a bitstream
    chars, tree = encode_tree(tree)
    char_size = len(chars)

    # Write length of characters, and characters
    res = bytes_to_bits(bytes([char_size]))
    res.extend(bytes_to_bits(bytes(list(map(ord, chars)))))

    # Write the bitstream representation of tree structure
    res.extend(tree)

    return res


def reconstruct_tree(tree_bits, chars, offset):
    # Reconstruct tree from bitstream
    flag = tree_bits[offset]
    offset += 1
    if not flag:
        return (chars[0], None), offset, chars[1:]
    else:
        l_node, offset, chars = reconstruct_tree(tree_bits, chars, offset)
        r_node, offset, chars = reconstruct_tree(tree_bits, chars, offset)
        return (l_node, r_node), offset, chars


def load_dictionary_from_bits(data):
    # Load number of used characters, and characters stored in tree
    char_size = bits_to_bytes(data[:8])[0]
    offset = 8+8*char_size
    chars = list(map(chr, bits_to_bytes(data[8:offset])))

    # Build huffman tree
    tree, offset, _ = reconstruct_tree(data, chars, offset)

    return tree, offset


def decode_ciphertext(buffer):
    # Read byte buffer and reconstruct pair of numbers and alphabets
    data = bytes_to_bits(buffer)
    tree, offset = load_dictionary_from_bits(data)
    curr = tree
    text = ''

    # Decode characters using huffman code tree
    while True:
        bit = data[offset]
        offset += 1
        if bit:
            curr = curr[1]
        else:
            curr = curr[0]

        if curr[1] is None:
            text += curr[0]
            if curr[0] != '*':
                curr = tree
            else:
                break

    count = len(text)

    # Decode integers
    ints = decode_integers(data, offset, count)

    res = []
    for i in range(count):
        res.append((ints[i], text[i]))

    return res


def load_ciphertext(file_name):
    with open(file_name, "rb") as f:
        buffer = f.read()
    return decode_ciphertext(buffer)


def get_code_from_tree(tree, curr, code_book):
    # Append boolean value per edge
    # Reconstruct codes from tree, and store it to code_book
    if tree[1] is None:
        code_book[tree[0]] = curr
    else:
        get_code_from_tree(tree[0], curr + [False], code_book)
        get_code_from_tree(tree[1], curr + [True], code_book)


def encode_ciphertext(ciphertext):
    chars = {}
    vals = []
    for _, char in ciphertext:
        if char in chars:
            chars[char] += 1
        else:
            chars[char] = 1

    # Decide at most how many characters huffman will use
    chars_dict = chars.items()
    heap_items = [(v, i, (k, None)) for i, (k, v) in enumerate(chars_dict)]

    index = len(chars_dict)

    heapq.heapify(heap_items)
    while len(heap_items) >= 2:
        first = heapq.heappop(heap_items)
        second = heapq.heappop(heap_items)

        heapq.heappush(heap_items, (first[0] + second[0], index, (first[2], second[2])))
        index += 1

    _, _, tree = heapq.heappop(heap_items)

    # Encode tree with bits
    res = code_dictionary_as_bits(tree)
    code_book = {}
    get_code_from_tree(tree, [], code_book)

    # Encode chars in ciphertext, ending with separator
    for val, char in ciphertext:
        res.extend(code_book[char])
        vals.append(val)

    # Encode integers in ciphertext
    encoded_vals = encode_integers(vals)
    res.extend(encoded_vals)

    # First byte represents mode of integer encoding
    return bits_to_bytes(res)


def save_ciphertext(ciphertext, file_name):
    # Check how many times characters are used
    byte_res = encode_ciphertext(ciphertext)
    with open(file_name, "wb") as f:
        f.write(byte_res)
