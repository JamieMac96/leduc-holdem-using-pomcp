from card import Card
import random

# In Leduc hold’em, the deck consists of two suits
# with three cards in each suit. There are two rounds. In the
# first round a single private card is dealt to each player. In
# the second round a single board card is revealed. There is
# a two-bet maximum, with raise amounts of 2 and 4 in the
# first and second round, respectively. Both players start the
# first round with 1 already in the pot

# f = fold
# b = bet
# C = call
# r = raise
BETS_ACTIONS_MAP = {
    0: ["f", "b"],
    1: ["f", "c", "r"],
    2: ["f", "c"]
}


class Game:
    def __init__(self, debug=False):
        self.button = -1
        self.current_player = -self.button
        self.dealer = Dealer()
        self.player_card = self.dealer.deal_private()[0]
        self.opponent_card = self.dealer.deal_private()[1]
        self.public_card = None
        self.debug = debug

    def get_initial_state_player(self):
        return str(-self.button) + str(self.player_card)

    def get_initial_state_public(self):
        return str(-self.button) + str(self.player_card) + str(self.opponent_card)

    def reset(self):
        self.button *= -1
        self.current_player = -self.button
        self.dealer.reset()
        self.player_card = self.dealer.deal_private()[0]
        self.opponent_card = self.dealer.deal_private()[1]
        self.public_card = None


class Dealer:
    def __init__(self):
        self.deck = [Card(14, 1), Card(14, 2), Card(13, 1), Card(13, 2), Card(12, 1), Card(12, 2)]
        random.shuffle(self.deck)

    def deal_private(self):
        return self.deck[0], self.deck[1]

    def deal_public(self):
        return self.deck[3]

    def reset(self):
        random.shuffle(self.deck)
