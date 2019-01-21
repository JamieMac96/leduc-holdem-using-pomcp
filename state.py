class LeducState:

    # Note that we assume that the history is composed of
    # actions and observations, with the observations
    # following the actions within the history list.
    # For example:
    #  - [a1, o1, a2, o2, a3, o3...] and so on
    def __init__(self, history, possible_actions, reward=None):
        self.history = history
        self.possible_actions = possible_actions
        self.reward = reward

    def get_possible_actions(self):
        return self.possible_actions

    def take_action(self, action):
        raise NotImplementedError()

    def is_terminal(self):
        return self.possible_actions == []

    # Possible application of state design pattern?
    # How to do this in pythonic fashion?
    def get_reward(self):
        # only needed for terminal states
        if not self.is_terminal():
            raise InvalidStateException("Cannot get reward from non terminal state")
        else:
            return self.reward

    def __eq__(self, other):
        raise NotImplementedError()


class Observation:
    def __init__(self, action, round_num, private, public=None):
        self.private = private
        self.action = action
        self.round_num = round_num
        self.public = public
        self.observed_set = {private, action, round_num, public}

class Action:
    def __init__(self, action, bet_amount=None):
        self.action = action
        self.bet_amount = bet_amount


class InvalidStateException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)