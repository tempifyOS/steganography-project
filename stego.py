#!/usr/bin/env python3
"""
Dependencies:
    pip install Pillow
"""
# Written by: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt
# Project Start: 02/07/2025
# Project Finished: XX/XX/2025

# Usage examples:
#   Embed secret.txt into an 8-bit grayscale BMP cover (LSB-only):
#     python stego.py hide -m secret.txt -c cover_gray.bmp -o out.bmp -M 2
#
#   Extract hidden data:
#     python stego.py extract -s out.bmp -o recovered.bin -M 2

import argparse
import time
import sys

# dependency check
try:
    from PIL import Image
except ImportError:
    print("Error: dependency 'Pillow' not installed. Please install by running: pip install Pillow",
          file=sys.stderr)
    sys.exit(1)


def file_to_binary_string(filepath):
    # read an arbitrary file and return its bits as a '0'/'1' string
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
    except Exception as e:
        print(f"Error: cannot open file '{filepath}': {e}", file=sys.stderr)
        sys.exit(1)
    return ''.join(f'{byte:08b}' for byte in data)


def find_runs_and_convert_to_output_string(s: str, M: int) -> str:
    """
    Finds all non-overlapping runs of at least length M in the binary string s.
    Even-length runs → '0', odd-length runs → '1'.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i, n = 0, len(s)
    output_bits = []
    while i < n:
        bit = s[i]
        start = i
        while i < n and s[i] == bit:
            i += 1
        run_len = i - start
        if run_len >= M:
            output_bits.append('1' if run_len % 2 else '0')
    return ''.join(output_bits)


def hide(message_file, cover_file, stego_file, M, threshold):
    # Read payload and prepend 32-bit length header
    with open(message_file, 'rb') as mf:
        data = mf.read()
    length = len(data)
    header_bits = ''.join(str((length >> i) & 1) for i in range(31, -1, -1))
    payload = header_bits + ''.join(f'{b:08b}' for b in data)
    bits = [int(b) for b in payload]

    # Load cover (must be 8-bit grayscale)
    try:
        img = Image.open(cover_file)
    except Exception as e:
        print(f"Error: cannot open cover file '{cover_file}': {e}", file=sys.stderr)
        sys.exit(1)
    if img.mode != 'L':
        print("Error: cover must be 8-bit grayscale BMP for LSB embedding", file=sys.stderr)
        sys.exit(1)

    pixels = list(img.getdata())  # values 0–255
    cover_lsbs = [px & 1 for px in pixels]

    # Capacity check
    cap = len(cover_lsbs)
    needed = sum(M + b for b in bits)
    if needed > cap:
        print(f"Error: cover capacity ({cap}) insufficient; need {needed}.", file=sys.stderr)
        sys.exit(1)

    # RLE encode on LSB stream
    stego_lsbs = []
    cur = cover_lsbs[0]
    for b in bits:
        stego_lsbs.extend([cur] * (M + b))
        cur ^= 1
    stego_lsbs.extend(cover_lsbs[len(stego_lsbs):])

    # Rebuild pixels: replace only the LSB, keep other bits intact
    out_pixels = [ (pixels[i] & 0xFE) | stego_lsbs[i] for i in range(cap) ]

    # Save stego image
    out_img = Image.new('L', img.size)
    out_img.putdata(out_pixels)
    try:
        out_img.save(stego_file)
    except Exception as e:
        print(f"Error: cannot save stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)


def extract(stego_file, message_file, M, threshold):
    # Load stego image
    try:
        img = Image.open(stego_file)
    except Exception as e:
        print(f"Error: cannot open stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)
    if img.mode != 'L':
        print("Error: stego image must be 8-bit grayscale BMP for LSB extraction", file=sys.stderr)
        sys.exit(1)

    pixels = list(img.getdata())
    lsbs = [px & 1 for px in pixels]

    # RLE decode on LSB stream
    raw = find_runs_and_convert_to_output_string(''.join(str(b) for b in lsbs), M)

    # First 32 bits = length header
    length = int(raw[:32], 2)
    data_bits = raw[32:32 + length * 8]

    # Write recovered file
    try:
        with open(message_file, 'wb') as mf:
            for i in range(0, len(data_bits), 8):
                byte = data_bits[i:i+8]
                mf.write(int(byte, 2).to_bytes(1, 'big'))
    except Exception as e:
        print(f"Error: cannot write message file '{message_file}': {e}", file=sys.stderr)
        sys.exit(1)


# aesthetic loading function 
def loading_HIDE(message_file, stego_file, cover_file):
    print(f"-------------------------Loading...---------------------------\n"
          f"(+): HIDE embedding '{message_file}' into '{cover_file}'")
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

#aesthetic loading function
def loading_EXTRACT(stego_file, message_file):
    print(f"-------------------------Loading...---------------------------\n"
          f"(/): EXTRACT MODE: Extracting hidden data in '{stego_file}' to '{message_file}'")
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
    time.sleep(1);  print('██████████ 100%')


def main():
    ascii_art = """
    ------------------------------------------------------------------
   |░▒█▀▀▀█░▀█▀░█▀▀░█▀▀▀░▄▀▀▄░░░▒█▀▀█░█▀▀▄░▄▀▀▄░█▀▀▀░█▀▀▄░█▀▀▄░█▀▄▀█ |
   |░░▀▀▀▄▄░░█░░█▀▀░█░▀▄░█░░█░░░▒█▄▄█░█▄▄▀░█░░█░█░▀▄░█▄▄▀░█▄▄█░█░▀░█ |
   |░▒█▄▄▄█░░▀░░▀▀▀░▀▀▀▀░░▀▀░░░░▒█░░░░▀░▀▀░░▀▀░░▀▀▀▀░▀░▀▀░▀░░▀░▀░░▒▀ |
    ----By: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt-----
    """
    print(ascii_art)

    parser = argparse.ArgumentParser(
        prog='stego.py',
        description='Hide/Extract Data within an 8-bit BMP using LSB+RLE'
    )
    if len(sys.argv) == 1:
        parser.print_help()
        print("""
Examples:
  python stego.py hide   -m secret.txt -c cover_gray.bmp -o stego.bmp -M 8
  python stego.py extract -s stego.bmp     -o recovered.bin -M 8

Arguments for hide:
  -m, --message   Path to message file to hide
  -c, --cover     Path to 8-bit grayscale BMP cover
  -o, --output    Output stego image (default: stego.bmp)
  -M, --min-run   Minimum RLE run length (default: 2)

Arguments for extract:
  -s, --stego     Path to stego image
  -o, --output    Recovered message file (default: message.bin)
  -M, --min-run   Minimum RLE run length used during extraction
""")
        sys.exit(0)

    subs = parser.add_subparsers(dest='command', required=True)

    # Hide mode
    h = subs.add_parser('hide', help='Embed a message into a cover image')
    h.add_argument('-m', '--message', required=True, help='Path to message file')
    h.add_argument('-c', '--cover',   required=True, help='Path to 8-bit grayscale BMP cover')
    h.add_argument('-o', '--output',  default='stego.bmp', help='Output stego image')
    h.add_argument('-M', '--min-run', type=int, default=2, help='Minimum RLE run length')

    # Extract mode
    e = subs.add_parser('extract', help='Extract a message from a stego image')
    e.add_argument('-s', '--stego',   required=True, help='Path to stego image')
    e.add_argument('-o', '--output',  default='message.bin', help='Recovered message file')
    e.add_argument('-M', '--min-run', type=int, default=2, help='Minimum RLE run length')

    args = parser.parse_args()

    if args.command == 'hide':
        loading_HIDE(args.message, args.output, args.cover)
        hide(args.message, args.cover, args.output, args.min_run, None)
        print(f"(✓): Embedded '{args.message}' into '{args.output}' using M={args.min_run}")
    else:
        loading_EXTRACT(args.stego, args.output)
        extract(args.stego, args.output, args.min_run, None)
        print(f"(✓): Extracted hidden data to '{args.output}' using M={args.min_run}")

if __name__ == "__main__":
    main()
