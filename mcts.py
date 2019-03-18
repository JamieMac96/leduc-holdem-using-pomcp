import time
import math
import random
import seaborn as sbn
import game
import potree
import util
import strategy_evaluator

DISCOUNT_FACTOR = .95
EPSILON = .01
EXPLORATION_CONSTANT = 50
environment = game.Game()
player_one_tree = {"": potree.PoNode()}  # Root node of tree
player_two_tree = {"": potree.PoNode()}  # Player 2 aka player -1
iterations_list = []
exploitability_values = list()
OUT_OF_TREE = {1: False, 0: False, -1: False}


def rollout_policy(actions):
    if not actions:
        return str(environment.dealer.deal_public())

    return random.choice(actions)


def search(history, time_limit=None, iterations=None):
    if time_limit is not None:
        time_limit = time.time() + time_limit / 1000
        while time.time() < time_limit:
            simulate(history)
            reset_out_of_tree()
    elif iterations is not None:
        for i in range(iterations):
            simulate(history)
            reset_out_of_tree()
            if i % 1000 == 0 and i != 0:
                pass
                # value = strategy_evaluator.calculate_exploitability(player_one_tree)
                # exploitability_values.append(-value)
                # iterations_list.append(i)
    else:
        raise ValueError("You must specify a time or iterations limit")


def rollout(history):
    if util.player(history) == 0:
        action = str(environment.dealer.deal_public())
    else:
        action = rollout_policy(util.get_available_actions(history))
    new_history = history + action
    return simulate(new_history)


def simulate(history):
    player = util.player(history)
    if util.is_terminal(history):
        reward = util.calculate_reward(history, environment)
        environment.reset()
        environment.cumulative_reward += reward
        environment.rewards.append(environment.cumulative_reward)
        environment.indices.append(environment.count)
        environment.count += 1
        return reward
    if OUT_OF_TREE[player]:
        return rollout(history)
    if history == "":
        return handle_initial_node()

    player_history = util.information_function(history, player)
    player_tree = get_tree(player)
    if not player_tree or player_history in player_tree:
        ensure_node_is_expanded(history)
        action = get_best_action_ucb(player_history)
    else:
        expand(get_tree(player), player_history)
        action = rollout_policy(util.get_available_actions(history))
        OUT_OF_TREE[player] = True

    new_history = history + action
    running_reward = util.calculate_reward(player_history, environment) + DISCOUNT_FACTOR * simulate(new_history)
    ensure_node_is_expanded(history)
    update_player_tree(history, action, 1, running_reward)
    update_player_tree(history, action, -1, running_reward)

    return running_reward


def add_new_history(player_tree, history, new_history):
    if new_history not in player_one_tree.keys():
        player_tree[new_history] = potree.PoNode()
        player_tree[new_history].visitation_count = 1
    player_tree[history].children.add(new_history)


def update_player_tree(history, action, player, reward):
    player_history = util.information_function(history, player)
    new_player_history = player_history + action
    add_new_history(get_tree(player), player_history, new_player_history)
    update(get_tree(player), player_history, new_player_history, reward)


def update(tree, history, new_history, running_reward):
    tree[history].visitation_count += 1
    tree[new_history].visitation_count += 1
    tree[new_history].value += (running_reward - tree[new_history].value) / tree[new_history].visitation_count


def handle_initial_node():
    new_history = environment.get_initial_state()
    add_initial_chance_node(player_one_tree, 1, new_history)
    add_initial_chance_node(player_two_tree, -1, new_history)
    return simulate(new_history)


def add_initial_chance_node(tree, player, history):
    new_player_history = util.information_function(history, player)
    tree[new_player_history] = potree.PoNode()
    tree[""].children.add(new_player_history)


def ensure_node_is_expanded(history):
    player_one_history = util.information_function(history, 1)
    player_two_history = util.information_function(history, -1)
    expand(player_one_tree, player_one_history)
    expand(player_two_tree, player_two_history)


def set_out_of_tree(player):
    OUT_OF_TREE[player] = True


def get_tree(player):
    if player == 1:
        return player_one_tree
    elif player == -1:
        return player_two_tree
    else:
        return []


def get_best_action_ucb(history):
    if util.player(history) == -1:
        return random.choice(util.get_available_actions(history))
    elif util.player(history) == 1:
        best_value = float('-inf')
        best_action = None
        for action in util.get_available_actions(history):
            next_history = history + action
            exploration_bonus = EXPLORATION_CONSTANT * \
                            math.sqrt(math.log(player_one_tree[history].visitation_count + 1) /
                                      player_one_tree[next_history].visitation_count)
            node_val = player_one_tree[next_history].value + exploration_bonus
            if node_val > best_value:
                best_action = action
                best_value = node_val
        return best_action
    else:
        return str(environment.dealer.deal_public())


def expand(tree, history):
    if history not in tree:
        tree[history] = potree.PoNode()

    for action in util.get_available_actions(history):
        new_history = history + action
        if new_history not in tree:
            tree[new_history] = potree.PoNode()
        tree[history].children.add(new_history)


def reset_out_of_tree():
    OUT_OF_TREE = {1: False, 0: False, -1: False}


if __name__ == "__main__":
    iteration_count = 200000
    num_searches = 1
    sbn.set_style("darkgrid")
    list_of_rewards = list()
    for i in range(num_searches):
        environment.rewards = list()
        environment.cumulative_reward = 0
        environment.count = 0
        environment.indices = list()
        player_one_tree = {"": potree.PoNode()}
        search("", iterations=iteration_count)
        list_of_rewards.append(environment.rewards)

    avg_rewards = list()
    reward_sum = 0
    for i in range(len(environment.indices)):
        for reward in list_of_rewards:
            reward_sum += reward[i]
        avg_rewards.append(reward_sum / num_searches)
        reward_sum = 0
    # for i in range(20):
    #    exploitability_values.pop(i)
    #    iterations_list.pop(i)

    slope_values = list()
    slope_indices = list()

    for i in range(len(avg_rewards)):
        if i % 1000 == 0 and i != 0:
            slope = (avg_rewards[i] - avg_rewards[i-1000]) / 1000
            slope_indices.append(i)
            slope_values.append(slope)

    # util.show_graph(iterations_list, exploitability_values, "Iterations", "Exploitability")
    # util.show_graph(environment.indices, avg_rewards, "Iterations", "Cumulative Reward")
    # util.show_graph(slope_indices, slope_values, "Iterations", "Slope - Cumulative Reward")
    util.print_tree(player_one_tree)
    util.manual_traverse_tree(player_one_tree)
    print("NUMBER OF ITERATIONS: " + str(iteration_count))
