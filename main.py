import Huffman_Dinamico as hd
import LZW as lzw
import Funciones_Bytes as FB

file = "bitnami.ico"


read_uncompressed = FB.read_bytes_as_ISO_8859(file)

print("original: ", len(read_uncompressed))

str_lzw_compression= lzw.compress(read_uncompressed)

print("compresion lzw: ", len(str_lzw_compression))

str_lzw_compression = FB.add_header(str_lzw_compression)
str_lzw_compression = FB.binary_to_ISO_8859(str_lzw_compression)

str_hd_compression =hd.dynamic_huffman_encode(str_lzw_compression, symbols=range(256))

print("compresion hd: ", len(str_hd_compression))


compressed_file = FB.add_header(str_hd_compression)

print("comprimido final: ", len(compressed_file))

FB.save_binary_string_to_file("compressed.lzwhd", compressed_file)

# Pasa a descomprimir
read_compressed=FB.read_file_as_binary_string("compressed.lzwhd")

print("lectura compreso: ", len(read_compressed))

read_compressed= FB.remove_header(read_compressed)

print("previo a descompresion hd: ", len(read_compressed))

str_hd_uncompression=hd.dynamic_huffman_decode(read_compressed, symbols=range(256))

str_hd_uncompression = FB.remove_header(str_hd_uncompression)

print("previo a descompresion lzw: ", len(str_hd_uncompression))

str_lzw_uncompression= lzw.decompress(str_hd_uncompression)

print("Tamaño decompreso: ", len(str_lzw_uncompression)/8)

FB.save_binary_string_to_file("decompressed_"+file,str_lzw_uncompression)


print(FB.file_compression(file, 'compressed.lzwhd'))

print(FB.compare_file_sizes(file, "decompressed_"+file))