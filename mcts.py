import time
import math
from leduc import sim
from leduc import game

discount_factor = .99
epsilon = .001
tree = {}
visitation_function = {}
value_function = {}
environment = game.Game()


def search(history, time_limit=None, iterations=None):
    if time_limit is not None:
        time_limit = time.time() + time_limit / 1000
        while time.time() < time_limit:
            execute_round(history, 0)
    elif iterations is not None:
        for i in range(iterations):
            execute_round(history, 0)
    else:
        raise ValueError("You must specify a time or iterations limit")
    return None  # TODO: argmax(V(hb))


def execute_round(history, depth):
    if not history:
        state = None  # TODO: acquire state from information state function
    else:
        state = None  # TODO: action state from belief state function
    simulate(history, state, depth)


def rollout(state, history, depth):
    if math.pow(discount_factor, depth) < epsilon:
        return 0
    action = None  # TODO: Use rollout policy to acquire action
    new_state, observation, reward = sim.generate_successor_tuple(state, action)
    new_history = history + [action, observation]
    return reward + rollout(new_state, new_history, depth+1)


def simulate(state, history, depth):
    if math.pow(discount_factor, depth) < epsilon:
        return 0
    if history not in tree.keys():
        for action in environment.get_possible_actions():
            new_history = history + [action]
            tree[new_history] = None  # TODO: apply default initial values to new history
        return rollout(state, history, depth)

    action = None  # TODO: argmax(V(hb) + c * sqrt(log(N(h))/N(hb)))
    new_state, observation, reward = sim.generate_successor_tuple(state, action)
    new_history = history + [action, observation]
    reward_update = reward + simulate(new_state, new_history, depth+1)
    new_belief_state = None  # TODO: B(h) = B(h) U {s}
    visitation_function[history] += 1
    visitation_function[new_history] += 1
    value_function[new_history] += (reward_update - value_function[new_history]) / visitation_function[new_history]
    return reward_update

