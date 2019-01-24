from pycfr import hand_evaluator
from pycfr.card import Card
import random


class LeducState:

    # Note that we assume that the history is composed of
    # actions and observations, with the observations
    # following the actions within the history list.
    # For example:
    #  - [a1, o1, a2, o2, a3, o3...] and so on
    def __init__(self, history, game, reward=None, is_terminal=False):
        self.history = history
        self.environment = game
        self.reward = reward
        self.is_terminal = is_terminal

    def get_possible_actions(self):
        return self.environment.get_possible_actions()

    def take_action(self, action):
        # If (mcts) player folds:
        # - Hand is over
        # - Reward rendered is the -half the pot
        # - Environment is reset
        # - Return the state
        # If player calls:
        # - Round is incremented, bet added to pot etc
        # - mcts player is next to act TODO: Store the player that is first to act
        # - add action to the history and create the new state
        # If player bets:
        # - action added to history
        # - random opponent acts
        # - observation created based on opponents action, observation added to history
        # -
        # If player raises:
        # - action added to history
        # - random opponent must act next
        # - observation made based on opponents actions
        # - observation added to history
        # -
        if action in self.environment.get_possible_actions():
            if action.action == "FOLD":
                return self.get_state_after_fold(action)
            elif action.action == "CALL":
                return self.get_state_after_call(action)
            elif action.action == "BET":
                return self.get_state_after_bet(action)
            elif action == "RAISE":
                return self.get_state_after_raise(action)
        else:
            raise InvalidActionException("The action chosen is not allowed in this state")

    # Possible application of state design pattern?
    def get_reward(self):
        # only needed for terminal states
        if not self.is_terminal:
            raise InvalidStateException("Cannot retrieve reward from non terminal state")
        else:
            return self.reward

    def get_state_after_fold(self, action):
        self.environment.update_state(action)
        reward = -self.environment.pot
        self.environment.reset()
        return self.get_terminal_state(Action("Fold"), reward)

    def get_state_after_call(self, action):
        self.environment.update_state(action)
        if self.environment.game_over:
            reward = self.get_showdown_reward()
            self.environment.reset()
            return self.get_terminal_state(action, reward)
        else:
            return self.get_default_next_state(action, self.history.copy())

    def get_state_after_bet(self, action):
        self.environment.update_state(action)

        new_observation = Observation(action, self.environment.round,
                                      self.environment.player_card,
                                      self.environment.public_card)
        next_history = self.history.copy() + [action, new_observation]

        # Allow random opponent to make move
        random_action = random.choice(self.get_possible_actions())
        self.environment.update_state(random_action)

        if random_action.action == "FOLD":
            reward = self.environment.pot
            self.environment.reset()
            return self.get_terminal_state(random_action, reward)
        elif random_action.action == "CALL":
            if not self.environment.game_over:
                return self.get_default_next_state(random_action, next_history)
            else:
                reward = self.get_showdown_reward()
                self.environment.reset()
                return self.get_terminal_state(random_action, reward)
        elif random_action.action == "RAISE":
            return self.get_default_next_state(random_action, next_history)

        else:
            raise InvalidActionException("The action " + action.action
                                         + " was not expected here")

    def get_state_after_raise(self, action):
        self.environment.update_state(action)
        return self.get_default_next_state(action, self.history.copy())

    def get_showdown_reward(self):
        pc = self.environment.player_card
        oc = self.environment.opponent_card
        pub = self.environment.public_card
        if pub is None:
            print("PUB NONE")
        if pc is None:
            print("PC NONE")
        if oc is None:
            print("OC NONE")
        hand_player = [pc, pub]
        hand_opponent = [oc, pub]
        player_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_player)
        opp_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_opponent)

        if player_val >= opp_val:
            reward = self.environment.pot
        else:
            reward = -self.environment.pot

        return reward

    def get_terminal_state(self, action, reward):
        history_copy = self.history.copy()
        terminal_observation = Observation(None, None, None)
        next_history = history_copy + [action, terminal_observation]
        return LeducState(next_history, self.environment,
                          reward=reward, is_terminal=True)

    def get_default_next_state(self, action, history):
        next_observation = Observation(action, self.environment.round,
                                       self.environment.player_card,
                                       self.environment.public_card)
        history += [action, next_observation]
        return LeducState(history, self.environment)

    def __eq__(self, other):
        raise NotImplementedError()


class Observation:
    def __init__(self, action, round_num, private, public=None):
        self.private = private
        self.action = action
        self.round_num = round_num
        self.public = public
        self.observed_set = {private, action, round_num, public}

    def __eq__(self, other):
        return self.observed_set == other.observed_set


class Action:
    def __init__(self, action, bet_amount=None):
        self.action = action
        self.bet_amount = bet_amount

    def __eq__(self, other):
        return other.action == self.action and other.bet_amount == self.bet_amount

    def __hash__(self):
        return hash((self.action, self.bet_amount))


class InvalidStateException(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidActionException(Exception):
    def __init__(self, message):
        super().__init__(message)
