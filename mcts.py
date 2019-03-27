import metrics
import potree
import util
import evaluator

import math
import random
from numpy import random as rand

player_one_tree = {}  # Root node of tree
player_two_tree = {}  # Player 2 aka player -1
GAMMA = .01


class Mcts:
    def __init__(self, m_metrics, discount_factor=.95, exploration_constant=18):
        self.discount_factor = discount_factor
        self.exploration_constant = exploration_constant
        self.m_metrics = m_metrics
        self.out_of_tree = {1: False, -1: False, 0: False}

    def simulate(self, history):
        player_tree = get_tree(util.player(history))
        if util.is_terminal(history):
            return self.handle_terminal_state(history)

        player = util.player(history)
        if self.out_of_tree[player]:
            return self.rollout(history)

        player_history = util.information_function(history, player)
        # TODO: fix: Some nodes do not have children (expanding both player's trees)
        if player_history in player_tree and player_tree[player_history].children:
            action = self.select(history)
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
        self.m_metrics.cumulative_reward += reward
        self.m_metrics.rewards.append(self.m_metrics.cumulative_reward)
        self.reset_out_of_tree()
        return reward

    def select(self, history):
        player = util.player(history)
        player_history = util.information_function(history, player)
        if player in {-1, 1}:
            tree = get_tree(player)
            eta_sub_expression = math.pow(1 + (.05 * math.sqrt(tree[player_history].visitation_count)), -1)
            eta = max((GAMMA, .9 * eta_sub_expression))
            z = random.uniform(0, 1)
            if z < eta:
                return self.get_best_action_ucb(history, player, tree)
            else:
                return self.get_best_action_avg_strategy(player_history, tree)
        else:
            return random.choice(util.get_available_actions(history))

    def get_best_action_avg_strategy(self, player_history, tree):
        total_child_visits = 0
        actions = []
        probabilities = []
        for child in tree[player_history].children:
            total_child_visits += tree[child].visitation_count

        for child in tree[player_history].children:
            child_prob = tree[child].visitation_count / total_child_visits
            actions.append(child.replace(player_history, ""))
            probabilities.append(child_prob)

        return rand.choice(actions, p=probabilities)

    def get_best_action_ucb(self, history, player, tree):
        player_history = util.information_function(history, player)
        best_value = float('-inf')
        best_action = None
        for action in util.get_available_actions(history):
            node_val = self.calculate_next_node_value(tree, player_history, action, player)
            if node_val > best_value:
                best_action = action
                best_value = node_val
        return best_action

    def calculate_next_node_value(self, tree, player_history, action, player):
        next_history = player_history + action
        new_visitation_count = 1
        new_value = 0
        if next_history in tree:
            new_visitation_count = tree[next_history].visitation_count
            new_value = tree[next_history].value * player
        exploration_bonus = self.exploration_constant * \
                            math.sqrt(math.log(tree[player_history].visitation_count + 1) /
                                      new_visitation_count)
        return new_value + exploration_bonus


def rollout_policy(actions):
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

    for action in util.get_available_actions(player_history, player=player):
        new_history = player_history + action
        if new_history not in tree:
            tree[new_history] = potree.PoNode()
        tree[player_history].children.add(new_history)