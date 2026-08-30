import arcade
import random
import time

WIDTH = 800
HEIGHT = 600
NUM_LINES = 5000


class LineWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "GPU Rendering with ShapeElementList")

        # Create a ShapeElementList (GPU batch)
        self.shape_list = arcade.shape_list.ShapeElementList()

        start = time.time()

        # Generate 5000 random lines and add them to the batch
        for _ in range(NUM_LINES):
            x1 = random.randint(0, WIDTH)
            y1 = random.randint(0, HEIGHT)
            x2 = random.randint(0, WIDTH)
            y2 = random.randint(0, HEIGHT)

            # Create a GPU line shape
            line = arcade.shape_list.create_line(
                x1, y1, x2, y2,
                arcade.color.WHITE,
                1,
            )

            # Add to the batch
            self.shape_list.append(line)

        end = time.time()
        print(f"CPU setup time: {end - start:.4f} seconds")

    def on_draw(self):
        # Clear screen
        self.clear()

        # Draw all 5000 lines in one GPU batch call
        self.shape_list.draw()


LineWindow()
arcade.run()
