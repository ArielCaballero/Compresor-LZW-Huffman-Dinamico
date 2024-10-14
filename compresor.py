import Huffman_Dinamico as hd
import LZW as lzw
import Funciones_Bytes as FB
import sys
import os




def compress(file):
    read_uncompressed = FB.read_bytes_as_ISO_8859(file)
    str_lzw_compression= lzw.compress(read_uncompressed)


    str_hd = FB.add_header(str_lzw_compression)

    str_hd = FB.binary_to_ISO_8859(str_hd)

    str_hd_compression =hd.dynamic_huffman_encode(str_hd, symbols=range(256))

    compressed_file = FB.add_header(str_hd_compression)
    FB.save_binary_string_to_file("compressed.lzwhd", compressed_file)
    print(FB.file_compression(file, 'compressed.lzwhd'))

def decompress(file, extension):
    read_compressed=FB.read_file_as_binary_string(file)

    str_hd= FB.remove_header(read_compressed)
    
    str_hd_uncompression=hd.dynamic_huffman_decode(str_hd, symbols=range(256))

    str_hd = FB.remove_header(str_hd_uncompression)

    str_lzw_uncompression= lzw.decompress(str_hd)

    FB.save_file("decompressed."+extension, str_lzw_uncompression)

def compare (compressed, uncompressed):
    print(FB.compare_file_sizes(compressed, uncompressed))

def main():
    if len(sys.argv) < 3:
        print("Uso: python compresor.py [compress archivo| decompress archivo extension | compare archivo_1 archivo_2] ")
        return
    
    command = sys.argv[1]
    file_path = sys.argv[2]

    if command == 'compress':
        compress(file_path)
    elif command == 'decompress':
        try:
            extension = sys.argv[3]
            decompress(file_path, extension)
        except IndexError:
            print("Faltan argumentos. Prueba con decompress 'archivo' 'extension'")
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