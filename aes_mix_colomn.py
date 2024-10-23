


def hex_to_matrix(hex_string):
    """Convert a hex string to a 4x4 matrix."""
    byte_array = [int(hex_string[i:i + 2], 16) for i in range(0, len(hex_string), 2)]
    return [byte_array[i:i + 4] for i in range(0, 16, 4)]

def matrix_to_hex(matrix):
    """Convert a 4x4 matrix back to a hex string."""
    return ''.join(f'{byte:02x}' for row in matrix for byte in row)



def mix_columns(state):
    fixed_matrix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]

    new_state = []
    for col in range(4):
        new_column = []
        for row in range(4):
            val = 0
            for i in range(4):
                val ^= gf_multiply(fixed_matrix[row][i], state[i][col])
            new_column.append(val)
        new_state.append(new_column)
    return new_state


def gf_multiply(a, b):
   p = 0
   for _ in range(8):
      if b & 1:
         p ^= a
      hi_bit_set = a & 0x80
      a <<= 1
      if hi_bit_set:
         a ^= 0x1B  # irreducible polynomial
      b >>= 1
   return p if p < 0x80 else p ^ 0x11B




def mix(hexstring):

    matrix = hex_to_matrix(hexstring)
    print(matrix)
    new_state = mix_columns(matrix)
    return (matrix_to_hex(new_state))

# print(mix("ab40f0c48b7ffce489f1184e35053f2f"))
print(mix("ab8b8935407ff105f0fc183fc4e44e2f"))
