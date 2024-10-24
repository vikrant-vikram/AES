# Thjs is the main file to performm AES
# Run this file to see the full output of the AES encryption














#inport supplmenty meterial
from librosa import chirp
import aes_supplymenty_meterial as asm
#impprt key expantion
import aes_key_expantion as ake
# import mix coulumns
import aes_mix_colomn


# This funcrtion takes hex strinfn and return the sub byte of the hex string
def sub_bytes(hex_string):
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    substituted = [asm.S_BOX[b] for b in byte_array]
    result = ''.join(f'{byte:02x}' for byte in substituted)
    return result


# this function takes hex string and returns matrix
def hex_to_matrix(hex_string):
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    return [byte_array[i:i + 4] for i in range(0, 16, 4)]

#this function takes matrix and return hex string
def matrix_to_hex(matrix):
    return ''.join(f'{byte:02x}' for row in matrix for byte in row)



# this funcrion convert row mazor to column mazor
def row_mazor_to_column_mazor(matrix):

    return [list(row) for row in zip(*matrix)]


#this function performs shift row functionality of AES
def shift_rows(matrix):
    # print(matrix)
    matrix = row_mazor_to_column_mazor(matrix)
    matrix[1] = matrix[1][1:] + matrix[1][:1]  # Shift row 1 left by 1
    matrix[2] = matrix[2][2:] + matrix[2][:2]  # Shift row 2 left by 2
    matrix[3] = matrix[3][3:] + matrix[3][:3]  # Shift row 3 left by 3
    # matrix = row_mazor_to_column_mazor(matrix)

    # print(matrix)
    return matrix


def shift_rows_hex(hex_string):
    matrix = hex_to_matrix(hex_string)
    matrix = shift_rows(matrix)
    matrix = row_mazor_to_column_mazor(matrix)
    return matrix_to_hex(matrix)

 # x^8 + x^4 + x^3 + x + 1
def multiply(x, y):
    p = 0
    for _ in range(8):
        if (y & 1) != 0:
            p ^= x
        high_bit = x & 0x80
        x <<= 1
        if high_bit:
            x ^= 0x1b
        y >>= 1
    return p

# this function performs mix column functionality of AES
def mix_columns(matrix):
    for i in range(4):
        a = [matrix[j][i] for j in range(4)]
        matrix[0][i] = multiply(a[0], 2) ^ multiply(a[1], 3) ^ a[2] ^ a[3]
        matrix[1][i] = a[0] ^ multiply(a[1], 2) ^ multiply(a[2], 3) ^ a[3]
        matrix[2][i] = a[0] ^ a[1] ^ multiply(a[2], 2) ^ multiply(a[3], 3)
        matrix[3][i] = multiply(a[0], 3) ^ a[1] ^ a[2] ^ multiply(a[3], 2)

def mix_columns_hex(hex_string):
    matrix = hex_to_matrix(hex_string)
    mix_columns(matrix)
    return matrix_to_hex(matrix)

# this function rake hex string and returns byte of hex
def hex_to_bytes(hex_string):
    return [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
# this function byte array and return hex string
def bytes_to_hex(byte_array):
    return ''.join(f'{byte:02x}' for byte in byte_array)




def add_round_key(state_hex, round_key_hex):
    # Convert hex strings to byte arrays
    state = hex_to_bytes(state_hex)
    round_key = hex_to_bytes(round_key_hex)
    # Perform XOR operation
    output_state = [state[i] ^ round_key[i] for i in range(16)]  # 16 bytes for AES
    # Convert output state back to hex string
    return bytes_to_hex(output_state)


printer = []

def print_formate(state):
    # print(state, end="\t")
    state = hex_to_matrix(state)
    state = row_mazor_to_column_mazor(state)
    return ' '.join(f'{byte:02x}' for row in state for byte in row)

# this Function is just for printing the output in required tabular formate
def main_printer(printer):
    print("start of round\t subByte\t ShiftRow\t MixColumn\t AddRoundKey\t")
    print("--------------\t -------\t --------\t ---------\t ------------\t")
    m = []
    for i in printer:
        temp = []
        for j in i:
            # temp = []
            temp.append(print_formate(j))
        m.append(temp)
    for i in m:
        for k in range(0, 16, 4):
            for j in i:
                # temp = i[j]
                temp = j.split(" ")
                # for k in range(0, len(temp), 4):
                print(temp[k], temp[k+1], temp[k+2], temp[k+3], end="\t")
            print()
        print()

            # print(i[j])
        print()

def aes( key = "0f 15 71 c9 47 d9 e8 59 0c b7 ad d6 af 7f 67 98", plaintext = "01 23 45 67 89 ab cd ef fe dc ba 98 76 54 32 10")-> str:
    key = key.replace(" ", "")
    plaintext = plaintext.replace(" ", "")
    round_keys = ake.key_expansion(key)
    state = add_round_key(plaintext, round_keys[0])
    temp = []
    temp.append(state)
    # print(state)
    for i in range(1, 10):

        state = sub_bytes(state)
        # print("After Sub Byte: ", state, end="\t")
        temp.append(state)

        state = shift_rows_hex(state)
        # print("After Shift Row",state, end="\t")
        temp.append(state)

        state = aes_mix_colomn.mix(state)
        # print( "After Mix Column",state , end="\t")
        temp.append(state)


        state = add_round_key(state, round_keys[i])
        # print(" After Add Roubd key",state)
        # temp.append(state)
        temp.append(round_keys[i])
        printer.append(temp)

        temp = []
        temp.append(state)
    print()

    main_printer(printer)
    state = sub_bytes(state)
    state = shift_rows_hex(state)
    state = add_round_key(state, round_keys[10])
    # print(state)
    return state




if __name__ == "__main__":
    # print("\033[96m")
    print("-------------------------------------------------[ADVANCED ENCRYPTION STANDARD (AES)]--------------------------------------")
    key = input("Enter the Key: ")
    plaintext = input("Enter the Plain Text: ")
    cipher = ""
    if key and plaintext:
        cipher = aes(key, plaintext)
    else:
        cipher = aes()

    print("Cipher Text for Given Input is : ", cipher)
    print("---------------------------------------------------------------------------------------")
        # return ""
