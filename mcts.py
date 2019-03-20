import metrics
import potree
import util
import evaluator

import math
import random

DISCOUNT_FACTOR = .95
EXPLORATION_CONSTANT = 50
m_metrics = metrics.Metrics()
player_one_tree = {}  # Root node of tree
player_two_tree = {}  # Player 2 aka player -1
iterations_list = []
OUT_OF_TREE = {1: False, 0: False, -1: False}


def simulate(history):
    player_tree = get_tree(util.player(history))
    if util.is_terminal(history):
        return handle_terminal_state(history)

    player = util.player(history)
    if OUT_OF_TREE[player]:
        return rollout(history)

    player_history = util.information_function(history, player)
    if player_history in player_tree:
        action = get_best_action_ucb(history)
    else:
        expand(player_one_tree, history, 1)
        expand(player_two_tree, history, -1)
        action = rollout_policy(util.get_available_actions(history))
        if player != 0:
            OUT_OF_TREE[1] = True
            OUT_OF_TREE[-1] = True

    new_history = history + action
    running_reward = evaluator.calculate_reward_full_info(history) + DISCOUNT_FACTOR * simulate(new_history)
    update_player_tree(history, action, 1, running_reward)
    update_player_tree(history, action, -1, running_reward)

    return running_reward


def rollout(history):
    action = rollout_policy(util.get_available_actions(history))
    new_history = history + action
    return simulate(new_history)


def rollout_policy(actions):
    try:
        actions.remove("f")
    except ValueError:
        pass
    return random.choice(actions)


def update(tree, history, new_history, running_reward):
    if history not in tree or new_history not in tree:
        return
    tree[history].visitation_count += 1
    tree[new_history].visitation_count += 1
    tree[new_history].value += (running_reward - tree[new_history].value) / tree[new_history].visitation_count


def get_best_action_ucb(history):
    player = util.player(history)
    player_history = util.information_function(history, player)
    if player == -1:
        return random.choice(util.get_available_actions(history))
    if player in {-1, 1}:
        tree = get_tree(player)
        best_value = float('-inf')
        best_action = None
        for action in util.get_available_actions(history):
            next_history = history + action
            if next_history not in tree:
                new_visitation_count = 1
                new_value = 0
            else:
                new_visitation_count = tree[next_history].visitation_count
                new_value = tree[next_history].value * player
            exploration_bonus = EXPLORATION_CONSTANT * \
                            math.sqrt(math.log(tree[player_history].visitation_count + 1) /
                                      new_visitation_count)
            node_val = new_value + exploration_bonus
            if node_val > best_value:
                best_action = action
                best_value = node_val
        return best_action
    else:
        return random.choice(util.get_available_actions(history))


def update_player_tree(history, action, player, reward):
    player_history = util.information_function(history, player)
    new_player_history = util.information_function(str(history + action), player)
    update(get_tree(player), player_history, new_player_history, reward)


def handle_terminal_state(history):
    reward = evaluator.calculate_reward_full_info(history)
    m_metrics.cumulative_reward += reward
    m_metrics.rewards.append(m_metrics.cumulative_reward)
    reset_out_of_tree()
    return reward


def get_tree(player):
    if player == 1:
        return player_one_tree
    elif player == -1:
        return player_two_tree
    else:
        return []


def expand(tree, history, player):
    player_history = util.information_function(history, player)
    if player_history not in tree:
        tree[player_history] = potree.PoNode()

    for action in util.get_available_actions(history):
        new_history = util.information_function(history + action, player)
        if new_history not in tree:
            tree[new_history] = potree.PoNode()
        tree[player_history].children.add(new_history)


def reset_out_of_tree():
    OUT_OF_TREE[0] = False
    OUT_OF_TREE[1] = False
    OUT_OF_TREE[-1] = False

