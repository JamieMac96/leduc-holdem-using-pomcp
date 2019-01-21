import random


class Agent:
    def __init__(self, stack_size=200):
        self.stack_size = stack_size
        self.private_cards = list()
        self.public_cards = list()

    def update_public_cards(self, cards):
        self.public_cards.extend(cards)

    def set_private_cards(self, private):
        self.private_cards = private

    def get_private_cards_str(self):
        return str(self.private_cards[0]) + ", " + str(self.private_cards[1])

    def choose_initial_action(self):
        return random.choice(["bet", "fold"])

    def choose_action(self):
        return random.choice(ACTIONS)

    def add_winnings(self, amount):
        self.stack_size += amount

    def subtract_bet(self):
        pass