import numpy as np
import hashlib
from func.generate_C_L_Q1 import generate_C_L_Q1

def generate_hash_digest_H(message: bytes, salt: bytes, m: int, r: int):
    """
    Generates the hash digest interpreted as m elements of F2^r, stored as r-bit integers in a 2D array of size m x 1.

    Args:
        message (bytes): The message to be signed.
        salt (bytes): A random 16-byte salt.
        m (int): The number of elements in the hash digest (vector length).
        r (int): The bit length of each element in F2^r (must be <= 8).

    Returns:
        np.ndarray: A 2D numpy array of shape (m, 1), where each element is an integer representing an r-bit value.
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
    elements = np.zeros((m, 1), dtype=np.uint8)  # Each element will hold r bits, treated as uint8

    bit_position = 0  # Track the current bit position in the hash output

    for i in range(m):
        # Extract r bits for the current element
        value = 0
        for bit in range(r):
            byte_index = (bit_position + bit) // 8
            bit_index = 7 - ((bit_position + bit) % 8)
            bit_value = (hash_output[byte_index] >> bit_index) & 1
            value = (value << 1) | bit_value  # Shift value and add new bit
        
        # Store the r-bit value in the matrix
        elements[i, 0] = value  # Store the r-bit value as a uint8
        
        # Increment the bit_position by r to move to the next r bits
        bit_position += r  

    return elements

def EvaluatePublicMap(public_seed, Q2, s, m, n, v):
    # Generar C, L y Q1 basados en el public_seed
    C, L, Q1 = generate_C_L_Q1(public_seed, m, n, v)

    # Concatenar Q1 y Q2 según el pseudocódigo
    Q = np.hstack((Q1, Q2))  # Unir Q1 y Q2 horizontalmente

    # Inicializar el vector de salida e con la parte constante y lineal
    e = np.copy(C) + np.dot(L, s)

    column = 0
    # Evaluar la parte cuadrática en las variables del mapa público
    for i in range(n):
        for j in range(i, n):
            for k in range(m):
                e[k] += Q[k, column] * s[i] * s[j]
            column += 1

    # Retornar el resultado
    return e


def verify(public_seed, Q2, message, s, salt, m, r, v, n):
    h = generate_hash_digest_H(message, salt, m, r)
    e = EvaluatePublicMap(public_seed, Q2, s, m, n, v)

    if e == h:
        return True
    else:
        return False
    
