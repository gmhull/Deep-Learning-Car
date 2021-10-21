import pyglet
from pyglet.window import key
import numpy as np
import tensorflow as tf
import os
import car, track, neural_net

class GameScreen(pyglet.window.Window):
    car_alive = None

    def __init__(self, car, race_track, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.race_track = race_track
        self.car = car

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

    def on_draw(self):
        self.clear()
        self.race_track.draw_track()
        self.race_track.draw_gates()
        if self.car_alive:
            self.car.draw_car()
            self.car.look(self.race_track.walls)
            if self.car.check_collision(self.race_track.walls):
                self.car_alive = False


class Game:
    OBSERVATION_SPACE_VALUES = 5
    ACTION_SPACE_SIZE = 5

    MOVE_PENALTY = 4
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 200

    MAX_EPISODES = 500
    episode_step = 0

    game_screen = None
    count = 0

    def __init__(self, screen=True, manual=True, model=None):
        self.MANUAL = manual
        self.model = model

        self.race_track = track.Track()
        self.create_car()

        if screen:
            self.create_screen(manual)


    def create_screen(self, manual):
        self.game_screen = GameScreen(fullscreen=True, car=self.car, race_track=self.race_track)
        screen_width, screen_height = self.game_screen.get_size()
        self.game_screen.car_alive = self.car_alive

        # Track key presses
        self.keys = key.KeyStateHandler()
        self.game_screen.push_handlers(self.keys)

        if manual:
            pyglet.clock.schedule_interval(self.update, 1/120.0)
        else:
            pyglet.clock.schedule_interval(self.auto_update, 1/120.0)

        pyglet.app.run()

    def create_car(self):
        if self.MANUAL:
            self.car = car.ManualCar()
        else:
            self.car = car.AutoCar()
        self.car.REWARD_GATES = self.race_track.reward_gates
        self.score = 0
        self.car_alive = True
        if self.game_screen != None:
            self.game_screen.car = self.car
            self.game_screen.car_alive = self.car_alive

    def reset(self):
        # print(self.score)
        del self.car
        self.create_car()
        self.episode_step = 0

        return self.car.look(self.race_track.walls)

    def update(self, dt):
        print(self.car.SPACE_STATE[-1])
        reward = self.get_reward()
        self.score += reward
        if self.game_screen.car_alive:
            self.game_screen.car.controls(self.keys)
        elif self.game_screen.car_alive == False:
            self.reset()

    def auto_update(self, dt):
        if self.game_screen.car_alive:
            action = np.argmax(self.model.predict(np.array([self.game_screen.car.SPACE_STATE,]))[0])
            if np.random.random() < 0.01:
                action = np.random.randint(0, self.ACTION_SPACE_SIZE)
            # print(action)
            self.car.SPACE_STATE, reward, done = self.step(action)

        self.score += reward

        if self.game_screen.car_alive == False or done:
            self.reset()

    def get_reward(self):
        if not self.car.ALIVE:
            reward = -self.CRASH_PENALTY
        elif self.car.update_score():
            reward = self.CHECKPOINT_REWARD
        else:
            reward = -self.MOVE_PENALTY

        return reward

    def step(self, action, training=False):
        self.episode_step += 1
        self.car.controls(action)
        if self.car.check_collision(self.race_track.walls):
            self.car_alive = False

        if training:
            reward = self.get_reward()
        else:
            reward = 0

        done = False
        if self.car.ALIVE == False:
            done = True
        elif training == True and self.episode_step >= self.MAX_EPISODES:
            done = True
        return self.car.SPACE_STATE, reward, done


def test():
    model = get_model()
    if model == None:
        print("No model was found.")
        return

    game = Game(manual=False, model=model)

def train(EPISODES, AGGREGATE_STATS_EVERY):
    model = get_model()

    neural_net.training(EPISODES, AGGREGATE_STATS_EVERY, model=model)

def play():
    game = Game()

def get_model():
    try:
        model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[0])
        print('models\\'+os.listdir('models\\')[0])
        print("ready to rock")
    except:
        model = None
        print('you messed up')

    return model


if __name__ == "__main__":
    # train(3000, 50)
    # test()
    play()
