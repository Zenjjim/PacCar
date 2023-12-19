import torch
import random
import numpy as np
from collections import deque
from game import Game
from model import Linear_QNet, QTrainer
from utils import plot
from car import Car

MAX_MEMORY = 10000
BATCH_SIZE = 1000
LR = 0.00003
DISCOUNT_RATE = 0.95
LEARNING_ROUNDS = 1_000
EXPLORATION_DECAY = 0.0001

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class Agent:
    def __init__(self, input_shape) -> None:
        print("DEVICE", device)
        self.n_games = 0
        self.epsilon = 1 # randomness
        self.gamma = DISCOUNT_RATE # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(input_shape, 256, 3).to(device)
        self.trainer = QTrainer(self.model, LR, self.gamma)

    def get_state(self, game, car):
        return game.get_state(car)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = self.epsilon * np.exp(-0.0001)
        final_move = [0, 0, 0]
        if random.random() < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            # predict action based on the old state
            state_tens = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state_tens)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = float("-inf")
    cars = [Car() for i in range(5)]
    game = Game()
    agent = Agent(input_shape = game.get_state(cars[0]).shape[0])

    while True:
        best_car = max(cars, key=lambda x: x.score)
        game.run(best_car)

        for car in cars:
            if car.dead:
                continue
            state_old = agent.get_state(game, car)
            # get move
            final_move = agent.get_action(state_old)
            # get new state
            reward, done, score = game.update(final_move, car)
            if best_car == car:
                car.draw_coin_vector(game.screen, game.coins)
                car.generate_sensors(game.screen, game.lines)
                car.draw(game.screen, best=True)
            else:
                car.draw(game.screen)
            state_new = agent.get_state(game, car)
            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
            # remember
            agent.remember(state_old, final_move, reward, state_new, done)

        game.flip()
        
        reset = True
        for car in cars:
            if not car.dead:
                reset = False
                break
        if reset:
            # train long memory
            print("RESETTING")
            for car in cars:
                car.reset()
                agent.n_games += len(cars)
                agent.train_long_memory()

                if score > record:
                    record = score
                    agent.model.save()
                
                print("Game", agent.n_games, "Score", score, "Record", record)

                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
            print("ALL RESET")
            
if __name__ == "__main__":
    train()