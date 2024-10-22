import Huffman_Dinamico as hd
import LZW as lzw
import Funciones_Bytes as FB

file = "original.txt"

read_uncompressed = FB.read_bytes_as_ISO_8859(file)
#str_lzw= lzw.compress(read_text)
str_lzw_compression = read_uncompressed

str_hd_compression =hd.dynamic_huffman_encode(str_lzw_compression, symbols=range(256))

compressed_file = FB.add_header(str_hd_compression)
FB.save_binary_string_to_file("compressed.lzwhd", compressed_file)


read_compressed=FB.read_file_as_binary_string("compressed.lzwhd")
read_compressed= FB.remove_header(read_compressed)
str_hd_uncompression=hd.dynamic_huffman_decode(read_compressed, symbols=range(256))

#str_lzw= lzw.decompress2(str_hd)
str_lzw_uncompression = str_hd_uncompression

FB.save_binary_string_to_file("decompressed_"+file,str(str_lzw_uncompression))

print(FB.file_compression(file, 'compressed.lzwhd'))
print(FB.compare_file_sizes(file, "decompressed_"+file))
