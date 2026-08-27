import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_grass():
    arcade.draw_lrbt_rectangle_filled(
        0, SCREEN_WIDTH,
        0, SCREEN_HEIGHT / 3,
        arcade.color.AIR_SUPERIORITY_BLUE
    )


def draw_snow_person(x, y):
    arcade.draw_point(x, y, arcade.color.RED, 5)

    arcade.draw_circle_filled(x, 60 + y, 60, arcade.color.WHITE)
    arcade.draw_circle_filled(x, 140 + y, 50, arcade.color.WHITE)
    arcade.draw_circle_filled(x, 200 + y, 40, arcade.color.WHITE)

    arcade.draw_circle_filled(x - 15, 210 + y, 5, arcade.color.BLACK)
    arcade.draw_circle_filled(x + 15, 210 + y, 5, arcade.color.BLACK)


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing with Functions")
        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.snow_person1_x = 150

    def on_draw(self):
        self.clear()  # <-- THIS IS THE CORRECT WAY TO CLEAR THE SCREEN
        draw_grass()
        draw_snow_person(self.snow_person1_x, 140)
        draw_snow_person(450, 180)

    def on_update(self, delta_time):
        self.snow_person1_x += 1


def main():
    game = MyGame()
    arcade.run()


main()
