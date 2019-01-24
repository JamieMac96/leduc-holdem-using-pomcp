from pycfr.card import Card
from leduc.state import Action
import random

# In Leduc hold’em, the deck consists of two suits
# with three cards in each suit. There are two rounds. In the
# first round a single private card is dealt to each player. In
# the second round a single board card is revealed. There is
# a two-bet maximum, with raise amounts of 2 and 4 in the
# first and second round, respectively. Both players start the
# first round with 1 already in the pot

# Note for the purpose of this game, a call with a bet value of 0
# is considered equivalent to checking
ACTIONS = ["FOLD", "CALL", "BET", "RAISE"]


class Game:
    def __init__(self):
        self.round = 1
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 0
        self.game_over = False
        self.dealer = Dealer()
        self.player_card = None
        self.opponent_card = None
        self.public_card = None

    def update_state(self, action):
        if action.action == "FOLD":
            self.game_over = True

        elif action.action == "CALL":
            self.pot += action.bet_amount
            if self.round == 1:
                self.round += 1
                self.num_bets_this_round = 0
                self.public_card = self.dealer.deal_public()
            else:
                self.game_over = True
        elif action.action == "BET":
            self.pot += action.bet_amount
            self.num_bets_this_round += 1

        elif action.action == "RAISE":
            self.num_bets_this_round += 1
            self.pot += action.bet_amount * 2

    def get_possible_actions(self):
        if self.game_over:
            return []
        amount = self.get_bet_amounts()
        if self.num_bets_this_round == 0:
            return [Action("FOLD"), Action("BET", amount)]
        elif self.num_bets_this_round == 1:
            return [Action("FOLD"), Action("CALL", amount), Action("RAISE", amount)]
        elif self.num_bets_this_round == 2:
            return [Action("FOLD"), Action("CALL", amount)]

    def get_bet_amounts(self):
        if self.round == 1:
            return 2
        elif self.round == 2:
            return 4

    def random_policy(self):
        return random.choice(self.get_possible_actions())

    def reset(self):
        self.round = 1
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 0
        self.game_over = False
        self.dealer.reset()
        self.player_card = None
        self.opponent_card = None
        self.public_card = None


class Dealer:
    def __init__(self):
        self.deck = [Card(13, 1), Card(13, 2), Card(12, 1), Card(12, 2), Card(11, 1), Card(11, 2)]
        random.shuffle(self.deck)

    def deal_private(self):
        return self.deck[0], self.deck[1]

    def deal_public(self):
        return self.deck[3]

    def reset(self):
        random.shuffle(self.deck)
