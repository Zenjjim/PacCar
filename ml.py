import random
import numpy as np
import pygame
import utils
from utils import preprocess_input
import q_learning

IF_ML = True

class ML:
    def __init__(self, games, game_obj = None):
        self.games = games
        self.values = None
        self.game_obj = game_obj
        self.highest_score = 0
        self.counter = 0
        if self.game_obj is None:
            self.games[0].hidden = False
        else:
            self.game_obj.hidden = False

        num_bins = 10
        state_bins = [np.linspace(0, 10, num_bins), np.linspace(0, 8, num_bins)]
        alpha = 0.1    # Learning rate, usually between 0 and 1
        gamma = 0.99   # Discount factor, usually between 0 and 1
        self.epsilon = 1.0  # Exploration rate, starting at 1.0 for full exploration
        self.epsilon_decay = 1.0
        self.min_epsilon = 0.01
        self.q_agent = q_learning.QLearningAgent(state_bins, ["up", "down", "left", "right"], alpha, gamma, self.epsilon)


    def update(self):
        for game in self.games:
            if IF_ML:
                state = utils.preprocess_input(game.ml_values())
                action = self.q_agent.choose_action(state)
                self.ml_stear_game(game, action)
            else:
                self.control_with_keys(game)
            
            game.update()
            
            if IF_ML:
                reward = game.reward()
                next_state = utils.preprocess_input(game.ml_values())
                self.q_agent.update(state, action, reward, next_state)
            
            if game.physics_obj.is_reset:
                game.reset()

        self.epsilon = max(self.epsilon * self.epsilon_decay, self.min_epsilon)
    
    def control_with_keys(self, game):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            game.control("up")
        if keys[pygame.K_DOWN]:   
            game.control("down")
        if keys[pygame.K_LEFT]:  
            game.control("left")
        if keys[pygame.K_RIGHT]:  
            game.control("right")
        
    
    def draw(self, window):
        for game in self.games:
            game.draw(window)

    def reset(self):
        for game in self.games:
            game.reset()

    def ml_stear_game(self, game_obj, action):
        game_obj.control(action)
        

