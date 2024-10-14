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

    return FB.binary_to_ISO_8859(decompressed)

