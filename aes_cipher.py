import aes_supplymenty_meterial as asm
import aes_key_expantion as ake

def sub_bytes(hex_string):
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    substituted = [asm.S_BOX[b] for b in byte_array]
    result = ''.join(f'{byte:02x}' for byte in substituted)
    return result



def hex_to_matrix(hex_string):
    """Convert a hex string to a 4x4 matrix."""
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    return [byte_array[i:i + 4] for i in range(0, 16, 4)]

def matrix_to_hex(matrix):
    """Convert a 4x4 matrix back to a hex string."""
    return ''.join(f'{byte:02x}' for row in matrix for byte in row)




def row_mazor_to_column_mazor(matrix):

    return [list(row) for row in zip(*matrix)]



def shift_rows(matrix):
    # print(matrix)
    """Perform the ShiftRows transformation."""
    matrix = row_mazor_to_column_mazor(matrix)
    matrix[1] = matrix[1][1:] + matrix[1][:1]  # Shift row 1 left by 1
    matrix[2] = matrix[2][2:] + matrix[2][:2]  # Shift row 2 left by 2
    matrix[3] = matrix[3][3:] + matrix[3][:3]  # Shift row 3 left by 3
    # matrix = row_mazor_to_column_mazor(matrix)

    # print(matrix)
    return matrix


def shift_rows_hex(hex_string):
    """ShiftRows transformation on a hex string."""
    matrix = hex_to_matrix(hex_string)
    matrix = shift_rows(matrix)
    return matrix_to_hex(matrix)


def multiply(x, y):
    """Multiply two bytes in GF(2^8)."""
    p = 0
    for _ in range(8):
        if (y & 1) != 0:
            p ^= x
        high_bit = x & 0x80
        x <<= 1
        if high_bit:
            x ^= 0x1b  # x^8 + x^4 + x^3 + x + 1
        y >>= 1
    return p

def mix_columns(matrix):
    """Perform the MixColumns transformation."""
    for i in range(4):
        # Store the original column
        a = [matrix[j][i] for j in range(4)]

        # Mix the column
        matrix[0][i] = multiply(a[0], 2) ^ multiply(a[1], 3) ^ a[2] ^ a[3]
        matrix[1][i] = a[0] ^ multiply(a[1], 2) ^ multiply(a[2], 3) ^ a[3]
        matrix[2][i] = a[0] ^ a[1] ^ multiply(a[2], 2) ^ multiply(a[3], 3)
        matrix[3][i] = multiply(a[0], 3) ^ a[1] ^ a[2] ^ multiply(a[3], 2)

def mix_columns_hex(hex_string):
    """MixColumns transformation on a hex string."""
    matrix = hex_to_matrix(hex_string)
    mix_columns(matrix)
    return matrix_to_hex(matrix)


def hex_to_bytes(hex_string):
    """Convert a hex string to a byte array."""
    return [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]

def bytes_to_hex(byte_array):
    """Convert a byte array back to a hex string."""
    return ''.join(f'{byte:02x}' for byte in byte_array)




def add_round_key(state_hex, round_key_hex):
    """Perform the AddRoundKey transformation (XOR operation)."""
    # Convert hex strings to byte arrays
    state = hex_to_bytes(state_hex)
    round_key = hex_to_bytes(round_key_hex)

    # Perform XOR operation
    output_state = [state[i] ^ round_key[i] for i in range(16)]  # 16 bytes for AES

    # Convert output state back to hex string
    return bytes_to_hex(output_state)



def aes( key = "0f 15 71 c9 47 d9 e8 59 0c b7 ad d6 af 7f 67 98", plaintext = "01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10")-> str:
    key = key.replace(" ", "")
    plaintext = plaintext.replace(" ", "")
    round_keys = ake.key_expansion(key)
    state = add_round_key(plaintext, round_keys[0])
    print(state)
    for i in range(1, 10):
        state = sub_bytes(state)
        print("After Sub Byte: ", state, end="\t")
        state = shift_rows_hex(state)
        print("After Shift Row",state, end="\t")
        state = mix_columns_hex(state)
        print( "After Mix Column",state , end="\t")
        state = add_round_key(state, round_keys[i])
        print(" After Add Roubd key",state)

    state = sub_bytes(state)
    state = shift_rows_hex(state)
    state = add_round_key(state, round_keys[10])
    print(state)
    return state




aes()
    # return ""
