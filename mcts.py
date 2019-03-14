import time
import math
import random
from matplotlib import pyplot as plt
import seaborn as sbn
import game
import potree
import util
import strategy_evaluator

DISCOUNT_FACTOR = .95
EPSILON = .01
EXPLORATION_CONSTANT = 18
environment = game.Game()
player_tree = {"": potree.PoNode()}  # Root node of tree


def rollout_policy(actions):
    return random.choice(actions)


def search(history, time_limit=None, iterations=None):
    if time_limit is not None:
        time_limit = time.time() + time_limit / 1000
        while time.time() < time_limit:
            simulate(history)
    elif iterations is not None:
        for i in range(iterations):
            simulate(history)
    else:
        raise ValueError("You must specify a time or iterations limit")


def rollout(history, out_of_tree):
    if not environment.get_possible_actions():
        return 0
    action = rollout_policy(environment.get_possible_actions())
    observation = environment.update_state(action)
    new_history = history + action + observation
    return simulate(new_history, out_of_tree)


def simulate(history, out_of_tree=False):
    if util.is_terminal(history):
        reward = util.calculate_reward(history, environment)
        environment.reset()
        environment.cumulative_reward += reward
        environment.rewards.append(environment.cumulative_reward)
        return reward
    if out_of_tree:
        return rollout(history, out_of_tree)
    if history == "":
        return handle_initial_states()
    if history not in player_tree:
        expand(history)
        action = rollout_policy(environment.get_possible_actions())
        out_of_tree = True
    else:
        ensure_node_is_expanded(history)
        action = get_best_action_ucb(history)

    new_history = get_next_history(history, action)
    running_reward = util.calculate_reward(history, environment) + DISCOUNT_FACTOR * simulate(new_history, out_of_tree)
    add_new_history(history, new_history)
    update(history, new_history, running_reward)

    return running_reward


def get_next_history(history, action):
    observation = environment.update_state(action)
    new_history = history + action + observation
    return new_history


def add_new_history(history, new_history):
    if new_history not in player_tree.keys():
        player_tree[new_history] = potree.PoNode()
        player_tree[new_history].visitation_count = 1
    player_tree[history].children.add(new_history)


def update(history, new_history, running_reward):
    player_tree[history].visitation_count += 1
    player_tree[new_history].visitation_count += 1
    player_tree[new_history].value += (running_reward - player_tree[new_history].value) / player_tree[new_history].visitation_count


def handle_initial_states():
    new_history = environment.get_initial_state_player()
    player_tree[new_history] = potree.PoNode()
    player_tree[""].children.add(new_history)
    return simulate(new_history)


def ensure_node_is_expanded(history):
    if len(player_tree[history].children) != len(environment.get_possible_actions()):
        expand(history)


# TODO: Change this function so that we are including
# TODO: observations in next possible actions
# TODO: eg 1Ahbr would have children:
# TODO:     - 1AhbrcQh, 1AhbrcAs etc
# TODO: not just 1Ahbrc, 1Ahbrf
def get_best_action_ucb(history):
    if environment.current_player == -1:
        return random.choice(environment.get_possible_actions())
    else:
        best_value = float('-inf')
        best_action = None
        for action in environment.get_possible_actions():
            next_history = history + action
            exploration_bonus = EXPLORATION_CONSTANT * \
                            math.sqrt(math.log(player_tree[history].visitation_count) /
                                      player_tree[next_history].visitation_count)
            node_val = player_tree[next_history].value + exploration_bonus
            if node_val >= best_value:
                best_action = action
                best_value = node_val
        return best_action


def expand(history):
    if history not in player_tree:
        player_tree[history] = potree.PoNode()

    for action in environment.get_possible_actions():
        new_history = history + action
        if new_history not in player_tree:
            player_tree[new_history] = potree.PoNode()
        player_tree[history].children.add(new_history)


if __name__ == "__main__":
    iterations = 100000
    num_searches = 1
    sbn.set_style("darkgrid")
    list_of_rewards = list()
    for i in range(num_searches):
        environment.rewards = list()
        environment.cumulative_reward = 0
        environment.count = 0
        environment.indices = list()
        player_tree = {"": potree.PoNode()}
        search("", iterations=iterations)
        list_of_rewards.append(environment.rewards)

    avg_rewards = list()
    reward_sum = 0
    # for i in range(len(environment.indices)):
    #    for reward in list_of_rewards:
    #        reward_sum += reward[i]
    #    avg_rewards.append(reward_sum / num_searches)
    #    reward_sum = 0

    # plt.plot(environment.indices, avg_rewards)
    # plt.xlabel("Iterations")
    # plt.ylabel("Cumulative reward")

    # plt.show()
    util.print_tree(player_tree)
    print("NUMBER OF ITERATIONS: " + str(iterations))

    strategy_evaluator.calculate_exploitability(player_tree)
