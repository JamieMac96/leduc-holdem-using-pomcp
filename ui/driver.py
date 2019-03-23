from numpy import random

import util
import evaluator
from ui.agent import Agent

ACTION_MESSAGES = {
    "f": "folded.\n",
    "c": "called.\n",
    "b": "made a bet.\n",
    "r": "made a raise.\n",
    "Ah": "Ah was dealt.\n",
    "As": "As was dealt.\n",
    "Kh": "Kh was dealt.\n",
    "Ks": "Ks was dealt.\n",
    "Qh": "Qh was dealt.\n",
    "Qs": "Qs was dealt.\n"
}

PLAYER_NAMES = {
    1: "Bot ",
    -1: "You "
}


class Driver:
    def __init__(self, strategy="../strategies/Deterministic_200000_random.json"):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""
        self.display_text = "New Game Started\n"
        self.first_to_act = 0
        self.agent = Agent(strategy)
        self.setup_game()

    def setup_game(self):
        self.history = random.choice(util.get_all_initial_chance_actions())

        self.first_to_act = util.get_prefix(self.history)
        self.p1_card = util.get_player_card(self.history, -1)
        self.p2_card = util.get_player_card(self.history, 1)
        if self.first_to_act == 1:
            self.take_agent_action()

    def get_game_state(self):
        return {
            "p1_card": self.p1_card + ".svg",
            "p2_card": self.get_player_two_display_card(),
            "textbox": self.display_text,
            "pot": evaluator.get_pot(self.history),
            "public": self.pub_card,
            "actions": util.get_available_actions(self.history)
        }

    def update_game_state(self, action):
        self.history += action
        self.display_text += PLAYER_NAMES[-1] + ACTION_MESSAGES[action]
        if util.is_terminal(self.history):
            winner = evaluator.get_winner(self.history)
            print(self.history)
            print(winner)
            winnings = abs(evaluator.calculate_reward_full_info(self.history))
            print(winnings)
            self.display_text += "Game over. " + PLAYER_NAMES[winner] + " won: " + str(winnings)
        elif util.player(self.history) == 1:
            self.take_agent_action()
        elif util.player(self.history) == 0:
            self.deal_card()

    def take_agent_action(self):
        action = self.agent.get_action(self.history)
        self.display_text += PLAYER_NAMES[1] + ACTION_MESSAGES[action]
        self.history += action

    def deal_card(self):
        card_dealt = random.choice(util.get_available_cards(self.history))
        self.display_text += ACTION_MESSAGES[card_dealt]
        self.pub_card = card_dealt
        self.history += card_dealt
        if self.first_to_act == 1:
            self.take_agent_action()

    def reset(self):
        self.history = ""
        self.p1_card = ""
        self.p2_card = ""
        self.pub_card = ""
        self.display_text = "New Game Started\n"
        self.first_to_act = 0
        self.setup_game()

    def get_player_two_display_card(self):
        if util.is_terminal(self.history):
            return self.p2_card + ".svg"
        else:
            return "back.png"
