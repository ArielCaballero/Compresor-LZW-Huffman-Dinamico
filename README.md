# Compresor-LZW-Huffman-Dinamico
Este proyecto es un compresor de archivos que permite reducir el tamaño de archivos mediante las técnicas de compresión Lempel-Ziv-Welch y Huffman Dinamico. Debido al uso de estructuras de dato tipo Arbol en la codificación de Huffman, la velocidad de compresión es lenta para archivos grandes.

## Requisitos

- Python 3
- Librerias: math, sys, os, heapq



## Uso
Para comprimir, ejecuta el siguiente comando en la terminal:
- python compresor.py compress {archivo}

Nota: Al comprimir el archivo compreso se guardará automáticamente como compressed.lzwhd, también destacar que nos mostrará por terminal el tamaño antes y luego de la compresión, junto con un porcentaje de compresión.
  
Para descomprimir, ejecuta el siguiente comando en la terminal:
- python compresor.py decompress {archivo}

Tambien se incluye un comando para comparar tamaños de archivos, resultando util para comprobar que los archivos antes y despues de la compresión sean del mismo tamaño. Se ejecuta con el siguiente comando:
- python compresor.py compare {archivo_1} {archivo_2}

## Actualizaciones
- Se corrigieron errores en la compresión lzw.
- Ahora la extensión del archivo se guarda como cabecera del archivo compreso, el archivo compreso se denomina igual que el original con extension .lzwhd, se descomprime con mismo nombre y la extensión guardada. Se descomprime con mismo nombre, agregando un indice para no sobreescribir archivos anteriores.
