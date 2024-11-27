import numpy as np
import hashlib
from Crypto.Hash import SHAKE256
from func.FindQ2 import findQ2
from func.H_G_functions import H, G
from func.generate_C_L_Q1 import generate_C_L_Q1
from func.generate_t_and_public_seed import generate_t_and_public_seed
import math


def InitializeAndAbsorb(seed):
    sponge = SHAKE256.new()
    sponge.update(seed)
    return sponge

def create_random_private_seed():
    shake = SHAKE256.new()
    return shake.read(32)

def bytes_to_bits(byte_array):
    return np.unpackbits(np.frombuffer(byte_array, dtype=np.uint8))

def SqueezePublicMap(public_sponge, m, v, n):
    # Leer y convertir los bytes de C a bits
    C_bytes = public_sponge.read(m)
    C = bytes_to_bits(C_bytes).reshape((m, 8))[:, :1]  # Mantener la dimensión (m, 1)

    # Leer y convertir los bytes de L a bits
    L_bytes = public_sponge.read(m * n)
    L = bytes_to_bits(L_bytes).reshape((m, n * 8))[:, :n]  # Mantener la dimensión (m, n)

    # Calcular el tamaño esperado para Q1 basado en los valores de m y v
    q1_size = (v * (v + 1)) // 2 + (v * m)

    # Leer y convertir los bytes de Q1 a bits
    Q1_bytes = public_sponge.read(q1_size * m)
    Q1 = bytes_to_bits(Q1_bytes).reshape((m, q1_size * 8))[:, :q1_size]  # Mantener la dimensión (m, q1_size)

    return C, L, Q1

# def encodePublicKey(public_seed, Q2):
def encode_public_key(Q2: np.ndarray, public_seed: bytes) -> bytes:
    """
    Codifica la clave pública según el esquema LUOV descrito.
    
    Parámetros:
        Q2 (np.ndarray): Matriz binaria de dimensiones m x (m * (m + 1)) / 2.
        public_seed (bytes): Cadena de bytes de longitud 32.
    
    Retorno:
        bytes: Clave pública codificada.
    """
    # Verificar que Q2 contiene solo entradas binarias
    if not np.all((Q2 == 0) | (Q2 == 1)):
        raise ValueError("Q2 debe ser una matriz binaria.")

    # Concatenar las columnas de Q2 en un vector de bits
    bit_sequence = Q2.flatten(order='F')  # 'F' para recorrer las columnas
    
    # Asegurarse de que la longitud sea divisible por 8 rellenando con ceros al final
    padding_length = (8 - len(bit_sequence) % 8) % 8
    padded_bit_sequence = np.append(bit_sequence, [0] * padding_length)
    
    # Convertir la secuencia de bits en bytes
    byte_array = np.packbits(padded_bit_sequence.astype(np.uint8))
    
    # Combinar public_seed con la representación en bytes de Q2
    encoded_public_key = public_seed + bytes(byte_array)
    
    return encoded_public_key


def KeyGen(m, v, n):
    # Paso 1: Crear la semilla privada aleatoria
    private_seed = create_random_private_seed()  

    # paso 2 Usar la semilla privada con la funcion H para luego obtner T y la public seed
    all_bytes_of_T_and_public_seed = H(private_seed, 32 + math.ceil(m / 8) *v)
    T, public_seed = generate_t_and_public_seed(all_bytes_of_T_and_public_seed, m, v)
    print(public_seed)

    # Paso 6: Obtener el mapa público
    C, L, Q1 = generate_C_L_Q1(public_seed, m, n, v)

    # Paso 7: Llamar a la función FindQ2 (dejada sin implementar)
    Q2 = findQ2(Q1, T, m, v)
    
    public_key = encode_public_key(Q2, public_seed)
    private_key = private_seed
    # Paso 8: Devolver la clave pública (public_seed) y Q2

    return public_key, private_key


# public_seed, Q2, private_seed = KeyGen(private_seed, m, v, n)




public_key, private_key = KeyGen(57, 197, 110 + 197)

print(len(public_key))
print(len(private_key))

# LUOV-7-57-197 2
# LUOV-7-83-283 
# LUOV-7-110-374