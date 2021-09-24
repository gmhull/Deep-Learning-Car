import pyglet
from pyglet.window import key
import car, track

class GameScreen(pyglet.window.Window):
    car_alive = None

    def __init__(self, car, race_track, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.race_track = race_track
        self.car = car

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

    def on_draw(self):
        # if self.car == 'ManualCar':
        self.clear()
        # print(self.car_alive)
        self.race_track.draw_track()
        if self.car_alive:
            self.car.draw_car()
            self.car.look(self.race_track.walls)
            if self.car.check_collision(self.race_track.walls):
                self.car_alive = False


class Game:
    OBSERVATION_SPACE_VALUES = 5
    ACTION_SPACE_SIZE = 6

    MOVE_PENALTY = 1
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 100

    MAX_EPISODES = 500
    episode_step = 0

    game_screen = None
    count = 0

    def __init__(self, screen=True):
        self.MANUAL = screen

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
        self.episode_step = 0

        return self.car.look(self.race_track.walls)

    def update(self, dt):
        if self.game_screen.car_alive:
            self.game_screen.car.controls(self.keys)
        elif self.game_screen.car_alive == False:
            self.reset()

    def step(self, action, training=False):
        self.episode_step += 1
        self.car.controls(action)
        if self.car.check_collision(self.race_track.walls):
            self.car_alive = False

        if training:
            if not self.car.ALIVE:
                reward = -self.CRASH_PENALTY
            elif self.car.update_score():
                reward = self.CHECKPOINT_REWARD
            else:
                reward = -self.MOVE_PENALTY
        else:
            reward = 0

        done = False
        if self.car.ALIVE == False:
            done = True
        elif training == True and self.episode_step >= self.MAX_EPISODES:
            done = True
        return self.car.SPACE_STATE, reward, done


if __name__ == "__main__":
    game = Game()
