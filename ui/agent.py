from numpy.random import choice
import json

import util


class Agent:
    def __init__(self, strategy_file):
        self.strategy = self.load_strategy(strategy_file)

    def load_strategy(self, filename):
        with open(filename) as f:
            strategy = json.load(f)

        return strategy

    def get_action(self, history):
        player_history = util.information_function(history, 1)
        if isinstance(self.strategy[player_history], dict):
            candidates = []
            probabilities = []

            for key, value in self.strategy[player_history].items():
                candidates.append(key)
                probabilities.append(value)

            action_choice = choice(candidates, p=probabilities)
            return action_choice
        else:
            return self.strategy[player_history]