import util


class Game:
    def __init__(self):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""

    def get_initial_cards(self):
        self.history = util.get_all_initial_chance_actions()

        p1_card = util.get_player_card(self.history, 1)
