import os
import numpy as np
# Pillow is the friendly fork of PIL (the Python Imaging Library).
from PIL import Image, ImageSequence

img_name = 'USC_dornsife.jpg'
img = Image.open(os.path.join('pics', img_name))
assert(isinstance(img, Image.Image))

arr = np.array(img)

arr_r = arr.copy()
arr_g = arr.copy()
arr_b = arr.copy()

for y in range(img.height):
    for x in range(img.width):
        arr_r[y][x][1] = 0
        arr_r[y][x][2] = 0

        arr_g[y][x][0] = 0
        arr_g[y][x][2] = 0

        arr_b[y][x][0] = 0
        arr_b[y][x][1] = 0

Image.fromarray(arr_r).save('result/' + img_name.split('.')[0] + '_red.png')
Image.fromarray(arr_g).save('result/' + img_name.split('.')[0] + '_green.png')
Image.fromarray(arr_b).save('result/' + img_name.split('.')[0] + '_blue.png')
