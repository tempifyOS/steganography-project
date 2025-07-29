from PIL import Image

img = Image.open('./testfiles/Grayscale/_img_92_1080x1080_gray.bmp')
print(img.mode)