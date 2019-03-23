from numpy import random

import util
from ui.agent import Agent


class Driver:
    def __init__(self, strategy="../strategies/Deterministic_200000_random.json"):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""
        self.first_to_act = 0
        self.setup_game()
        self.agent = Agent(strategy)

    def setup_game(self):
        self.history = random.choice(util.get_all_initial_chance_actions())

        self.first_to_act = util.get_prefix(self.history)
        self.p1_card = util.get_player_card(self.history, 1)
        self.p2_card = util.get_player_card(self.history, -1)

    def get_game_state(self):
        pass

    def update_game_state(self, action):
        pass

    def reset(self):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""
        self.first_to_act = 0
        self.setup_game()