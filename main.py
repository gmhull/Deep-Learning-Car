import pyglet
from pyglet.window import key
import car

class GameScreen(pyglet.window.Window):
    def draw_me(self):
        pass

def update(dt):
    car.controls(keys)

MANUAL = True

if __name__ == "__main__":
    # Initialize the screen
    game_screen = GameScreen(fullscreen=True)
    # Initialize the car
    if MANUAL:
        car = car.ManualCar(angle=0)
    else:
        car = car.AutoCar(angle=0)
    # Track key presses
    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    @game_screen.event
    def on_draw():
        game_screen.clear()
        car.draw_car()

    pyglet.clock.schedule_interval(update, 1/120.0)

    pyglet.app.run()
