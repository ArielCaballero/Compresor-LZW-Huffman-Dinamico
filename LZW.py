import math
import Funciones_Bytes as FB

def compress(uncompressed):
    # Crear un diccionario para la compresión
    dictionary = {chr(i): i for i in range(256)}  # Inicializar el diccionario con caracteres ASCII
    current_code = 256
    w = ""
    compressed = []

    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            compressed.append(dictionary[w])
            dictionary[wc] = current_code
            current_code += 1
            w = c

    if w:
        compressed.append(dictionary[w])
    
    return ''.join(format(code, '08b') for code in compressed)  # Convertir a binario para salida


def decompress(compressed):
    # Crear un diccionario para la descompresión
    dictionary = {i: bin(i).encode("ISO 8859-1") for i in range(256)}  # Inicializar el diccionario con caracteres ASCII
    current_code = 256

    # Convertir el string comprimido en una lista de códigos enteros
    compressed_codes = [int(compressed[i:i + 8], 2) for i in range(0, len(compressed), 8)]
    
    w = bin(compressed_codes[0]).encode("ISO 8859-1")
    decompressed = bytes(int(w.decode("ISO 8859-1"), 2)).decode("ISO 8859-1")

    for code in compressed_codes[1:]:
        char_code = bin(code).encode("ISO 8859-1")
        if code in dictionary:
            entry = dictionary[int(char_code.decode("ISO 8859-1"), 2)]
        elif int(char_code.decode("ISO 8859-1")) == current_code:
            entry = w + w[:8]
        else:
            raise ValueError("Código inválido en la entrada comprimida.")
        
        decompressed += bytes((int(entry[j:j+8].decode("ISO 8859-1"),2)) for j in range(0, len(entry), 8)).decode("ISO 8859-1") 

        # Agregar la nueva entrada al diccionario
        dictionary[current_code] = w + entry[:8]
        current_code += 1
        
        w = entry
    return str(decompressed)

'''def compress2(uncompressed):
    # Crear un diccionario para la compresión
    dictionary = [FB.int_to_binary_string(i) for i in range(256)]  # Inicializar el diccionario con caracteres ASCII
    w = ''
    for i in range(0, len(uncompressed)-8, 8):
        char_code = uncompressed[i:i+j]
        while(not (char_code in dictionary)):
            j-=1
            char_code = uncompressed[i:i+j]
            if j==7:
                raise ValueError("No se encontro ningun caracter")
        entry = dictionary[int(char_code, 2)]
        
        compressed= compressed + entry

        # Agregar la nueva entrada al diccionario
        dictionary.append(w + entry[:8])
        
        w = entry
        i=i+j
    
    return compressed # Convertir a binario para salida'''

def decompress2(compressed):
    # Crear un diccionario para la descompresión
    dictionary = [FB.int_to_binary_string(i) for i in range(256)]  # Inicializar el diccionario con caracteres ASCII
    
    w = compressed[0:8]
    decompressed = w
    i = 8
    while i<len(compressed):
        j = math.ceil(math.log2(len(dictionary)))
        char_code = compressed[i:i+j]
        if char_code[0]=="0":
            j=8
            char_code = compressed[i:i+j]
        else:
            while(int(char_code, 2) >= len(dictionary)):
                j-=1
                char_code = compressed[i:i+j]
                if j==7:
                    #raise ValueError("No se encontro ningun caracter")
                    return decompressed
        entry = dictionary[int(char_code, 2)]

        decompressed= decompressed + entry

        # Agregar la nueva entrada al diccionario
        dictionary.append(w + entry[:8])
        
        w = entry
        i=i+j
    return decompressed