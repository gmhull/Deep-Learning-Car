# Holds the neural network used for deep q learning.

import numpy as np
import random
from PIL import Image
import ctypes
import cv2
import matplotlib.pyplot as plt
import pickle
import time
from matplotlib import style
import tensorflow as tf
from keras.layers import *
from keras.callbacks import TensorBoard
from collections import deque
import os
import track
import car
import main


class NeuralNetwork:
    REPLAY_MEMORY_SIZE = 50_000
    MIN_REPLAY_MEMORY_SIZE = 1_000
    MEMORY_FRACTION = 0.20
    MINIBATCH_SIZE = 64
    DISCOUNT = 0.99
    UPDATE_TARGET_EVERY = 5

    def __init__(self, env):
        self.env = env

        self.learning_rate = 0.001

        # Create the target model. What we predict against each step
        self.model = self.create_model()

        # Create the target model. What we predict against each step
        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=self.REPLAY_MEMORY_SIZE)

        # self.tensorboard = ModifiedTensorBoard(log_dir=f'logs/{MODEL_NAME}-{int(time.time())}')

        self.target_update_counter = 0

    def create_conv_model(self):
        model = tf.keras.models.Sequential()
        model.add(Conv2D(256, (3, 3), input_shape=self.env.OBSERVATION_SPACE_VALUES))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.2))

        model.add(Conv2D(256, (3, 3)))
        model.add(Activation('relu'))
        model.add(MaxPooling2D(2,2))
        model.add(Dropout(0.2))

        model.add(Flatten())
        model.add(Dense(24, activation='relu'))

        model.add(Dense(self.env.ACTION_SPACE_SIZE,activation="linear"))
        model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate), metrics=['accuracy'])
        return model

    def create_model(self):
        model = tf.keras.models.Sequential()
        model.add(Input(shape=self.env.OBSERVATION_SPACE_VALUES))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.env.ACTION_SPACE_SIZE, activation="linear"))
        model.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(lr=self.learning_rate), metrics=['accuracy'])
        return model

    def train(self, terminal_state, step):

        # Start training only if certain number of samples is already saved
        if len(self.replay_memory) < self.MIN_REPLAY_MEMORY_SIZE:
            return

         # Get a minibatch of random samples from memory replay table
        minibatch = random.sample(self.replay_memory, self.MINIBATCH_SIZE)

        # Get current states from minibatch, then query NN model for Q values
        current_states = np.array([transition[0] for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        # Get future states from minibatch, then query NN model for Q values
        # When using target network, query it, otherwise main network should be queried
        new_current_states = np.array([transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        X = []
        y = []

        # Now we need to enumerate our batches
        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            # If not a terminal state, get new q from future states, otherwise set it to 0
            # almost like with Q Learning, but we use just part of equation here
            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + self.DISCOUNT * max_future_q
            else:
                new_q = reward

            # Update Q value for given state
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            # And append to our training data
            X.append(current_state)
            y.append(current_qs)

        # Fit on all samples as one batch, log only on terminal state
        self.model.fit(np.array(X), np.array(y), batch_size=self.MINIBATCH_SIZE, verbose=0, shuffle=False)

        # Update target network counter every episode
        if terminal_state:
            self.target_update_counter += 1

        # If counter reaches set value, update target network with weights of main network
        if self.target_update_counter > self.UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(np.array([state,]))[0]


def training(EPISODES, AGGREGATE_STATS_EVERY, model=False):
    style.use('ggplot')
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    epsilon = 1
    EPS_DECAY = 0.9975
    MIN_EPSILON = 0.001
    MODEL_NAME = "Car_Brain"
    MIN_REWARD = 1000

    env = main.Game(screen=False, manual=False)

    ep_rewards = []
    aggr_ep_rewards = {'ep': [], 'avg': [], 'min': [], 'max': []}

    # random.seed(1)
    # np.random.seed(1)
    # tf.random.set_seed(1)

    agent = NeuralNetwork(env)

    if model:
        agent.model = model

    for episode in range(1, EPISODES+1):
        episode_reward = 0
        step = 1
        current_state = env.reset()
        done = False

        while not done:
            if np.random.random() > epsilon:
                action = np.argmax(agent.get_qs(current_state))
            else:
                action = np.random.randint(0, env.ACTION_SPACE_SIZE)

            new_state, reward, done = env.step(action, training=True)

            episode_reward += reward

            agent.update_replay_memory((current_state, action, reward, new_state, done))

            agent.train(done, step)

            current_state = new_state
            step += 1

        # print(episode_reward)
        ep_rewards.append(episode_reward)
        if not episode % AGGREGATE_STATS_EVERY or episode == 1:
            average_reward = sum(ep_rewards[-AGGREGATE_STATS_EVERY:])/len(ep_rewards[-AGGREGATE_STATS_EVERY:])
            min_reward = min(ep_rewards[-AGGREGATE_STATS_EVERY:])
            max_reward = max(ep_rewards[-AGGREGATE_STATS_EVERY:])
            aggr_ep_rewards['ep'].append(episode)
            aggr_ep_rewards['avg'].append(average_reward)
            aggr_ep_rewards['min'].append(min_reward)
            aggr_ep_rewards['max'].append(max_reward)
            print(f'Episode: {episode:>5d}, average reward: {average_reward:>4.1f}, current epsilon: {epsilon:>1.2f}, Min: {min_reward}, Max: {max_reward}')

            if min_reward > MIN_REWARD or episode == EPISODES:
                agent.model.save(f'models/{MODEL_NAME}__{max_reward:_>7.2f}max_{average_reward:_>7.2f}avg_{min_reward:_>7.2f}min__{int(time.time())}.model')

        if epsilon > MIN_EPSILON:
            epsilon *= EPS_DECAY
            epsilon = max(MIN_EPSILON, epsilon)

    print(aggr_ep_rewards)
    print("EP_REWARDS ", ep_rewards)
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['avg'], label='average')
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['min'], label='minimum')
    plt.plot(aggr_ep_rewards['ep'], aggr_ep_rewards['max'], label='maximum')
    plt.legend(loc=4)
    plt.show()

if __name__ == '__main__':
    try:
        model = tf.keras.models.load_model('models\\'+os.listdir('models\\')[0])
        print('models\\'+os.listdir('models\\')[0])
        print("ready to rock")
    except:
        model = False
        print('you messed up')

    training(1000, 100, model=model)
