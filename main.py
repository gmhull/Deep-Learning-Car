import pyglet
from pyglet.window import key
import numpy as np
# import tensorflow as tf
import os
import car, game
# import neural_net

class GameScreen(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keys = None
        self.game = game.Game()

    def on_mouse_press(self, x, y, button, modifiers):
        print(x, y)

    def on_draw(self):
        self.clear()
        self.game.car.draw_car()
        for wall in self.game.walls:
            wall.draw()
        self.game.car.draw_reward_gate()
        self.game.car.draw_next_check_dir()

    def update(self, dt, keys):
        self.game.car.update(keys)

# class OLD_Game:
#     OBSERVATION_SPACE_VALUES = 5
#     ACTION_SPACE_SIZE = 5
#
#     MOVE_PENALTY = 4
#     CRASH_PENALTY = 1000
#     CHECKPOINT_REWARD = 200
#
#     MAX_EPISODES = 500
#     episode_step = 0
#
#     game_screen = None
#     count = 0
#
#     def __init__(self, screen=True, manual=True, model=None):
#         self.MANUAL = manual
#         self.model = model
#
#         # Initialize the track
#         self.race_track = track.Track()
#         # Initialize the car
#         self.create_car()
#
#         if screen:
#             self.create_screen(manual)
#
#
#
#     def reset(self):
#         # print(self.score)
#         del self.car
#         self.create_car()
#         self.episode_step = 0
#
#         return self.car.get_current_state(self.race_track.walls)
#
#
#
#     def get_reward(self):
#         if not self.car.alive:
#             reward = -self.CRASH_PENALTY
#         elif self.car.update_score():
#             reward = self.CHECKPOINT_REWARD
#         else:
#             reward = -self.MOVE_PENALTY
#
#         return reward
#
#     def step(self, action, training=False):
#         self.episode_step += 1
#         self.car.controls(action)
#         if self.car.check_collision(self.race_track.walls):
#             self.car_alive = False
#
#         if training:
#             reward = self.get_reward()
#         else:
#             reward = 0
#
#         done = False
#         if self.car.ALIVE == False:
#             done = True
#         elif training == True and self.episode_step >= self.MAX_EPISODES:
#             done = True
#         return self.car.SPACE_STATE, reward, done


# def test():
#     model = get_model()
#     if model == None:
#         print("No model was found.")
#         return
#
#     game = Game(manual=False, model=model)
#
# def train(EPISODES, AGGREGATE_STATS_EVERY):
#     model = get_model()
#
#     neural_net.training(EPISODES, AGGREGATE_STATS_EVERY, model=model)
#
# def play():
#     game = Game()
#
# def get_model():
#     try:
#         model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[0])
#         print('models\\'+os.listdir('models\\')[0])
#         print("ready to rock")
#     except:
#         model = None
#         print('you messed up')
#
#     return model


if __name__ == "__main__":
    # train(3000, 50)
    # test()
    # play()
    game_screen = GameScreen(fullscreen=True, resizable=False)

    keys = key.KeyStateHandler()
    game_screen.push_handlers(keys)

    pyglet.clock.schedule_interval(game_screen.update, 1/120.0, keys)
    pyglet.app.run()
