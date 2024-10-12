import os
import heapq


def compare_file_sizes(file1, file2):
    try:
        size1 = os.path.getsize(file1)
        size2 = os.path.getsize(file2)

        if size1 < size2:
            return f"{file1} es más pequeño que {file2}"
        elif size1 > size2:
            return f"{file1} es más grande que {file2}"
        else:
            return f"{file1} y {file2} tienen el mismo tamaño"

    except FileNotFoundError:
        return "Al menos uno de los archivos no existe"

def file_compression(raw, compressed):
    try:
        size1 = os.path.getsize(raw)
        size2 = os.path.getsize(compressed)

        return f"Tamaño Sin comprimir: {size1}\nTamaño Archivo Compreso: {size2}\nPorcentaje de Compresion: {(size1-size2)/size1*100 :.2f} %"

    except FileNotFoundError:
        return "Al menos uno de los archivos no existe"

def read_bytes_as_windows_1252(filename):
    try:
        with open(filename, 'rb') as file:
            windows_1252_text = ''
            while True:
                byte = file.read(1)  # Lee un byte del archivo
                if not byte:
                    break  # Si no se lee ningún byte, se ha llegado al final del archivo
                windows_1252_char = byte.decode('windows-1252')  # Intenta decodificar el byte como windows-1252
                windows_1252_text += windows_1252_char  # Agrega el carácter windows-1252 al texto resultante
            return windows_1252_text
    except FileNotFoundError:
        print(f"El archivo '{filename}' no se encuentra.")

def save_binary_string_to_file(filename, binary_string):
    # Verificar que la cadena solo contenga 0s y 1s y que su longitud sea múltiplo de 8
    if not all(c == '0' or c == '1' for c in binary_string) or len(binary_string) % 8 != 0:
        raise ValueError("La cadena debe contener solo 0s y 1s y tener una longitud múltiplo de 8.")

    # Convertir la cadena binaria en bytes
    byte_data = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))

    # Guardar los bytes en el archivo
    try:
        with open(filename, 'wb') as file:
            file.write(byte_data)
        print(f"El archivo '{filename}' ha sido guardado correctamente.")
    except OSError as e:
        print(f"Error al guardar el archivo: {e}")

def read_file_as_binary_string(filename):
    try:
        with open(filename, 'rb') as file:
            byte_data = file.read()
            binary_string = ''.join(format(byte, '08b') for byte in byte_data)
            return binary_string
    except FileNotFoundError:
        print(f"El archivo '{filename}' no se encuentra.")

def save_header_to_file(filename, bwt_header):
    byte_data = str(bwt_header).encode('windows-1252')

    try:
        with open(filename, 'wb') as file:
            file.write(byte_data)
        print(f"Se guardo la cabecera correctamente.")
    except OSError as e:
        print(f"Error al guardar la cabecera")

def add_zero(text):
  cant = (8 - (len(text) % 8))
  for i in range(cant):
    text += '0'
  return text, cant

def get_header(header_bytes):
  aux=header_bytes[:8]
  # Convertimos la cadena de bits a una secuencia de bytes
  bytes_data = bytes(int(aux[i:i+8], 2) for i in range(0, len(aux), 8))
  # Decodificamos los bytes en una cadena (str) utilizando la codificación windows-1252
  header = bytes_data.decode('windows-1252')
  #print(header_bytes[:8], header)
  return header

def save_file(filename, string_descomp):
  try:
    with open(filename, 'w') as file:
        file.write(string_descomp)
    print(f"Se guardo el archivo con la cadena descomprimida correctamente.")
  except OSError as e:
    print(f"Error al guardar la cadena descomprimida")

def int_to_binary_string(number):
    # Convierte el número a bytes (usando 'big' endian)
    byte_representation = number.to_bytes(1, byteorder='big')
    
    # Convierte los bytes a una cadena binaria y elimina el prefijo '0b'
    binary_string = ''.join(format(byte, '08b') for byte in byte_representation)
    
    return binary_string

def binary_to_windows_1252(binary_string):
    # Verifica que la longitud de la cadena sea un múltiplo de 8
    if len(binary_string) % 8 != 0:
        raise ValueError("La longitud de la cadena debe ser un múltiplo de 8.")
    
    # Divide la cadena en grupos de 8 bits
    byte_values = []
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]  # Toma un grupo de 8 bits
        byte_value = int(byte, 2)  # Convierte el byte a un valor entero
        byte_values.append(byte_value)
    
    # Convierte los valores de bytes a una cadena usando la codificación Windows-1252
    ascii_bytes = bytes(byte_values)
    windows_1252_string = ascii_bytes.decode('windows-1252')
    
    return windows_1252_string

def add_header(bytes):
    required_bits = (8-((len(bytes)+3) % 8 ))%8
    for i in range(required_bits):
        bytes += '0'
    return format(required_bits, '03b') + bytes

def remove_header(bytes):
    added_bits = int(bytes[0:3],2)
    return bytes[3:len(bytes)-added_bits]
