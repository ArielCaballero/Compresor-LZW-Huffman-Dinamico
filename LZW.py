import math
import Funciones_Bytes as FB

def compress(uncompressed):
    # Crear un diccionario para la compresión, el diccionario contiene la codificación en binario de todos los caracteres de 8 bits
    dictionary = [FB.int_to_binary_string(i) for i in range(256)]  # Inicializar el diccionario con caracteres de la ISO 8859-1
    #Setea el codigo de la proxima entrada
    current_code = 256
    #Inicializa la cadena a comprimir
    w = ''
    #Inicializa el resultado en vacio
    compressed = ''
    #Loopea por cada caracter de la cadena de entrada (La entrada debe estar decodificada en caracteres de la ISO 8859-1)
    for char in uncompressed:
        #Obtiene el codigo binario de cada caracter
        ISO_8859_char = char.encode('ISO 8859-1')
        #formatea para que los caracteres codificados sean de 8 bits y no tengan la b del tipo de datos bytes
        byte_str = format(ISO_8859_char[0], '08b')
        #añade el ultimo caracter leido de la cadena a w
        wc = w + byte_str
        #Analiza si la cadena que incluye el nuevo caracter está en el diccionario
        if wc in dictionary:
            #Si esta en el diccionario 
            # agrega a w el ultimo caracter y vuelve a iterar
            w = wc
        else:
            #Si no esta en el diccionario
            #Calcula cuantos bits requiere para codificar la longitud del codigo
            #Como vienen codigos de longitud variable, emplea la menor cantidad de bits posibles
            #Para codificar la longitud. A modo de ejemplo, con 1 bit calcula longitud 8 o 9
            #Con 2 bits codifica longitudes del 8 al 11, con 3 bits codifica del 8 al 15 y asi consecutivamente.
            #El largo de la codificación lo hace en base al tamaño actual del diccionario
            max_actual_length=math.ceil(math.log2(math.ceil(math.log2(current_code)-7)))
            #Trae la codificacion del ultimo simbolo que hay almacenado en la tabla
            actual_symbol = dictionary.index(w)
            if len(w) == 8:
                #Si es un solo caracter, utiliza la funcion int_to_binary_string para codificarlo como 8 bits
                #Rellena con 0 la longitud de la codificacion de la longitud del codigo
                codigo = "0".zfill(max_actual_length) + FB.int_to_binary_string(actual_symbol)
            else:
                #Si es mas de un caracter, codifica la longitud del codigo, rellenando con 0 a la longitud
                #maxima posible del codigo según la longitud del diccionario y codifica el simbolo actual (quitando el prefijo "0b")
                codigo = bin(math.ceil((math.log2(actual_symbol+1)))-8)[2:].zfill(max_actual_length) + bin(actual_symbol)[2:]
            #Almacena el resultado en la cadena de salida
            compressed = compressed + codigo
            #Agrega la cadena mas el siguiente caracter en la tabla
            dictionary.append(wc)
            #Incrementa el numero del codigo actuak
            current_code += 1
            #Inicia nuevamente la cadena a iniciar con el ultimo caracter leido
            w = byte_str
    #Una vez finalizada la codificación puede quedar una ultima cadena sin codificar, se toma este caso especial y se guarda en el resultado igual que antes
    if w:
        actual_symbol = dictionary.index(w)
        if len(w) == 8:
                codigo = "0".zfill(max_actual_length) + FB.int_to_binary_string(actual_symbol)
        else:
            codigo = bin(math.ceil((math.log2(actual_symbol+1)))-8)[2:].zfill(max_actual_length) + bin(actual_symbol)[2:]
        compressed = compressed + codigo
    return compressed


def decompress(compressed):
    # Crear un diccionario para la descompresión, el diccionario contiene la codificación en binario de todos los caracteres de 8 bits
    dictionary = [FB.int_to_binary_string(i) for i in range(256)]  # Inicializar el diccionario con caracteres de la ISO 8859-1
    #Lee el primer caracter (que esta codificado como la ISO 8859-1) y lo almacena en la salida. El primer bit es de la longitud de la cadena. Es un "0"
    w = compressed[1:9]
    decompressed = w
    i = 9
    #Comienza a iterar a partir del segundo caracter
    while i<len(compressed):
        #Obtiene en base a la longitud del diccionario cual es la maxima longitud posible de la codificación de la longitud del caracter
        max_actual_length=math.ceil(math.log2(math.ceil(math.log2(len(dictionary)+1)-7)))
        #Obtiene cual es la longitud del caracter
        actual_length = 8+int(compressed[i:i+max_actual_length],2)
        #Incrementa i para estar al principio del caracter a leer
        i = i+max_actual_length
        #Lee el caracter
        char_code = compressed[i:i+actual_length]
        #Busca en que entrada del diccionario debe estar la codificación del caracter
        dict_entry = int(char_code, 2)
        #Analiza si el caracter a leer no es el mismo caracter que se esta leyendo actualmente
        if dict_entry < len(dictionary):
            #Si no lo es, busca la entrada correspondiente
            entry = dictionary[dict_entry]
            #Agrega al diccionario la cadena leida anteriormente concatenada con el primer caracter de la cadena leida actualmente
            dictionary.append(w + entry[:8])
        elif dict_entry == len(dictionary):
            #Si quiere leer el mismo caracter que esta decodificando, Se repite la entrada anterior con el primer caracter de la entrada anterior para sincronizar
            entry=w+w[:8]
            #Se agrega esto al diccionario concatenado con el primer caracter de la entrada
            dictionary.append(w + entry[:8])
        else:
            #Si Busca cualquier otro caso es un error
            raise ValueError
        #Se añade a la cadena a descomprimir
        decompressed= decompressed + entry
        #Se almacena en w la entrada actual, para utilizarla como entrada anterior en la proxima iteracion
        w = entry
        #Se incrementa i para que coincida con el inicio del siguiente codigo
        i=i+actual_length
    return decompressed