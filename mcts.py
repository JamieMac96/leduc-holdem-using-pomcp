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
iterations_list = []
exploitability_values = list()


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
            if i % 1000 == 0 and i != 0:
                value = strategy_evaluator.calculate_exploitability(player_tree)
                exploitability_values.append(-value)
                iterations_list.append(i)
    else:
        raise ValueError("You must specify a time or iterations limit")


def rollout(history, out_of_tree):
    if util.player(history) == 0:
        action = str(environment.dealer.deal_public())
    else:
        action = rollout_policy(util.get_available_actions(history))
    new_history = history + action
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
        action = rollout_policy(util.get_available_actions(history))
        out_of_tree = True
    else:
        ensure_node_is_expanded(history)
        action = get_best_action_ucb(history)
    new_history = history + action
    running_reward = util.calculate_reward(history, environment) + DISCOUNT_FACTOR * simulate(new_history, out_of_tree)
    add_new_history(history, new_history)
    update(history, new_history, running_reward)

    return running_reward


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
    if len(player_tree[history].children) != len(util.get_available_actions(history)):
        expand(history)


def get_best_action_ucb(history):
    if util.player(history) == -1:
        return random.choice(util.get_available_actions(history))
    elif util.player(history) == 1:
        best_value = float('-inf')
        best_action = None
        for action in util.get_available_actions(history):
            next_history = history + action
            exploration_bonus = EXPLORATION_CONSTANT * \
                            math.sqrt(math.log(player_tree[history].visitation_count) /
                                      player_tree[next_history].visitation_count)
            node_val = player_tree[next_history].value + exploration_bonus
            if node_val >= best_value:
                best_action = action
                best_value = node_val
        return best_action
    else:
        return str(environment.dealer.deal_public())


def expand(history):
    if history not in player_tree:
        player_tree[history] = potree.PoNode()

    for action in util.get_available_actions(history):
        new_history = history + action
        if new_history not in player_tree:
            player_tree[new_history] = potree.PoNode()
        player_tree[history].children.add(new_history)


if __name__ == "__main__":
    iteration_count = 1000000
    num_searches = 1
    sbn.set_style("darkgrid")
    list_of_rewards = list()
    for i in range(num_searches):
        environment.rewards = list()
        environment.cumulative_reward = 0
        environment.count = 0
        environment.indices = list()
        player_tree = {"": potree.PoNode()}
        search("", iterations=iteration_count)
        list_of_rewards.append(environment.rewards)

    avg_rewards = list()
    reward_sum = 0
    # for i in range(len(environment.indices)):
    #    for reward in list_of_rewards:
    #        reward_sum += reward[i]
    #    avg_rewards.append(reward_sum / num_searches)
    #    reward_sum = 0
    for i in range(20):
        exploitability_values.pop(i)
        iterations_list.pop(i)
    for i in range(len(exploitability_values)):
        print("iteration: " + str(iterations_list[i]))
        print("exploitability: " + str(exploitability_values[i]))
        print("-------------------------------------------------------")
    plt.plot(iterations_list, exploitability_values)
    plt.xlabel("Iterations")
    plt.ylabel("Exploitability")

    plt.show()
    util.print_tree(player_tree)
    print("NUMBER OF ITERATIONS: " + str(iteration_count))
