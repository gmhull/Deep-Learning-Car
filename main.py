import pyglet
from pyglet.window import key
import car, track

class GameScreen(pyglet.window.Window):
    MANUAL = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.MANUAL:
            self.car = car.ManualCar()
        else:
            self.car = car.AutoCar()

        self.race_track = track.Track()

    def on_draw(self):
        self.clear()
        self.car.draw_car()
        self.car.look(self.race_track.walls)
        self.race_track.draw_track()

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)


def update(dt):
    game_screen.car.controls(keys)

if __name__ == "__main__":
    # Initialize the screen
    game_screen = GameScreen(fullscreen=True)
    screen_width, screen_height = game_screen.get_size()

    # Initialize the car



    # Track key presses
    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    pyglet.clock.schedule_interval(update, 1/120.0)

    pyglet.app.run()
