from func.generate_C_L_Q1 import generate_C_L_Q1
from func.generate_t_and_public_seed import generate_t_and_public_seed
from func.H_G_functions import H, G
from func.genenrate_C_L_Q1_Bytes import generate_C_L_Q1_Bytes
from func.BuildAugmentedMatrix import BuildAugmentedMatrix
import math
import os
import numpy as np
from hashlib import shake_128


def generate_salt(length=16):
    # Genera un salt de la longitud especificada (16 bytes por defecto)
    salt = os.urandom(length)
    return salt

import numpy as np
import hashlib

def generate_hash_digest_H(message: bytes, salt: bytes, m: int, r: int):
    """
    Generates the hash digest interpreted as m elements of F2^r, stored as bytes in a 2D array of size m x 1.

    Args:
        message (bytes): The message to be signed.
        salt (bytes): A random 16-byte salt.
        m (int): The number of elements in the hash digest (vector length).
        r (int): The bit length of each element in F2^r (must be <= 8).

    Returns:
        np.ndarray: A 2D numpy array of shape (m, 1), where each element is a byte (uint8) representing an r-bit value.
    """
    if r > 8:
        raise ValueError("Each element must fit within a single byte (r <= 8).")
    
    # Concatenate message, 0x00 byte, and salt
    concatenated_input = message + b'\x00' + salt

    # Initialize SHAKE128
    shake = hashlib.shake_128()
    shake.update(concatenated_input)
    
    # Total number of bits needed (m * r)
    total_bits = m * r
    total_bytes = (total_bits + 7) // 8  # Convert to bytes, rounding up

    # Get the raw hash output as bytes
    hash_output = shake.digest(total_bytes)

    # Create a numpy array to store the results as a 2D array (m x 1)
    elements = np.zeros((m, 1), dtype=np.uint8)  # Each element is a byte (uint8)

    bit_position = 0  # Track the current bit position in the hash output

    for i in range(m):
        # Extract r bits for the current element
        value = 0
        for bit in range(r):
            byte_index = (bit_position + bit) // 8
            bit_index = 7 - ((bit_position + bit) % 8)
            bit_value = (hash_output[byte_index] >> bit_index) & 1
            value = (value << 1) | bit_value  # Shift value and add new bit
        
        # Store the value as a byte (uint8) in the matrix
        elements[i, 0] = value  # Store the r-bit value as a byte
        bit_position += r  # Move to the next r bits

    return elements


def Sign(private_seed, message, m, v, n, r):
    all_bytes_of_T_and_public_seed = H(private_seed, 32 + math.ceil(m / 8) *v)
    T, public_seed = generate_t_and_public_seed(all_bytes_of_T_and_public_seed, m, v)
    C, L, Q1 = generate_C_L_Q1_Bytes(public_seed, m, n, v)
    salt = generate_salt()
    h = generate_hash_digest_H(message, salt, m, r)

    while True:
        v_ = generate_hash_digest_H(message, salt, v, r)
        A = BuildAugmentedMatrix(C, L, Q1, T, h, v_, m, n, r)

private_seed = os.urandom(32)
message = b"Hello, world!"
r = 7
m = 57
v = 197
n = m + v

Sign(private_seed, message, m, v, n, r)

    