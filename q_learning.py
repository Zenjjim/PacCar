import numpy as np
import random

class QLearningAgent:
    def __init__(self, state_bins, actions, alpha, gamma, epsilon, buffer_size=10000, batch_size=32, replay_frequency=10):
        self.state_bins = state_bins
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.buffer = []
        self.buffer_size = buffer_size
        self.batch_size = batch_size
        self.replay_frequency = replay_frequency
        # Initialize Q-table as a nested dictionary
        self.q_table = {}
        for state in self.get_all_states():
            self.q_table[state] = {action: 0 for action in actions}

    def discretize_state(self, state):
        discretized_state = []
        for value, bins in zip(state, self.state_bins):
            discretized_state.append(np.digitize(value, bins))
        return tuple(discretized_state)

    def get_all_states(self):
        all_states = [[]]
        for bins in self.state_bins:
            all_states = [state + [i] for state in all_states for i in range(len(bins) + 1)]
        return [tuple(state) for state in all_states]

    def choose_action(self, state):
        discretized_state = self.discretize_state(state)

        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        else:
            return max(self.q_table[discretized_state], key=self.q_table[discretized_state].get)

    def update(self, state, action, reward, next_state):
        # Add experience to buffer
        self.buffer.append((state, action, reward, next_state))

        # Update Q-table from buffer every replay_frequency steps
        if len(self.buffer) % self.replay_frequency == 0:
            if len(self.buffer) >= self.batch_size:
                batch = random.sample(self.buffer, self.batch_size)
                for state, action, reward, next_state in batch:
                    discretized_state = self.discretize_state(state)
                    discretized_next_state = self.discretize_state(next_state)
                    current_q = self.q_table[discretized_state][action]
                    max_future_q = max(self.q_table[discretized_next_state].values())
                    new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
                    self.q_table[discretized_state][action] = new_q

        # Choose next action
        if random.uniform(0, 1) < self.epsilon:
            next_action = random.choice(self.actions)
        else:
            discretized_next_state = self.discretize_state(next_state)
            next_action = max(self.q_table[discretized_next_state], key=self.q_table[discretized_next_state].get)

        # Decay epsilon
        self.epsilon *= 0.99

        return next_action

    def replay(self, batch_size):
        # Sample a batch of experiences from the buffer
        batch = random.sample(self.buffer, batch_size)

        for state, action, reward, next_state in batch:
            # Update the Q-value for the selected action and state
            discretized_state = self.discretize_state(state)
            discretized_next_state = self.discretize_state(next_state)

            current_q = self.q_table[discretized_state][action]
            max_future_q = max(self.q_table[discretized_next_state].values())

            new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
            self.q_table[discretized_state][action] = new_q