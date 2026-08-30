import arcade
import random
import time

WIDTH = 1200
HEIGHT = 600
NUM_LINES = 5000


class CompareWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "CPU vs GPU Rendering Comparison")

        # -----------------------------
        # LEFT SIDE: Non-batched lines
        # -----------------------------
        self.lines = []
        start = time.time()
        for _ in range(NUM_LINES):
            x1 = random.randint(0, WIDTH // 2)
            y1 = random.randint(0, HEIGHT)
            x2 = random.randint(0, WIDTH // 2)
            y2 = random.randint(0, HEIGHT)
            self.lines.append((x1, y1, x2, y2))
        end = time.time()
        self.cpu_setup_time = end - start

        # -----------------------------
        # RIGHT SIDE: Batched GPU lines
        # -----------------------------
        self.shape_list = arcade.shape_list.ShapeElementList()

        start = time.time()
        for _ in range(NUM_LINES):
            x1 = random.randint(WIDTH // 2, WIDTH)
            y1 = random.randint(0, HEIGHT)
            x2 = random.randint(WIDTH // 2, WIDTH)
            y2 = random.randint(0, HEIGHT)

            line = arcade.shape_list.create_line(
                x1, y1, x2, y2,
                arcade.color.WHITE,
                1,
            )
            self.shape_list.append(line)
        end = time.time()
        self.gpu_setup_time = end - start

        print(f"Non-batched setup time: {self.cpu_setup_time:.4f} seconds")
        print(f"Batched setup time:     {self.gpu_setup_time:.4f} seconds")

        self.fps = 0

    def on_update(self, delta_time):
        self.fps = 1 / delta_time if delta_time > 0 else 0

    def on_draw(self):
        self.clear()

        # -----------------------------
        # Draw LEFT SIDE (non-batched)
        # -----------------------------
        for x1, y1, x2, y2 in self.lines:
            arcade.draw_line(x1, y1, x2, y2, arcade.color.WHITE, 1)

        # -----------------------------
        # Draw RIGHT SIDE (batched)
        # -----------------------------
        self.shape_list.draw()

        # -----------------------------
        # Labels (dark text for visibility)
        # -----------------------------
        arcade.draw_text(
            f"Non-batched (CPU-style)\nSetup: {self.cpu_setup_time:.4f}s",
            10, HEIGHT - 40,
            arcade.color.BLACK, 14
        )

        arcade.draw_text(
            f"Batched GPU\nSetup: {self.gpu_setup_time:.4f}s",
            WIDTH // 2 + 10, HEIGHT - 40,
            arcade.color.BLACK, 14
        )

        arcade.draw_text(
            f"FPS: {self.fps:.1f}",
            WIDTH - 120, 20,
            arcade.color.BLACK, 18
        )


CompareWindow()
arcade.run()
