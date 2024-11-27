import hashlib

def H(message: bytes, output_length: int) -> bytes:
    """
    Función extendable de salida (XOF) H, utiliza SHAKE128 para hashear el mensaje
    y derivar la clave pública.
    
    :param message: El mensaje a hashear como bytes.
    :param output_length: La longitud deseada de la salida en bytes.
    :return: El hash del mensaje de la longitud especificada.
    """
    shake = hashlib.shake_128()
    shake.update(message)
    return shake.digest(output_length)

def G(public_seed: bytes, output_length: int) -> bytes:
    """
    Función extendable de salida (XOF) G, utiliza SHAKE128 para generar el mapa público
    a partir de una semilla pública.
    
    :param public_seed: La semilla pública como bytes.
    :param output_length: La longitud deseada de la salida en bytes.
    :return: El mapa público generado de la longitud especificada.
    """
    shake = hashlib.shake_128()
    shake.update(public_seed)
    return shake.digest(output_length)

