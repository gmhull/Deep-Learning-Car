import pyglet
from pyglet.window import key
import car, track

class GameScreen(pyglet.window.Window):
    car_alive = None

    def __init__(self, car, race_track, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.race_track = race_track
        self.car = car

    # def on_mouse_press(self, x, y, button, modifiers):
    #     print(x, y)

    def on_draw(self):
        self.clear()
        # print(self.car_alive)
        self.race_track.draw_track()
        if self.car_alive:
            self.car.draw_car()
            self.car.look(self.race_track.walls)
            if self.car.check_collision(self.race_track.walls):
                self.car_alive = False


class Game:
    MANUAL = True
    OBSERVATION_SPACE_VALUES = 5
    ACTION_SPACE_SIZE = 6

    MOVE_PENALTY = 1
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 100

    game_screen = None

    def __init__(self, screen=True):
        self.create_car()
        self.race_track = track.Track()

        if screen:
            # Initialize the screen
            self.game_screen = GameScreen(fullscreen=True, car=self.car, race_track=self.race_track)
            screen_width, screen_height = self.game_screen.get_size()
            self.game_screen.car_alive = self.car_alive

            # Track key presses
            self.keys = key.KeyStateHandler()
            self.game_screen.push_handlers(self.keys)

            pyglet.clock.schedule_interval(self.update, 1/120.0)

            pyglet.app.run()

    def create_car(self):
        if self.MANUAL:
            self.car = car.ManualCar()
        else:
            self.car = car.AutoCar()
        self.car_alive = True
        if self.game_screen != None:
            self.game_screen.car = self.car
            self.game_screen.car_alive = self.car_alive

    def reset(self):
        del self.car
        self.create_car()

    def update(self, dt):
        if self.game_screen.car_alive:
            self.game_screen.car.controls(self.keys)
        elif self.game_screen.car_alive == False:
            self.reset()


if __name__ == "__main__":
    game = Game()
