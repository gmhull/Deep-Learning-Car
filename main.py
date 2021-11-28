import pyglet
from pyglet.window import key
import numpy as np
import tensorflow as tf
import os, math
import car, game
import neural_net

class GameScreen(pyglet.window.Window):
    def __init__(self, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = None
        if not model:
            self.game = game.Game()
            self.manual = True
        else:
            self.game = TrainingAgent(model)
            self.manual = False

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
        # for r in self.game.reward_gates:
        #     r.draw()
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

    MOVE_PENALTY = 3
    STOPPED_PENALTY = 50
    CRASH_PENALTY = 1000
    CHECKPOINT_REWARD = 100

    MAX_EPISODES = 500
    episode_step = 0
    epsilon = 0.01

    def __init__(self, model):
        self.game = game.Game(manual=False)

        self.model = model

    def step(self, action, training=False):
        self.episode_step += 1
        self.game.car.update(action, training)

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

            if np.random.random() > self.epsilon:
                action = np.argmax(model_output)
            else:
                action = np.random.randint(0, self.ACTION_SPACE_SIZE)
        except:
            action = np.random.randint(0, self.ACTION_SPACE_SIZE)
            print(action)

        return action

    def reset(self):
        self.episode_step = 0
        return self.game.reset()

    def get_reward(self, done):
        if done:
            reward = -self.CRASH_PENALTY
        elif self.game.car.update_score():
            reward = self.CHECKPOINT_REWARD
        elif self.game.car.speed == 0:
            reward = -self.STOPPED_PENALTY
        else:
            reward = -self.MOVE_PENALTY * (1.5-round(self.game.car.speed/7.6, 1))

        reward -= abs(self.game.car.next_gate_angle)

        return reward


def test():
    model = get_model()
    if model == None:
        print("You need a model to test.")
        return

    game_screen = GameScreen(model=model, fullscreen=True, resizable=False)

    pyglet.clock.schedule_interval(game_screen.auto_update, 1/120.0)
    pyglet.app.run()

def play():
    game_screen = GameScreen(fullscreen=True, resizable=False)

    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    pyglet.clock.schedule_interval(game_screen.update, 1/120.0, keys)
    pyglet.app.run()

def get_model():
    try:
        model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[0])
        print('models\\'+os.listdir('models\\')[0])
        print("ready to rock")
    except:
        model = None
        print("Ain't no model here")

    return model


if __name__ == "__main__":
    test()
    # play()
