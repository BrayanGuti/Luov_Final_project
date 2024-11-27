import numpy as np

def generate_t_and_public_seed(all_bytes, m, v):
    """
    Genera la semilla pública y la matriz T basándose en los bytes generados.

    :param all_bytes: Bytes generados por la función H(private_seed, 32 + (m//8)*v).
    :param m: Número de filas de la matriz T.
    :param v: Número de columnas de la matriz T.
    :return: Una tupla (T, public_seed), donde T es una matriz binaria de tamaño m x v,
             y public_seed son los primeros 32 bytes de la entrada.
    """
    # Separar la semilla pública (primeros 32 bytes)
    public_seed = all_bytes[:32]
    
    # Resto de los bytes que representan T
    t_bytes = all_bytes[32:]
    bits_per_row = v  # Número de columnas por fila
    bits_per_byte = 8

    # Crear la matriz T (m x v) binaria
    T = np.zeros((m, v), dtype=int)

    # Llenar la matriz T fila por fila
    for i in range(m):
        start_bit = i * bits_per_row
        end_bit = start_bit + bits_per_row
        start_byte = start_bit // bits_per_byte
        end_byte = (end_bit + bits_per_byte - 1) // bits_per_byte
        row_bytes = t_bytes[start_byte:end_byte]

        # Convertir los bytes a bits
        row_bits = np.unpackbits(np.frombuffer(row_bytes, dtype=np.uint8))

        # Ajustar los bits de la última fila si m no es divisible por 8
        if (v % 8 != 0) and (len(row_bits) > v):
            row_bits = row_bits[:v]  # Ignorar los bits más significativos sobrantes

        T[i, :] = row_bits[:v]  # Tomar solo los primeros v bits para la fila

    return T.T, public_seed

