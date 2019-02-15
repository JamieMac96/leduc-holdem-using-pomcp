from pycfr.card import Card
import random
from pycfr import hand_evaluator

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
        self.reward = 0
        self.cumulative_reward = 0
        self.count = 0
        self.rewards = list()
        self.indices = list()

    # updates the state of the game.
    # Returns the observation and reward received, if there is
    # no observation/reward then we return empty string/none
    def update_state(self, action):
        if action == "f":
            self.game_over = True
            self.reward = -self.pot*self.current_player
            self.cumulative_reward += self.reward
            self.rewards.append(self.cumulative_reward)
            self.count += 1
            self.indices.append(self.count)
            return "O", self.reward
        elif action == "c":
            self.pot += self.get_bet_amounts()
            self.current_player = -self.button
            if self.round == 1:
                self.round += 1
                self.num_bets_this_round = 0
                self.public_card = self.dealer.deal_public()
                return self.public_card.__str__(), 0
            else:
                self.game_over = True
                self.reward = self.get_showdown_reward()
                self.cumulative_reward += self.reward
                self.rewards.append(self.cumulative_reward)
                self.count += 1
                self.indices.append(self.count)
                return "O", self.reward
        elif action == "b":
            self.num_bets_this_round += 1
            self.current_player *= -1
            self.pot += self.get_bet_amounts()
        elif action == "r":
            self.num_bets_this_round += 1
            self.current_player *= -1
            self.pot += self.get_bet_amounts()
        return "", 0

    def get_possible_actions(self):
        if self.game_over:
            return []
        if self.num_bets_this_round == 0:
            return ["f", "b"]
        elif self.num_bets_this_round == 1:
            return ["f", "c", "r"]
        elif self.num_bets_this_round == 2:
            return ["f", "c"]

    def get_bet_amounts(self):
        if self.round == 1:
            return 2
        elif self.round == 2:
            return 4

    def random_policy(self):
        return random.choice(self.get_possible_actions())

    def get_initial_state(self):
        return str(-self.button) + str(self.player_card)

    def get_showdown_reward(self):
        pc = self.player_card
        oc = self.opponent_card
        pub = self.public_card
        if self.debug:
            print("CARDS AT SHOWDOWN: ")
            print("p: " + repr(pc))
            print("o: " + repr(oc))
            print("pub: " + repr(pub))

        hand_player = [pc, pub]
        hand_opponent = [oc, pub]
        player_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_player)
        opp_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_opponent)

        if player_val >= opp_val:
            reward = self.pot
        else:
            reward = -self.pot
        return reward

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
