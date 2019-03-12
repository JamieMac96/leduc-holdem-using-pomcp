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
        self.round = 1
        self.current_player = -self.button
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 2  # initial blinds for each round are 2
        self.dealer = Dealer()
        self.player_card = self.dealer.deal_private()[0]
        self.opponent_card = self.dealer.deal_private()[1]
        self.public_card = None
        self.debug = debug
        self.cumulative_reward = 0
        self.count = 0
        self.rewards = list()
        self.indices = list()
        self.last_action = None

    # updates the state of the game.
    # Returns the observation and reward received, if there is
    # no observation/reward then we return empty string/none
    def update_state(self, action):
        if action == "f":
            self.count += 1
            self.indices.append(self.count)
        elif action == "c":
            self.pot += self.get_bet_amounts()
            self.current_player = -self.button
            if self.round == 1:
                self.round += 1
                self.last_action = None
                self.num_bets_this_round = 0
                self.public_card = self.dealer.deal_public()
                return self.public_card.__str__()
            else:
                self.count += 1
                self.indices.append(self.count)
        elif action == "b":
            self.num_bets_this_round += 1
            self.current_player *= -1
            self.pot += self.get_bet_amounts()
        elif action == "r":
            self.num_bets_this_round += 1
            self.current_player *= -1
            self.pot += self.get_bet_amounts()
        return ""

    def get_possible_actions(self):
        return BETS_ACTIONS_MAP[self.num_bets_this_round]

    def get_bet_amounts(self):
        if self.round == 1:
            return 2
        elif self.round == 2:
            return 4

    def random_policy(self):
        return random.choice(self.get_possible_actions())

    def get_initial_state_player(self):
        return str(-self.button) + str(self.player_card)

    def get_initial_state_public(self):
        return str(-self.button) + str(self.player_card) + str(self.opponent_card)

    def reset(self):
        self.button *= -1
        self.round = 1
        self.current_player = -self.button
        self.num_bets_this_round = 0
        self.moves_record = list()
        self.pot = 2
        self.dealer.reset()
        self.player_card = self.dealer.deal_private()[0]
        self.opponent_card = self.dealer.deal_private()[1]
        self.public_card = None
        self.last_action = None


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
