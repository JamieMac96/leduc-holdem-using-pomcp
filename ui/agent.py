import random
import json


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
            num_choices = 0

            for key, value in self.strategy[history].items():
                candidates.append(key)
                probabilities.append(value)
                num_choices += 1

            draw = random.choice(candidates, num_choices, p=probabilities)
            return draw
        else:
            return self.strategy[history]
