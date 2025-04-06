# a general hex converter

import sys

usage = """Usage: python hex_converter.py <command> <argument>
          
Commands:
    texth:    convert hexadecimal to text
    hext:     convert text to hexadecimal + padding
    endian:   convert between big and little endian
    dech:     convert hexadecimal to decimal
    hexd:     convert decimal to hexadecimal
    padding:  add padding
          
Example: python hex_converter.py hexd 51966
"""

if len(sys.argv) != 3:
    print(usage)
    sys.exit(0)

command = sys.argv[1]
argm = sys.argv[2]

def add_padding(hex_arg):
    hex_diff = len(hex_arg) % 4
    print("Result:", hex_arg)
    if hex_diff == 0:
        if len(hex_arg) == 4:
            hex_arg += "0" * 4
        else:
            hex_arg += "00" * 4
        hex_arg = "Result with padding: " + separate(hex_arg)
        return hex_arg
    else:
        hex_arg += "0" * hex_diff
        hex_arg = "Result with padding: " + separate(hex_arg)
        return hex_arg

def separate(formatted_arg):
    formatted_new = [formatted_arg, "Separated by bytes: "]
    block_size = 8
    for i in range(0, len(formatted_arg), block_size):
        formatted_new.append(formatted_arg[i: i + block_size])
    return "\n".join(formatted_new)
    
def to_x_endian(hex_arg):
    hex_x = hex_arg

    if len(hex_arg) % 2 != 0:
        hex_x = '0' + hex_arg       
    hex_length = len(hex_x) / 2
    formatted = ""
    chari = -1
    while hex_length > 0:
        formatted += hex_x[chari - 1] + hex_x[chari]
        hex_length -= 1
        chari += -2

    if len(formatted) > 4:
        formatted = "Result: " + separate(formatted)

    return formatted
    
def text_to_hex(text_arg):
    hex_text = text_arg.encode('utf-8').hex()
    # padding
    return add_padding(hex_text)
 
def hex_to_text(hex_arg):
    arg = bytes.fromhex(hex_arg)
    print("Saving to the hex_to_text.txt file...")
    with open("hex_to_text.txt", "wb") as f:
        f.write(arg)
        return "Done!"

def dec_to_hex(dec_arg):
    if dec_arg.isdigit():
        dec_converted = hex(int(dec_arg))[2:].upper()
        return add_padding(dec_converted)
    
def hex_to_dec(hex_arg):
    return int(hex_arg, 16)

if command == "hext":        # text to hex
    print(text_to_hex(argm))
elif command == "texth":     # hex to text
    print(hex_to_text(argm))
elif command == "endian":    # endian conversion
    print(to_x_endian(argm))
elif command == "hexd":      # decimal to hex
    print(dec_to_hex(argm))
elif command == "dech":      # hex to decimal
    print(hex_to_dec(argm))
elif command == "padding":   # add padding
    print(add_padding(argm))
else:
    print("Error: Invalid argument")
    print(usage)