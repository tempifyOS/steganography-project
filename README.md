
# Steganography Hide/Extract Program

This command-line tool lets you hide and extract arbitrary binary files inside 8-bit grayscale BMP images by using a simple run-length encoding (RLE) scheme on each pixel’s least significant bit. You supply a “cover” image and a message file, and the program weaves the payload into the image without noticeably changing its appearance. When you’re ready, you run the extractor with the same parameters and recover exactly the original data—no extra padding or noise.

Who It’s For

* Developers & Security Enthusiasts who need a quick way to embed small files (up to tens of kilobytes) in an image without writing custom steganography code.

* Students & Educators looking for a hands-on example of digital steganography with clear, tunable parameters (run-length and threshold) and a visible demonstration of LSB-based hiding.

* Anyone who wants an easy, no-frills CLI tool to hide configuration snippets, text notes, or tiny binaries inside a “harmless” photo, with minimal visual artifacts and no GUI dependencies.

## Contributors

- [@TempifyOS](https://www.github.com/TempifyOS) — Ryan Hunt
- [@Isker](https://github.com/Isker) — Lawrence Skergan
- [@lev-ijtor](https://github.com/lev-ijtor) — Levi Torres
- [@Andrew043y](https://github.com/andrew043y) — Andrew Kolb



## Installation

To download and run this project:

&nbsp;Download the repository:

```bash
  git clone git@github.com:tempifyOS/steganography-project.git
```
&nbsp;Install Python Dependencies:

```pip
    pip install Pillow
```
&nbsp;Hide Command (files included in ```/testfiles```)
```bash
python stego.py hide -m "./testfiles/message/tone.wav" -c "./testfiles/Grayscale/_img_02_1920x1280_gray.bmp" -o stego_tone.bmp -M 2 -T 128
```
&nbsp; Extract Command
```bash
python stego.py extract -s stego_tone.bmp -o recovered_tone.wav -M 2
```
## Documentation

[Google Doc: Documentation/Final Report](https://docs.google.com/document/d/1BKFy9F3aYkB1D2ZtkUSzWKrQEUWBWRFQclWnBbTZ8qs/edit?usp=sharing)




## Demo

[![Demo Video](https://img.youtube.com/vi/ZcKshXf1ZfI/0.jpg)](https://www.youtube.com/watch?v=ZcKshXf1ZfI)
