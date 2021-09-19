import pyglet
from pyglet.window import key
import car, track

class GameScreen(pyglet.window.Window):
    def draw_me(self):
        pass

def update(dt):
    car.controls(keys)

MANUAL = True

if __name__ == "__main__":
    # Initialize the screen
    game_screen = GameScreen(fullscreen=True)
    screen_width, screen_height = game_screen.get_size()

    # Initialize the car
    if MANUAL:
        car = car.ManualCar()
    else:
        car = car.AutoCar()

    race_track = track.Track()

    # Track key presses
    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    @game_screen.event
    def on_draw():
        game_screen.clear()
        car.draw_car()
        print(race_track.walls)
        car.look(race_track.walls)
        race_track.draw_track()

    pyglet.clock.schedule_interval(update, 1/120.0)

    pyglet.app.run()
