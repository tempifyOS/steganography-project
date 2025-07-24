#!/usr/bin/env python3
"""
Dependencies:
    pip install Pillow
"""
# Written by: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt
# Project Start: 02/07/2025
# Project Finished: XX/XX/2025
# Repository: https://github.com/tempifyOS/steganography-project

import argparse
import time
import math
import sys
from PIL import Image


def file_to_binary_string(filepath):
    """
    Read an arbitrary file in binary mode and return its contents
    as a string of '0' and '1' chars.
    """
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
    If the run length is even, append '0'; if odd, append '1'.
    """
    if M <= 0:
        raise ValueError("Minimum length M must be greater than 0.")

    i = 0
    n = len(s)
    output = []
    while i < n:
        run_char = s[i]
        start = i
        while i < n and s[i] == run_char:
            i += 1
        run_length = i - start
        if run_length >= M:
            output.append('1' if run_length % 2 else '0')
    return ''.join(output)


def hide(message_file, stego_file, cover_file):
    print("Hide code goes here... Delete this")
    # TODO: implement hide(message_file, cover_file, stego_file)


def extract(stego_file, message_file):
    print("Extract code goes here... Delete this")
    # TODO: implement extract(stego_file, message_file)


def loading_HIDE(message_file, stego_file, cover_file):
    print(
        "-------------------------Loading...---------------------------"
        f"\n(+): HIDE embedding '{message_file}' into '{cover_file}'"
    )
    print(f"(→): Writing file to {stego_file}")
    for pct in range(10, 101, 10):
        print(f"{'█' * (pct // 10)}{'▒' * (10 - pct // 10)} {pct}%")
        time.sleep(0.5)
    print(f"(✓): Embedded '{message_file}' to {stego_file}")


def loading_EXTRACT(stego_file, message_file):
    print(
        "-------------------------Loading...---------------------------"
        f"\n(/): EXTRACT MODE: Extracting hidden data in '{stego_file}' to '{message_file}'"
    )
    print(f"(→): Extracting data to {message_file}")
    for pct in range(10, 101, 10):
        print(f"{'█' * (pct // 10)}{'▒' * (10 - pct // 10)} {pct}%")
        time.sleep(0.5)
    print(f"(✓): Extracted data in '{stego_file}' to {message_file}")


def main():
    ascii_art = (
        "------------------------------------------------------------------"
        "\n|░▒█▀▀▀█░▀█▀░█▀▀░█▀▀▀░▄▀▀▄░░░▒█▀▀█░█▀▀▄░▄▀▀▄░█▀▀▀░█▀▀▄░█▀▀▄░█▀▄▀█ |"
        "\n|░░▀▀▀▄▄░░█░░█▀▀░█░▀▄░█░░█░░░▒█▄▄█░█▄▄▀░█░░█░█░▀▄░█▄▄▀░█▄▄█░█░▀░█ |"
        "\n|░▒█▄▄▄█░░▀░░▀▀▀░▀▀▀▀░░▀▀░░░░▒█░░░░▀░▀▀░░▀▀░░▀▀▀▀░▀░▀▀░▀░░▀░▀░░▒▀ |"
        "\n----By: Levi Torres, Lawrence Skergan, Andrew Kolb, Ryan Hunt-----"
    )
    print(ascii_art)

    parser = argparse.ArgumentParser(
        prog='Stego Program',
        description='Hide/Extract Data within a binary file using RLE/Edge Hiding'
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    hide_parser = subparsers.add_parser('hide', help='Embed a message into a cover file')
    hide_parser.add_argument('-m', '--message', help='Path to message file')
    hide_parser.add_argument('-c', '--cover', help='Cover file')
    hide_parser.add_argument('-o', '--output', help='Output stego file')

    extract_parser = subparsers.add_parser('extract', help='Extract a message from a stego file')
    extract_parser.add_argument('-s', '--stego', required=True, help='Path to stego file')
    extract_parser.add_argument('-o', '--output', required=True, help='Recovered message file')

    args = parser.parse_args()
    if args.command == 'hide':
        loading_HIDE(args.message, args.output, args.cover)
        # hide(args.message, args.cover, args.output)
    else:
        loading_EXTRACT(args.stego, args.output)
        # extract(args.stego, args.output)


if __name__ == '__main__':
    main()
