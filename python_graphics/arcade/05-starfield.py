import random

import arcade
import random

window = arcade.Window(title="Arcade tutorials")
window.center_window()

# background star color
bg_star_color = (255, 255, 255, 95)

# foreground star colors
fg_star_colors = [arcade.color.WHITE, arcade.color.BABY_BLUE, arcade.color.AQUA,
                  arcade.color.BUFF, arcade.color.ALIZARIN_CRIMSON]


# This function creates the stars, and adds them to the ShapeElementList (batch).
def create_starfield(batch: arcade.shape_list.ShapeElementList,
                     color=bg_star_color, random_color=False):
    for i in range(200):
        x = random.randint(0, 1280)
        y = random.randint(0, 720)
        w = random.randint(1, 3)
        h = random.randint(1, 3)

        if random_color:
            color = random.choice(fg_star_colors)

        star = arcade.shape_list.create_rectangle_filled(x, y, w, h, color)
        batch.append(star)


class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

        # first foreground stars
        self.fg_stars1 = arcade.shape_list.ShapeElementList()
        create_starfield(self.fg_stars1, random_color=True)
    def on_draw(self) -> None:
        self.clear()

    def on_update(selfself, delta_time: float) -> None:
        pass

game = GameView()
window.show_view(game)
arcade.run()