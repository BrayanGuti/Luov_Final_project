import hashlib
import numpy as np

def G(seed, counter, output_length):
    """
    Function G: Generates pseudorandom bytes using SHAKE256 from a given seed and counter.
    
    Args:
    - seed (bytes): Public seed.
    - counter (int): Counter for distinct calls.
    - output_length (int): Number of bytes to output.
    
    Returns:
    - bytes: Pseudorandomly generated bytes of specified output length.
    """
    # Concatenate seed with counter byte and hash using SHAKE256 for extensible output
    shake = hashlib.shake_256()
    shake.update(seed + counter.to_bytes(1, 'big'))
    return shake.digest(output_length)

def generate_C_L_Q1(public_seed, m, n, v):
    """
    Generates the matrices C, L, Q1 as described in the specifications.

    Args:
    - public_seed (bytes): Seed for random generation.
    - m (int): Number of rows in C, L, Q1.
    - n (int): Number of columns in L.
    - v (int): Parameter defining dimensions of Q1.

    Returns:
    - tuple: (C, L, Q1), numpy arrays with bits (0 or 1).
    """
    q1_size = (v * (v + 1)) // 2 + (v * m)  # Total columns in Q1
    output_len = 2 * (1 + n + q1_size)  # Total bytes per block
    
    # Initialize matrices as numpy arrays of bits (0, 1)
    C = np.zeros((m, 1), dtype=np.uint8)
    L = np.zeros((m, n), dtype=np.uint8)
    Q1 = np.zeros((m, q1_size), dtype=np.uint8)
    
    # Process rows in blocks of 16
    for block in range((m + 15) // 16):  # Number of blocks (ceiling of m/16)
        # Generate pseudorandom bytes for the current block
        output = G(public_seed, block, output_len)

        index = 0  # Pointer to current position in output
        
        # Process up to 16 rows in the current block
        for row in range(16):
            row_index = block * 16 + row
            if row_index >= m:
                break  # Stop if we've processed all rows (m is not divisible by 16)
            
            # Fill C (1 bit per row, stored in 16 bits)
            C[row_index, 0] = int.from_bytes(output[index:index+2], 'big') & 1  # Extract the least significant bit
            index += 2  # Move by 2 bytes (16 bits)
            
            # Fill L (n bits per row)
            for col in range(n):
                L[row_index, col] = (int.from_bytes(output[index:index+2], 'big') >> (15 - col % 16)) & 1
                index += 2 if (col + 1) % 16 == 0 else 0  # Move every 16 columns by 2 bytes
            
            # Fill Q1 (q1_size bits per row)
            for col in range(q1_size):
                Q1[row_index, col] = (int.from_bytes(output[index:index+2], 'big') >> (15 - col % 16)) & 1
                index += 2 if (col + 1) % 16 == 0 else 0  # Move every 16 columns by 2 bytes

    
    return C, L, Q1
