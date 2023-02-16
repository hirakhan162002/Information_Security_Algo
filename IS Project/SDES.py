"""
    Submitted by:
            BSEF20M010      Mehak Nadeem
            BSEF20M020      Hira Asghar
            
"""

global p8_table, p10_table, p4_table, IP, IP_inv, expansion, s0, s1
p8_table = [6, 3, 7, 4, 8, 5, 10, 9]
p10_table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
p4_table = [2, 4, 3, 1]
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]
expansion = [4, 1, 2, 3, 2, 3, 4, 1]
s0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
s1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

def apply_table(inp, table):
    res = ""
    for i in table:
        res += inp[i - 1]
    return res


def left_shift(data):
    return data[1:] + data[0]


def xor(a, b):
    res = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            res += "0"
        else:
            res += "1"
    return res


def apply_sbox(s, data):
    row = int("0b" + data[0] + data[-1], 2)
    col = int("0b" + data[1:3], 2)
    return bin(s[row][col])[2:]


def function(expansion, s0, s1, key, message):
    left = message[:4]
    right = message[4:]
    temp = apply_table(right, expansion)
    temp = xor(temp, key)
    l = apply_sbox(s0, temp[:4])
    r = apply_sbox(s1, temp[4:])
    l = "0" * (2 - len(l)) + l
    r = "0" * (2 - len(r)) + r
    temp = apply_table(l + r, p4_table)
    temp = xor(left, temp)
    return temp + right

def key_generation(key):
    temp = apply_table(key, p10_table)
    left = temp[:5]
    right = temp[5:]
    left = left_shift(left)
    right = left_shift(right)
    key1 = apply_table(left + right, p8_table)
    left = left_shift(left)
    right = left_shift(right)
    left = left_shift(left)
    right = left_shift(right)
    key2 = apply_table(left + right, p8_table)
    return (key1,key2)

def encryption(message,key):
    key1, key2 = key_generation(key)
    temp = apply_table(message, IP)
    temp = function(expansion, s0, s1, key1, temp)
    temp = temp[4:] + temp[:4]
    temp = function(expansion, s0, s1, key2, temp)
    CT = apply_table(temp, IP_inv)
    return CT

def decryption(CT, key):
    key1, key2 = key_generation(key)
    temp = apply_table(CT, IP)
    temp = function(expansion, s0, s1, key2, temp)
    temp = temp[4:] + temp[:4]
    temp = function(expansion, s0, s1, key1, temp)
    PT = apply_table(temp, IP_inv)
    return PT

def divide_into_8_blocks(text):
    # Initialize an empty list to store the blocks
    blocks = []
    # Split the string into 8-character blocks
    if len(text) % 8 != 0:
        padding = 8 - (len(text) % 8)
        j = 0
        while j < padding:
            text = text + '0'
            j = j + 1
    for i in range(0, len(text), 8):
        blocks.append(text[i:i+8])
    return blocks

if __name__ == "__main__":
    ed = input('Enter E for Encrypt, or D for Decrypt: ').upper()
    if ed == 'E':
        key = input("Enter 10 bit key: ")
        message = input("Enter message: ")
        if len(message) == 8:
            cipher = encryption(message,key)
            print("Cipher text is: ",cipher)
        elif len(message) > 8:
            msg_blocks = divide_into_8_blocks(message)
            cipher_result = ""
            for block in msg_blocks:
                cipher_result = cipher_result + " " + encryption(block, key)
            print("Cipher text is:", cipher_result)
        else:
            print("\nMessage must be 8 bits long.")

    elif ed == 'D':
        key = input("Enter 10 bit key: ")
        ciphertext = input("Enter cipher text: ")
        if len(ciphertext) == 8:
            plaintext = decryption(ciphertext,key)
            print("Plain text is: ",plaintext)
        elif len(ciphertext) > 8:
            msg_blocks = divide_into_8_blocks(ciphertext)
            plain_result = ""
            for block in msg_blocks:
                plain_result = plain_result + " " + decryption(block, key)
            print("Plain text is:", plain_result)
        else:
            print("\nCipher text must be 8 bits long.")
    else:
        print('Error in input - try again.')

