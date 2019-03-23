from numpy.random import choice
import json
from pprint import pprint


class Agent:
    def __init__(self, strategy_file):
        self.strategy = self.load_strategy(strategy_file)

    def load_strategy(self, filename):
        with open(filename) as f:
            strategy = json.load(f)

        return strategy

    def get_action(self, history):
        if isinstance(self.strategy[history], dict):
            candidates = []
            probabilities = []

            for key, value in self.strategy[history].items():
                candidates.append(key)
                probabilities.append(value)

            draw = choice(candidates, p=probabilities)
            return draw
        else:
            return self.strategy[history]