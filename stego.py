#!/usr/bin/env python3
"""
Dependencies:
    pip install Pillow
"""
# Written by: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt
# Project Start: 02/07/2025
# Project Finished: XX/XX/2025

# Usage examples:
#   Embed secret.txt into a 1-bit or grayscale BMP cover:
#   python stego.py hide -m secret.txt -c cover.bmp -o out.bmp -M 2 -T 128
#
#   Extract hidden data:
#   python stego.py extract -s out.bmp -o recovered.bin -M 2

import argparse
import time
import sys
from PIL import Image

def file_to_binary_string(filepath):
    # read an arbitrary file in binary mode and return its contents as a
    # string of '0' and '1' chars.
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error: cannot open file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    # convert each byte to its 8-bit binary representation
    return ''.join(f'{byte:08b}' for byte in data)

def find_runs_and_convert_to_output_string(s: str, M: int) -> str:
    """
    Finds all non-overlapping runs of at least length M in the binary string s.
    If the run length is even, then append a '0' to the output.
    If the run length is odd, then append a '1' to the output.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i = 0
    n = len(s)
    output_bits = []

    # Walk the bit‑stream looking for runs ≥ M
    while i < n:
        current_bit = s[i]
        start = i
        while i < n and s[i] == current_bit:
            i += 1
        run_len = i - start
        if run_len >= M:
            output_bits.append('1' if run_len % 2 else '0')

    return ''.join(output_bits)

def hide(message_file, cover_file, stego_file, M, threshold):
    # hides the content of 'message_file' within the 'cover_file' using run length encoding (RLE)
    # even length runs encode '0' while odd-length runs will encode '1'
    # 'M' is the min run length (>=1)
    # 'threshold' only used if cover is grayscale

    # read message as a long bit stream
    bitstring = file_to_binary_string(message_file)
    message_bits = [int(b) for b in bitstring]

    # load cover image
    try:
        img = Image.open(cover_file)
    except Exception as e:
        print(f"Error: cannot open cover file '{cover_file}': {e}", file=sys.stderr)
        sys.exit(1)

    mode = img.mode
    if mode == '1':
        # 1-bit cover: use exactly as before
        bw = img.convert('1', dither=Image.NONE)
        pixels = list(bw.getdata())
        cover_bits = [0 if p == 0 else 1 for p in pixels]

    elif mode == 'L':
        # 8-bit grayscale: threshold to get our bit-stream
        gray = list(img.getdata())
        cover_bits = [1 if px >= threshold else 0 for px in gray]

    else:
        print(f"Error: unsupported cover mode '{mode}'; use 1-bit or 8-bit grayscale BMP.", file=sys.stderr)
        sys.exit(1)

    # check capacity
    capacity = len(cover_bits)
    needed = sum(M + b for b in message_bits)
    if needed > capacity:
        print(f"Error: cover capacity ({capacity} pixels) insufficient; need {needed}.", file=sys.stderr)
        sys.exit(1)

    # build stego bitstream via RLE
    stego_bits = []
    current = cover_bits[0] if cover_bits else 0
    for bit in message_bits:
        stego_bits.extend([current] * (M + bit))
        current ^= 1
    # leftover
    stego_bits.extend(cover_bits[len(stego_bits):])

    # convert back to pixels
    if mode == '1':
        out_pixels = [0 if b == 0 else 255 for b in stego_bits]
        out_img = Image.new('1', img.size)
    else:  # grayscale output
        # map 0→0, 1→255
        out_pixels = [0 if b == 0 else 255 for b in stego_bits]
        out_img = Image.new('L', img.size)

    out_img.putdata(out_pixels)
    try:
        out_img.save(stego_file)
    except Exception as e:
        print(f"Error: cannot save stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)

def extract(stego_file, message_file, M, threshold):
    # recover hidden data from 'stego_file' by scanning runs of length >= M
    # (threshold arg unused here, but kept for symmetry)

    try:
        img = Image.open(stego_file)
    except Exception as e:
        print(f"Error: cannot open stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)

    mode = img.mode
    if mode == '1' or mode == 'L':
        bw = img.convert('1', dither=Image.NONE)
        bits = [0 if p == 0 else 1 for p in bw.getdata()]
        bitstring = ''.join(str(b) for b in bits)
        recovered = find_runs_and_convert_to_output_string(bitstring, M)
    else:
        print(f"Error: unsupported stego mode '{mode}'; expected 1-bit or 8‑bit grayscale BMP.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(message_file, 'wb') as f:
            for i in range(0, len(recovered), 8):
                byte = recovered[i:i+8].ljust(8, '0')
                f.write(int(byte, 2).to_bytes(1, 'big'))
    except Exception as e:
        print(f"Error: cannot write message file '{message_file}': {e}", file=sys.stderr)
        sys.exit(1)

# aesthetic loading function 
def loading_HIDE(message_file, stego_file, cover_file):
    print(f"-------------------------Loading...---------------------------\n(+): HIDE embedding '{message_file}' into '{cover_file}'")
    print(f"(→): Writing file to {stego_file}")
    time.sleep(0.5); print("█▒▒▒▒▒▒▒▒▒ 10%")
    time.sleep(0.5); print("██▒▒▒▒▒▒▒▒ 20%")
    time.sleep(0.5); print("███▒▒▒▒▒▒▒ 30%")
    time.sleep(0.5); print("████▒▒▒▒▒▒ 40%")
    time.sleep(0.5); print("█████▒▒▒▒▒ 50%")
    time.sleep(0.5); print("██████▒▒▒▒ 60%")
    time.sleep(0.5); print("███████▒▒▒ 70%")
    time.sleep(0.5); print('████████▒▒ 80%')
    time.sleep(0.5); print('█████████▒ 90%')
    time.sleep(1);   print('██████████ 100%')

def loading_EXTRACT(stego_file, message_file):
    print(f"-------------------------Loading...---------------------------\n(/): EXTRACT MODE: Extracting hidden data in '{stego_file}' to '{message_file}'")
    print(f"(→): Extracting data to {message_file}")
    time.sleep(0.5); print("█▒▒▒▒▒▒▒▒▒ 10%")
    time.sleep(0.5); print("██▒▒▒▒▒▒▒▒ 20%")
    time.sleep(0.5); print("███▒▒▒▒▒▒▒ 30%")
    time.sleep(0.5); print("████▒▒▒▒▒▒ 40%")
    time.sleep(0.5); print("█████▒▒▒▒▒ 50%")
    time.sleep(0.5); print("██████▒▒▒▒ 60%")
    time.sleep(0.5); print("███████▒▒▒ 70%")
    time.sleep(0.5); print('████████▒▒ 80%')
    time.sleep(0.5); print('█████████▒ 90%')
    time.sleep(1);   print('██████████ 100%')

def main():
    ascii_art = """
    ------------------------------------------------------------------
   |░▒█▀▀▀█░▀█▀░█▀▀░█▀▀▀░▄▀▀▄░░░▒█▀▀█░█▀▀▄░▄▀▀▄░█▀▀▀░█▀▀▄░█▀▀▄░█▀▄▀█ |
   |░░▀▀▀▄▄░░█░░█▀▀░█░▀▄░█░░█░░░▒█▄▄█░█▄▄▀░█░░█░█░▀▄░█▄▄▀░█▄▄█░█░▀░█ |
   |░▒█▄▄▄█░░▀░░▀▀▀░▀▀▀▀░░▀▀░░░░▒█░░░░▀░▀▀░░▀▀░░▀▀▀▀░▀░▀▀░▀░░▀░▀░░▒▀ |
    ----By: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt-----
    """
    print(ascii_art)

    parser = argparse.ArgumentParser(prog='stego.py',
        description='Hide/Extract Data within a 1-bit or 8-bit BMP using RLE')
    subs = parser.add_subparsers(dest='command', required=True)

    # Hide mode
    h = subs.add_parser('hide', help='Embed a message into a cover image')
    h.add_argument('-m','--message', required=True, help='Path to message file')
    h.add_argument('-c','--cover',   required=True, help='Path to cover image (1-bit or 8-bit BMP)')
    h.add_argument('-o','--output',  default='stego.bmp', help='Output stego image file')
    h.add_argument('-M','--min-run', type=int, default=2, help='Minimum run length (default: 2)')
    h.add_argument('-T','--threshold', type=int, default=128,
                   help='Threshold for grayscale→bit (default: 128)')

    # Extract mode
    e = subs.add_parser('extract', help='Extract a message from a stego image')
    e.add_argument('-s','--stego',   required=True, help='Path to stego image (1-bit or 8-bit BMP)')
    e.add_argument('-o','--output',  default='message.bin',   help='Recovered message file')
    e.add_argument('-M','--min-run', type=int, default=2,     help='Minimum run length used during extraction')
    e.add_argument('-T','--threshold', type=int, default=128, help='(unused) just symmetry with hide')

    args = parser.parse_args()

    if args.command == 'hide':
        loading_HIDE(args.message, args.output, args.cover)
        hide(args.message, args.cover, args.output, args.min_run, args.threshold)
        print(f"(✓): Embedded '{args.message}' into '{args.output}' using M={args.min_run}, T={args.threshold}")
    else:
        loading_EXTRACT(args.stego, args.output)
        extract(args.stego, args.output, args.min_run, args.threshold)
        print(f"(✓): Extracted hidden data to '{args.output}' using M={args.min_run}")

if __name__ == "__main__":
    main()
