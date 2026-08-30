import arcade

window = arcade.Window(title="Arcade tutorials")
window.center_window()

class GameView(arcade.View):
    def __init__(self) -> None:
        super().__init__()

    def on_draw(self) -> None:
        self.clear()

    def on_update(selfself, delta_time: float) -> None:
        pass

game = GameView()
window.show_view(game)
arcade.run()