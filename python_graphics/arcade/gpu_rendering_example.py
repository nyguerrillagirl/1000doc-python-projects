import arcade
import random
import time

WIDTH = 800
HEIGHT = 600
NUM_LINES = 5000

class LineWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "GPU Rendering Example")
        self.lines = []
        self.start_time = time.time()

        for _ in range(NUM_LINES):
            x1 = random.randint(0, WIDTH)
            y1 = random.randint(0, HEIGHT)
            x2 = random.randint(0, WIDTH)
            y2 = random.randint(0, HEIGHT)
            self.lines.append((x1, y1, x2, y2))

        self.end_time = time.time()
        print(f"Setup time (CPU): {self.end_time - self.start_time:.4f} seconds")

    def on_draw(self):
        self.clear()
        for x1, y1, x2, y2 in self.lines:
            arcade.draw_line(x1, y1, x2, y2, arcade.color.WHITE, 1)

window = LineWindow()
arcade.run()
