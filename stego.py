#!/usr/bin/env python3
"""
Dependencies:
    pip install Pillow
"""
# Written by: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt
# Project Start: 02/07/2025
# Project Finished: XX/XX/2025

# Usage examples:
#   Embed secret.txt into a 1‑bit or grayscale BMP cover:
#     python stego.py hide -m secret.txt -c cover.bmp -o out.bmp -M 2 -T 128
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
    # read an arbitrary file in binary mode and return its contents as a
    # string of '0' and '1' chars.
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
    If the run length is even, then append a '0' to the output.
    If the run length is odd, then append a '1' to the output.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i = 0
    n = len(s)
    output_bits = []

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
    # hides the content of 'message_file' within the 'cover_file' using RLE
    # prefixes a 32-bit length header so no extra junk is recovered
    with open(message_file, 'rb') as mf:
        data = mf.read()
    length = len(data)
    # build 32-bit big-endian header
    header_bits = ''.join(str((length >> i) & 1) for i in range(31, -1, -1))
    payload = header_bits + ''.join(f'{b:08b}' for b in data)
    bits = [int(b) for b in payload]

    # load cover image
    try:
        img = Image.open(cover_file)
    except Exception as e:
        print(f"Error: cannot open cover file '{cover_file}': {e}", file=sys.stderr)
        sys.exit(1)

    mode = img.mode
    if mode == '1':
        bw = img.convert('1', dither=Image.NONE)
        cover_bits = [0 if p == 0 else 1 for p in bw.getdata()]
    elif mode == 'L':
        gray = list(img.getdata())
        cover_bits = [1 if px >= threshold else 0 for px in gray]
    else:
        print(f"Error: unsupported cover mode '{mode}'; use 1-bit or 8-bit grayscale BMP.",
              file=sys.stderr)
        sys.exit(1)

    capacity = len(cover_bits)
    needed = sum(M + b for b in bits)
    if needed > capacity:
        print(f"Error: cover capacity ({capacity}) insufficient; need {needed}.", file=sys.stderr)
        sys.exit(1)

    # RLE encode
    stego_bits = []
    current = cover_bits[0] if cover_bits else 0
    for b in bits:
        stego_bits.extend([current] * (M + b))
        current ^= 1
    stego_bits.extend(cover_bits[len(stego_bits):])

    # write stego image
    out_pixels = [0 if b == 0 else 255 for b in stego_bits]
    out_img = Image.new('1' if mode == '1' else 'L', img.size)
    out_img.putdata(out_pixels)
    try:
        out_img.save(stego_file)
    except Exception as e:
        print(f"Error: cannot save stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)


def extract(stego_file, message_file, M, threshold):
    # recover hidden data from 'stego_file' by scanning runs ≥ M
    try:
        img = Image.open(stego_file)
    except Exception as e:
        print(f"Error: cannot open stego file '{stego_file}': {e}", file=sys.stderr)
        sys.exit(1)

    if img.mode not in ('1', 'L'):
        print(f"Error: unsupported stego mode '{img.mode}'; expected 1-bit or 8-bit grayscale BMP.",
              file=sys.stderr)
        sys.exit(1)

    bw = img.convert('1', dither=Image.NONE)
    bits = [0 if p == 0 else 1 for p in bw.getdata()]
    raw = find_runs_and_convert_to_output_string(''.join(str(b) for b in bits), M)

    # first 32 bits = length
    length = int(raw[:32], 2)
    data_bits = raw[32:32 + length * 8]

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
        description='Hide/Extract Data within a 1-bit or 8-bit BMP using RLE + length header'
    )
    if len(sys.argv) == 1:
        parser.print_help()
        print("""
Examples:
  python stego.py hide   -m secret.txt -c cover.bmp -o stego.bmp -M 2 -T 128
  python stego.py extract -s stego.bmp  -o recovered.bin -M 2

Arguments for hide:
  -m, --message    Path to message file to hide
  -c, --cover      Path to cover (1-bit or 8-bit BMP)
  -o, --output     Stego image output file (default: stego.bmp)
  -M, --min-run    Minimum RLE run length (default: 2)
  -T, --threshold  Grayscale threshold (default: 128)

Arguments for extract:
  -s, --stego      Path to stego image (1-bit or 8-bit BMP)
  -o, --output     Recovered message file output (default: message.bin)
  -M, --min-run    Minimum RLE run length used during extraction (default: 2)
""")
        
        if getattr(sys, 'frozen', False):  # Detect if running from PyInstaller bundle
            input("\nPress Enter to exit...")   # Pause after running by double-clicking the .exe
        sys.exit(0)

    subs = parser.add_subparsers(dest='command', required=True)

    # Hide mode
    h = subs.add_parser('hide', help='Embed a message into a cover image')
    h.add_argument('-m', '--message',   required=True, help='Path to message file')
    h.add_argument('-c', '--cover',     required=True, help='Path to cover image (1-bit or 8-bit BMP)')
    h.add_argument('-o', '--output',    default='stego.bmp', help='Output stego image file')
    h.add_argument('-M', '--min-run',   type=int, default=2,    help='Minimum run length (default: 2)')
    h.add_argument('-T', '--threshold', type=int, default=128,  help='Threshold for grayscale→bit (default: 128)')

    # Extract mode
    e = subs.add_parser('extract', help='Extract a message from a stego image')
    e.add_argument('-s', '--stego',     required=True, help='Path to stego image (1-bit or 8-bit BMP)')
    e.add_argument('-o', '--output',    default='message.bin', help='Recovered message file')
    e.add_argument('-M', '--min-run',   type=int, default=2,    help='Minimum run length used during extraction')
    e.add_argument('-T', '--threshold', type=int, default=128,  help='(unused) symmetry with hide')

    args = parser.parse_args()

    if args.command == 'hide':
        loading_HIDE(args.message, args.output, args.cover)
        hide(args.message, args.cover, args.output, args.min_run, args.threshold)
        print(f"(✓): Embedded '{args.message}' into '{args.output}' using M={args.min_run}, T={args.threshold}")
    else:
        loading_EXTRACT(args.stego, args.output)
        extract(args.stego, args.output, args.min_run, args.threshold)
        print(f"(✓): Extracted hidden data to '{args.output}' using M={args.min_run}'")
    


if __name__ == "__main__":
    main()