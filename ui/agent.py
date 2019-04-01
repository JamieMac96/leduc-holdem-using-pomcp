from numpy.random import choice
import json

import util


def load_strategy(filename):
    with open(filename) as f:
        strategy = json.load(f)

    return strategy


# This class takes a strategy and returns the behavior associated
# with that strategy based on calls to the get_action method
class Agent:
    def __init__(self, strategy_file):
        self.strategy = load_strategy(strategy_file)

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