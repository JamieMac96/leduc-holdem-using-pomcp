import metrics
import potree
import util
import evaluator

import math
import random

m_metrics = metrics.Metrics()
player_one_tree = {}  # Root node of tree
player_two_tree = {}  # Player 2 aka player -1


class Mcts:
    def __init__(self, discount_factor=.95, exploration_constant=50):
        self.discount_factor = discount_factor
        self.exploration_constant = exploration_constant
        self.out_of_tree = {1: False, -1: False, 0: False}

    def simulate(self, history):
        player_tree = get_tree(util.player(history))
        if util.is_terminal(history):
            return self.handle_terminal_state(history)

        player = util.player(history)
        if self.out_of_tree[player]:
            return self.rollout(history)

        player_history = util.information_function(history, player)
        if player_history in player_tree:
            action = self.get_best_action_ucb(history)
        else:
            expand(player_one_tree, history, 1)
            expand(player_two_tree, history, -1)
            action = rollout_policy(util.get_available_actions(history))
            if player != 0:
                self.out_of_tree[1] = True
                self.out_of_tree[-1] = True

        new_history = history + action
        running_reward = evaluator.calculate_reward_full_info(history) + self.discount_factor * self.simulate(new_history)
        update_player_tree(history, action, 1, running_reward)
        update_player_tree(history, action, -1, running_reward)

        return running_reward

    def rollout(self, history):
        action = rollout_policy(util.get_available_actions(history))
        new_history = history + action
        return self.simulate(new_history)

    def reset_out_of_tree(self):
        self.out_of_tree[0] = False
        self.out_of_tree[1] = False
        self.out_of_tree[-1] = False

    def handle_terminal_state(self, history):
        reward = evaluator.calculate_reward_full_info(history)
        m_metrics.cumulative_reward += reward
        m_metrics.rewards.append(m_metrics.cumulative_reward)
        self.reset_out_of_tree()
        return reward

    def get_best_action_ucb(self, history):
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
                exploration_bonus = self.exploration_constant * \
                                math.sqrt(math.log(tree[player_history].visitation_count + 1) /
                                          new_visitation_count)
                node_val = new_value + exploration_bonus
                if node_val > best_value:
                    best_action = action
                    best_value = node_val
            return best_action
        else:
            return random.choice(util.get_available_actions(history))


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


def update_player_tree(history, action, player, reward):
    player_history = util.information_function(history, player)
    new_player_history = util.information_function(str(history + action), player)
    update(get_tree(player), player_history, new_player_history, reward)


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

