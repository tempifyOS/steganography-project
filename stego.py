# Written by: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt
# Project Start: 02/07/2025
# Project Finished: XX/XX/2025
# Repository: https://github.com/tempifyOS/steganography-project
import argparse
import time
import math
import sys
from PIL import Image

def hide(message_file,stego_file,cover_file):
    print("Hide code goes here... Delete this")
    #TODO: Hide {message_file} in {cover_file} and write to {stego_file}
    #TODO: Write to hidden file with hidden content
    
def extract(stego_file, message_file):
    print("Extract code goes here... Delete this")
    
    #TODO: Extract data from {stego_file} to {message_file}
    #TODO: Write extracted data to a file 

def file_to_binary_string(filepath):
    # read an arbitrary file in binary mode and return its contents as a string of '0' and '1' chars.
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        binary_string = ''.join(f'{byte:08b}' for byte in data)
        return binary_string
    except Exception as e:
        print(f"Error: cannot open file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    return ''.join(f'{byte:08b}' for byte in data)

    #example usage
    #binary = file_to_binary_string('message.txt')
    #print(binary)

def find_runs_and_convert_to_output_string(s: str, M: int) -> str:
    """
    Finds all non-overlapping runs of at least length M in the binary string s.
    If the run length is even, then append a '0' to the output.
    If the run length is odd, then append a '1' to the output.

    Parameters:
    - s (str): A string of '0's and '1's.
    - M (int): The minimum run length.

    Returns:
    - str: A string of '0's and '1's - this should be converted into the output file/message
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i = 0
    n = len(s)
    output = ""

    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        if run_length >= M:
            output += '1' if run_length     % 2 == 1 else '0'

    return output

def main():
    ascii_art = """
    ------------------------------------------------------------------
   |░▒█▀▀▀█░▀█▀░█▀▀░█▀▀▀░▄▀▀▄░░░▒█▀▀█░█▀▀▄░▄▀▀▄░█▀▀▀░█▀▀▄░█▀▀▄░█▀▄▀█ |
   |░░▀▀▀▄▄░░█░░█▀▀░█░▀▄░█░░█░░░▒█▄▄█░█▄▄▀░█░░█░█░▀▄░█▄▄▀░█▄▄█░█░▀░█ |
   |░▒█▄▄▄█░░▀░░▀▀▀░▀▀▀▀░░▀▀░░░░▒█░░░░▀░▀▀░░▀▀░░▀▀▀▀░▀░▀▀░▀░░▀░▀░░▒▀ |
    ----By: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt-----
    """
    
    print(ascii_art)
    
    parser = argparse.ArgumentParser(prog='Stego Program',
            description='Hide/Extract Data within a binary file using RLE/Edge Hiding')
    
    subparsers = parser.add_subparsers(dest='command', 
            required=True, help='Available modes')
    
    #1: Hide Mode
    ### example usage: python3 stego.py hide -m <test.txt> -c <cover.???> -o <output.???>
    hide_parser = subparsers.add_parser('hide')
    hide_parser.add_argument('-m', '--message', 
                             help='Path to message file') # message to be hidden argument
    hide_parser.add_argument('-c', '--cover', 
                             help='Cover file') # cover file argument
    hide_parser.add_argument('-o', '--output', 
                             help='Output file name') # output file argument
    
    #2: Extract mode
    extract_parser = subparsers.add_parser('extract', 
                            help='Extract a message from a stego file')

    
    extract_parser.add_argument('-s', '--stego', required=True, help='Path to stego file') # stego file to extract from
    extract_parser.add_argument('-o', '--output', required=True, help='Output file name') # name output file
    
    
    args = parser.parse_args()
    
    if args.command == 'hide': # hide case
        message_file = args.message # THIS IS THE MESSAGE TO BE HIDDEN
        cover_file = args.cover # THIS IS THE FILE THAT WILL STORE THE HIDDEN MESSAGE
        stego_file = args.output # OUTPUTTED FILE WITH MESSAGE HIDDEN
        loading_HIDE(message_file,stego_file,cover_file)
        # TODO: call hide function:: 
        # hide(message_file, cover_file, stego_file)
        
    if args.command == 'extract': # extract case
        stego_file = args.stego
        message_file = args.output
        loading_EXTRACT(stego_file, message_file)
        # TODO: call extract function::
        # extract(stego_file, message_file)
        
        
        
        
def loading_HIDE(message_file, stego_file, cover_file):
    print(f"-------------------------Loading...---------------------------\n(+): HIDE embedding '{message_file}' into '{cover_file}'")
    print(f"(→): Writing file to {stego_file}")
    time.sleep(0.5)
    print("█▒▒▒▒▒▒▒▒▒ 10%")
    time.sleep(0.5)
    print("██▒▒▒▒▒▒▒▒ 20%")
    time.sleep(0.5)
    print("███▒▒▒▒▒▒▒ 30%")
    time.sleep(0.5)
    print("████▒▒▒▒▒▒ 40%")
    time.sleep(0.5)
    print("█████▒▒▒▒▒ 50%")
    time.sleep(0.5)
    print("██████▒▒▒▒ 60%")
    time.sleep(0.5)
    print("███████▒▒▒ 70%")
    time.sleep(0.5)
    print('████████▒▒ 80%')
    time.sleep(0.5)
    print('█████████▒ 90%')
    time.sleep(1)
    print('██████████ 100%')
    print(f"(✓): Embedded '{message_file}' to {stego_file}")

def loading_EXTRACT(stego_file, message_file):
    print(f"-------------------------Loading...---------------------------\n(/): EXTRACT MODE: Extracting hidden data in '{stego_file}' to '{message_file}'")
    print(f"(→): Extracting data to {message_file}")
    time.sleep(0.5)
    print("█▒▒▒▒▒▒▒▒▒ 10%")
    time.sleep(0.5)
    print("██▒▒▒▒▒▒▒▒ 20%")
    time.sleep(0.5)
    print("███▒▒▒▒▒▒▒ 30%")
    time.sleep(0.5)
    print("████▒▒▒▒▒▒ 40%")
    time.sleep(0.5)
    print("█████▒▒▒▒▒ 50%")
    time.sleep(0.5)
    print("██████▒▒▒▒ 60%")
    time.sleep(0.5)
    print("███████▒▒▒ 70%")
    time.sleep(0.5)
    print('████████▒▒ 80%')
    time.sleep(0.5)
    print('█████████▒ 90%')
    time.sleep(1)
    print('██████████ 100%')
    print(f"(✓): Extracted data in '{stego_file}' to {message_file}")
if __name__ == "__main__":
    main()