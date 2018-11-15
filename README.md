# NKUST-Data-Compression-Midterm

## Usage
**encode**  
`python compress.py encode <algorithm> <input file name> <output file name>`  
**decode**  
`python compress.py decode <algorithm> <input file name> <output file name>`  

Accepted algorithm:  
* `nocompress` - No compression
* `lz78` - LZ78
* `xp01` - Invented by myself, only works for UTF-8 encoding
* `xp01b` - Invented by myself, similar to xp01, binary mode
* `xp02` - Invented by myself, combination of xp01 and huffman, only works for UTF-8 encoding
* `xp02b` - Invented by myself, combination of xp01 and huffman, similar to xp02, binary mode
* `huffman` - Huffman
* `auto` - Automatically choose the best of the above algorithms
