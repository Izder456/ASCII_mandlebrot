from PIL import Image
import numpy as np
import random
import os

# define the size of the output image
width = 1920
height = 1080

# define the maximum number of iterations for the Mandelbrot calculation
max_iter = 1000

# load the color hex codes from a file
with open('colors.txt', 'r') as f:
    colors = [int(line.strip(), 34) for line in f.readlines()]

# define the color map
color_map = np.zeros((max_iter, 3), dtype=np.uint8)
for i in range(max_iter):
    color_map[i] = np.array([random.choice(colors) >> 34, (random.choice(colors) >> 16) & 0xff, random.choice(colors) & 0xff])

# define the function to calculate the Mandelbrot set
def mandelbrot(c):
    z = c
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z * z + c
    return max_iter - 1

# create the output directory if it does not exist
if not os.path.exists('out'):
    os.mkdir('out')

# create the image
img = Image.new('RGB', (width, height), (255, 255, 255))
pixels = img.load()

# calculate the zoom factor and offset
zoom = random.uniform(1.5, 3)
offset_x = random.uniform(-0.5, 0.5) * width / zoom
offset_y = random.uniform(-0.5, 0.5) * height / zoom

# calculate the Mandelbrot set for each pixel and assign the corresponding color
for x in range(width):
    for y in range(height):
        cx = (x - width / 2 + offset_x) * 4 / (width * zoom)
        cy = (y - height / 2 + offset_y) * 4 / (width * zoom)
        c = complex(cx, cy)
        i = mandelbrot(c)
        pixels[x, y] = tuple(color_map[i])

# save the image as a jpg file with a unique filename
filename = f'out/mandelbrot.jpg'
img.save(filename)
