import Huffman_Dinamico as hd
import LZW as lzw
import Funciones_Bytes as FB
import sys
import os




def compress(file):
    #Lee el archivo a descomprimir y lo transforma en caracteres en codificacion ISO 8859-1
    read_uncompressed = FB.read_bytes_as_ISO_8859(file)
    #Comprime los bytes con compresion LZW
    str_lzw_compression= lzw.compress(read_uncompressed)
    #Agrega una cabecera para completar los bytes, siendo asi multiplo de 8 la longitud
    str_hd = FB.add_header(str_lzw_compression)
    
    #Transforma la salida en binario a una entrada como caracteres para que pueda codificar el algoritmo de Huffman Dinamico
    str_hd = FB.binary_to_ISO_8859(str_hd)
    #Comprime los bytes con compresión Huffmann Dinamico
    str_hd_compression =hd.dynamic_huffman_encode(str_hd, symbols=range(256))
    #Agrega una cabecera para completar los bytes para su escritura
    compressed_file = FB.add_header(str_hd_compression)
    #Cambia la extensión del archivo original y le coloca la extensión .lzwhd
    name = file.split(".")[0]+".lzwhd"
    extension = FB.set_extension(file)
    print(extension)
    #Escribe los bytes resultantes en un archivo denominado compressed.lzwhd
    FB.save_binary_string_to_file(name, extension+compressed_file)
    #Muestra porcentaje de compresión
    print(FB.file_compression(file, name))

def decompress(file):
    #Lee el archivo a descomprimir
    read_compressed=FB.read_file_as_binary_string(file)
    extension, read_compressed = FB.get_extension(read_compressed)
    #Quita la cabecera que completa bytes en la compresión
    str_hd= FB.remove_header(read_compressed)
    #Descomprime la cadena con el algoritmo de Huffman Dinamico
    str_hd_uncompression=hd.dynamic_huffman_decode(str_hd, symbols=range(256))
    #Remueve la cabecera que se añadio para completar los bytes en la compresión de Huffman Dinamico
    str_hd = FB.remove_header(str_hd_uncompression)
    #Descomprime utlizando el algoritom de Lempel-Ziv-Welch
    str_lzw_uncompression= lzw.decompress(str_hd)
    #Cambia la extensión del archivo original y le coloca la extensión seleccionada
    name = file.split(".")[0]+"."+extension
    #Escribe el resultado en un archivo con el nombre de entrada
    FB.save_binary_string_to_file(name, str_lzw_uncompression)

def compare (compressed, uncompressed):
    print(FB.compare_file_sizes(compressed, uncompressed))

def main():
    if len(sys.argv) < 3:
        print("Uso: python compresor.py [compress archivo | decompress archivo | compare archivo_1 archivo_2] ")
        return
    
    command = sys.argv[1]
    file_path = sys.argv[2]

    if command == 'compress':
        compress(file_path)
    elif command == 'decompress':
        decompress(file_path)
    elif command == 'compare':
        try:
            uncompressed = sys.argv[3]
            compare(file_path, uncompressed)
        except IndexError:
            print("Faltan argumentos. Prueba con compare 'archivo_1' 'archivo_2")
    else:
        print("Comando no reconocido o argumentos invalidos. Usa los comandos'compress', 'decompress' o 'compare'")

if __name__ == "__main__":
    main()