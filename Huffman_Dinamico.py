class HuffmanNode:
    def __init__(self, char, frequency):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

    def __contains__(self, target_node):
        # Verificar si el nodo actual es igual al nodo objetivo
        if self == target_node:
            return True

        # Luego, comprobar si el nodo objetivo está en el subárbol izquierdo o derecho
        if self.left and target_node in self.left:
            return True
        if self.right and target_node in self.right:
            return True

        # Si no se encuentra en el subárbol izquierdo ni en el derecho, retornar False
        return False

class DynamicHuffmanTree:
    def __init__(self):
      self.root = None
      self.char_to_node = {}

    def build_initial_tree(self):
      # Inicialmente, crea un árbol con un nodo especial (EOF) con frecuencia 1
      self.root = HuffmanNode('imaginario', 0)
      self.char_to_node['imaginario'] = self.root

    def update_tree(self, char, symbols):
      flag = False
      if char in self.char_to_node:
          self.char_to_node[char].frequency += 1
          self.update_frequency(self.root)
          self.reorganize_tree(self.root)

      else:
          # Si el carácter no existe, crea un nuevo nodo con frecuencia 1
          new_node = HuffmanNode(char, 1)
          self.char_to_node[char] = new_node

          if self.root.char == 'imaginario':

            # Combina el nuevo nodo con el nodo especial EOF
            combined_node = HuffmanNode(None, 0)
            combined_node.left = self.root
            combined_node.right = new_node
            combined_node.frequency = new_node.frequency + self.root.frequency
            self.root = combined_node

          else:
            if(len(symbols) != len(self.char_to_node)- 1):
              combined_node = HuffmanNode(None, 1)
              combined_node.left = self.char_to_node['imaginario']
              combined_node.right = new_node
            else:
              flag = True
            current_node = self.root
            while (current_node.left != self.char_to_node['imaginario']):
                if (current_node.left is not None) and (self.char_to_node['imaginario'] in current_node.left):
                  current_node = current_node.left
                elif self.char_to_node['imaginario'] in current_node.right:
                  current_node = current_node.right
            if not flag:
              current_node.left = combined_node
            else:
              current_node.left = new_node
          # Reorganiza el árbol
          self.update_frequency(self.root)
          self.reorganize_tree(self.root)
          #self.preorden(self.root)

    def preorden(self, current):
      if current:
        #print(current.char, current.frequency)
        self.preorden(current.left)
        self.preorden(current.right)

    def update_frequency(self, current): #MOSTRAR CHICAS
      if current:
        self.update_frequency(current.left)
        self.update_frequency(current.right)
        if current.left is None and current.right is None:
            return
        else:
            current.frequency = current.left.frequency + current.right.frequency

    def reorganize_tree(self, current):
        if current:
          if current.left is not None and current.right is not None:
            if current.left.frequency > current.right.frequency:
                if (current.left.frequency-current.right.frequency) == 1:
                    aux= current.left
                    current.left = current.right
                    current.right = aux
                else:
                    if current.right.left is not None and current.right.right is not None:
                      if current.left.frequency < current.right.left.frequency:
                        aux= current.left
                        current.left = current.right.left
                        current.right.left = aux
                      else:
                        aux= current.left
                        current.left = current.right.right
                        current.right.right = aux
            elif (current.right.right is not None) and (current.left.frequency < current.right.right.frequency):
              aux= current.left
              current.left = current.right.right
              current.right.right = aux
          self.reorganize_tree(current.left)
          self.reorganize_tree(current.right)


def encode_path_to_root(root, target_node):
  # Codifica el camino desde el nodo actual al nodo objetivo
  current_node = root
  encoded_path = ''

  while current_node != target_node:
    if target_node in current_node.left:
      encoded_path += '0'
    elif target_node in current_node.right:
      encoded_path += '1'

    current_node = current_node.left if target_node in current_node.left else current_node.right

  return encoded_path

def dynamic_huffman_encode(text, symbols):
    huffman_tree = DynamicHuffmanTree()
    huffman_tree.build_initial_tree()
    encode = ''
    for char in text:
        ISO_8859_char = char.encode('ISO 8859-1')
        for byte_char in ISO_8859_char:
            byte_str = format(byte_char, '08b')  # Convertir byte a cadena binaria
            if byte_str not in huffman_tree.char_to_node:
                encode += encode_path_to_root(huffman_tree.root, huffman_tree.char_to_node['imaginario'])
                huffman_tree.update_tree(byte_str, symbols)
                encode += byte_str  # Agregar la representación binaria del byte
            else:
                encode += encode_path_to_root(huffman_tree.root, huffman_tree.char_to_node[byte_str])
                huffman_tree.update_tree(byte_str, symbols)
        #print(encode)
    return encode

def dynamic_huffman_decode(encoded_text, symbols):
    huffman_tree = DynamicHuffmanTree()
    huffman_tree.build_initial_tree()
    decoded_text = b""
    i = 0

    while i < len(encoded_text):
        current_node = huffman_tree.root
        while current_node.char is None:
            if encoded_text[i] == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right
            i += 1

        if current_node.char == 'imaginario':
            byte_str = encoded_text[i:i + 8]
            byte_char = int(byte_str, 2)
            huffman_tree.update_tree(byte_str, symbols)
            decoded_text += bytes([byte_char])
            i += 8
        else:
            byte_str = current_node.char
            byte_char = int(byte_str, 2)
            huffman_tree.update_tree(byte_str, symbols)
            decoded_text += bytes([byte_char])
    return ''.join(format(byte, '08b') for byte in decoded_text)