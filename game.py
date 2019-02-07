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
    def __init__(self, debug=False):
        self.button = -1
        self.round = 1
        self.current_player = -self.button
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 2  # initial blinds for each round are 2
        self.game_over = False
        self.dealer = Dealer()
        self.player_card = self.dealer.deal_private()[0]
        self.opponent_card = self.dealer.deal_private()[1]
        self.public_card = None
        self.debug = debug

    def update_state(self, action):
        if action.action == "FOLD":
            self.game_over = True

        elif action.action == "CALL":
            self.pot += action.bet_amount
            self.current_player = 1
            if self.round == 1:
                self.round += 1
                self.num_bets_this_round = 0
                self.public_card = self.dealer.deal_public()
            else:
                self.game_over = True
        elif action.action == "BET":
            self.current_player *= -1
            self.pot += action.bet_amount
            self.num_bets_this_round += 1

        elif action.action == "RAISE":
            self.current_player *= -1
            self.num_bets_this_round += 1
            self.pot += action.bet_amount

    def get_possible_actions(self):
        if self.game_over:
            return []
        amount = self.get_bet_amounts()
        if self.num_bets_this_round == 0:
            return [Action(1, "BET", amount)]
        elif self.num_bets_this_round == 1:
            return [Action(-1, "FOLD"),
                    Action(-1, "CALL", amount),
                    Action(-1, "RAISE", amount)]
        elif self.num_bets_this_round == 2:
            return [Action(1, "FOLD"), Action(1, "CALL", amount)]

    def get_bet_amounts(self):
        if self.round == 1:
            return 2
        elif self.round == 2:
            return 4

    def random_policy(self):
        return random.choice(self.get_possible_actions())

    def reset(self):
        self.button *= -1
        self.round = 1
        self.current_player = -self.button
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 2
        self.game_over = False
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
