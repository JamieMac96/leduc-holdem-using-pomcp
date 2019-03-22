import random

import util


class Game:
    def __init__(self):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""
        self.button = 0

    def get_initial_cards(self):
        self.history = random.choice(util.get_all_initial_chance_actions())

        self.button = -util.get_prefix(self.history)
        self.p1_card = util.get_player_card(self.history, 1)
        self.p2_card = util.get_player_card(self.history, -1)