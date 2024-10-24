


# this file is used used for key expansion in AES encryption and decryption.
import aes_supplymenty_meterial  as asm


def sub_bytes(word):
    return [asm.S_BOX[b] for b in word]

def rotate(word):
    return word[1:] + word[:1]

def key_schedule_core(word, iteration):
    word = rotate(word)
    word = sub_bytes(word)
    word[0] ^= asm.R_CON[iteration]  # XOR with round constant
    return word

def key_expansion_base(key):
    key = "".join(key.split(" "))
    """Expand the key into round keys."""
    # Convert the hex key into a list of bytes
    key_bytes = [int(key[i:i+2], 16) for i in range(0, len(key), 2)]

    Nk = 4  # Number of 32-bit words in the key
    Nb = 4  # Number of 32-bit words in a block
    Nr = 10 # Number of rounds for AES-128

    # Initialize the key schedule with the original key
    W = [key_bytes[i:i + 4] for i in range(0, len(key_bytes), 4)]

    # Generate round keys
    for i in range(Nk, Nb * (Nr + 1)):
        temp = W[i - 1]
        if i % Nk == 0:
            temp = key_schedule_core(temp, i // Nk - 1)
        W.append([W[i - Nk][j] ^ temp[j] for j in range(4)])
    round_keys = [''.join(f'{b:02x}' for b in W[i]) for i in range(Nb * (Nr + 1))]
    return round_keys



def key_expansion(key):
    keys = key_expansion_base(key)
    temp = []
    for i in range(0, len(keys), 4):
        temp.append("".join(keys[i:i+4]))
    return temp
