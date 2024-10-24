
def row_mazor_to_column_mazor(matrix):

    return [list(row) for row in zip(*matrix)]



# def hex_to_matrix(hex_string):
#     """Convert a hex string to a 4x4 matrix."""
#     byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
#     return [byte_array[i:i + 4] for i in range(0, 16, 4)]

# def matrix_to_hex(matrix):
#     """Convert a 4x4 matrix back to a hex string."""
#     return ''.join(f'{byte:02x}' for row in matrix for byte in row)



# def mix_columns(state):
#     fixed_matrix = [
#         [0x02, 0x03, 0x01, 0x01],
#         [0x01, 0x02, 0x03, 0x01],
#         [0x01, 0x01, 0x02, 0x03],
#         [0x03, 0x01, 0x01, 0x02]
#     ]

#     new_state = []
#     for col in range(4):
#         new_column = []
#         for row in range(4):
#             val = 0
#             for i in range(4):
#                 val ^= gf_multiply(fixed_matrix[row][i], state[i][col])
#             new_column.append(val)
#         new_state.append(new_column)
#     return new_state


# def gf_multiply(a, b):
#    p = 0
#    for _ in range(8):
#       if b & 1:
#          p ^= a
#       hi_bit_set = a & 0x80
#       a <<= 1
#       if hi_bit_set:
#          a ^= 0x1B  # irreducible polynomial
#       b >>= 1
#    return p if p < 0x80 else p ^ 0x11B




# def mix(hexstring):

#     matrix = hex_to_matrix(hexstring)
#     matrix = row_mazor_to_column_mazor(matrix)
#     print(matrix)
#     new_state = mix_columns(matrix)
#     return (matrix_to_hex(new_state))

# print(mix("ab40f0c48b7ffce489f1184e35053f2f"))
# # print(mix("ab8b8935407ff105f0fc183fc4e44e2f"))


def row_major_to_column_major(matrix):
    """Convert a 4x4 matrix from row-major to column-major order."""
    return [list(row) for row in zip(*matrix)]

def hex_to_matrix(hex_string):
    """Convert a hex string to a 4x4 matrix."""
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    return [byte_array[i:i + 4] for i in range(0, 16, 4)]

def matrix_to_hex(matrix):
    """Convert a 4x4 matrix back to a hex string."""
    return ''.join(f'{byte:02x}' for row in matrix for byte in row)

def mix_columns(state):
    """Perform the MixColumns operation on the state matrix."""
    fixed_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    new_state = [[0] * 4 for _ in range(4)]  # Initialize new state matrix

    for col in range(4):
        for row in range(4):
            val = 0
            for i in range(4):
                val ^= gf_multiply(fixed_matrix[row][i], state[i][col])
            new_state[row][col] = val
    return new_state

def gf_multiply(a, b):
    """Multiply two bytes in the Galois Field GF(2^8)."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        high_bit = a & 0x80  # Check if the high bit is set
        a <<= 1  # Multiply by 2
        if high_bit:
            a ^= 0x1b  # Reduce modulo x^8 + x^4 + x^3 + x + 1
        b >>= 1  # Divide by 2
    return p % 256  # Return the result as a byte


def mix(hexstring):

    matrix = hex_to_matrix(hexstring)
    matrix = row_mazor_to_column_mazor(matrix)

    # print(matrix)
    new_state = mix_columns(matrix)
    new_state = row_mazor_to_column_mazor(new_state)

    return (matrix_to_hex(new_state))

# print(mix("ab40f0c48b7ffce489f1184e35053f2f"))
# # print(mix("ab8b8935407ff105f0fc183fc4e44e2f"))
