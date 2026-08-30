from PIL import Image, ImageDraw
import time
import random

WIDTH = 800
HEIGHT = 600
NUM_LINES = 5000

img = Image.new("RGB", (WIDTH, HEIGHT), "black")
draw = ImageDraw.Draw(img)

start = time.time()

for _ in range(NUM_LINES):
    x1 = random.randint(0, WIDTH)
    y1 = random.randint(0, HEIGHT)
    x2 = random.randint(0, WIDTH)
    y2 = random.randint(0, HEIGHT)
    draw.line((x1, y1, x2, y2), fill="white")

end = time.time()

print(f"Software rendering time: {end - start:.4f} seconds")

img.show()
