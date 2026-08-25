import arcade

window = arcade.Window(title="Arcade tutorials")
#window.set_location(400, 200)
window.center_window()

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

game = GameView()
window.show_view(game)
arcade.run()