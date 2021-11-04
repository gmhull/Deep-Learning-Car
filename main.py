import pyglet
from pyglet.window import key
import numpy as np
# import tensorflow as tf
import os
import car, game
import neural_net

class GameScreen(pyglet.window.Window):
    def __init__(self, manual=True, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = None
        if manual:
            self.game = game.Game(manual=manual)
        else:
            self.game = TrainingAgent()
        self.manual = manual

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

    def on_draw(self):
        if self.manual:
            self.draw_screen()
        else:
            self.auto_draw_screen()

    def draw_screen(self):
        self.clear()
        self.game.car.draw_car()
        for wall in self.game.walls:
            wall.draw()
        self.game.car.draw_reward_gate()
        # self.game.car.draw_next_check_dir()

    def auto_draw_screen(self):
        self.clear()
        self.game.game.car.draw_car()
        for wall in self.game.game.walls:
            wall.draw()
        self.game.game.car.draw_reward_gate()
        # self.game.game.car.draw_next_check_dir()

    def update(self, dt, keys):
        self.game.car.update(keys)

    def auto_update(self, dt):
        action = self.game.get_action()
        self.game.step(action)


class TrainingAgent:
    OBSERVATION_SPACE_VALUES = 7
    ACTION_SPACE_SIZE = 6

    MOVE_PENALTY = 2
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 100

    MAX_EPISODES = 600
    episode_step = 0

    def __init__(self):
        self.model = self.get_model()

        self.game = game.Game(manual=False)

    def get_model(self):
        try:
            model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[0])
            print('models\\'+os.listdir('models\\')[0])
            print("ready to rock")
        except:
            model = None
            print("Ain't no model here")

        return model

    def step(self, action, training=False):
        self.episode_step += 1
        self.game.car.update(action)

        done = False
        if self.game.car.alive == False:
            done = True
        elif training == True and self.episode_step >= self.MAX_EPISODES:
            done = True

        reward = self.get_reward(done)

        return self.game.car.SPACE_STATE, reward, done

    def get_action(self):
        try:
            model_output = self.model.predict(np.array([self.game.car.SPACE_STATE,]))[0]

            if np.random.random() > epsilon:
                action = np.argmax(model_output)
            else:
                action = np.random.randint(0, self.ACTION_SPACE_SIZE)
        except:
            action = np.random.randint(0, self.ACTION_SPACE_SIZE)

        return action

    def reset(self):
        self.episode_step = 0
        return self.game.reset()

    def get_reward(self, done):
        if done:
            reward = -self.CRASH_PENALTY
        elif self.game.car.update_score():
            reward = self.CHECKPOINT_REWARD
        else:
            reward = -self.MOVE_PENALTY

        return reward


def test():
    game_screen = GameScreen(manual=False, fullscreen=True, resizable=False)

    pyglet.clock.schedule_interval(game_screen.auto_update, 1/120.0)
    pyglet.app.run()

def play():
    game_screen = GameScreen(fullscreen=True, resizable=False)

    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    pyglet.clock.schedule_interval(game_screen.update, 1/120.0, keys)
    pyglet.app.run()


if __name__ == "__main__":
    # test()
    play()
