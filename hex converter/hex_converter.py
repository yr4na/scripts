# a general hex converter

import sys

usage = """Usage: python hex_converter.py <command> <argument>
          
Commands:
    texth:  convert hexadecimal to text
    hext:   convert text to hexadecimal + padding
    endian: convert between big and little endian
    dech:   convert hexadecimal to decimal
    hexd:   convert decimal to hexadecimal
          
Example: python hex_converter.py hexd 51966
"""

if len(sys.argv) != 3:
    print(usage)
    sys.exit(0)

command = sys.argv[1]
argm = sys.argv[2]
    
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
    return formatted

    
def text_to_hex(text_arg):
    hex_text = text_arg.encode('utf-8').hex()
    text_diff = len(hex_text) % 4
    if text_diff == 0: # padding
        hex_text += "00" * 4
        return hex_text
    else:
        padding = (4 - (text_diff)) * 2
        hex_text += "00" * padding
        return hex_text
 
def hex_to_text(hex_arg):
    arg = bytes.fromhex(hex_arg)
    print("Saving to the hex_to_text.txt file...")
    with open("hex_to_text.txt", "wb") as f:
        f.write(arg)
        return "Done!"

def dec_to_hex(dec_arg):
    if dec_arg.isdigit():
        return hex(int(dec_arg))[2:].upper()
    
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
else:
    print("Error: Invalid argument")
    print(usage)