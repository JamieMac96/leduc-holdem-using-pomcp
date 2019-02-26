import time
import math
import random
from leduc import game
from leduc import potree
from matplotlib import pyplot as plt

cumulative_reward = 0
DISCOUNT_FACTOR = .95
EPSILON = .01
EXPLORATION_CONSTANT = 18
environment = game.Game()
tree = {"": potree.PoNode()}  # Root node of tree


def search(history, time_limit=None, iterations=None):
    if time_limit is not None:
        time_limit = time.time() + time_limit / 1000
        while time.time() < time_limit:
            simulate(history, 0)
    elif iterations is not None:
        for i in range(iterations):
            simulate(history, 0)
            environment.reset()
    else:
        raise ValueError("You must specify a time or iterations limit")


def rollout(history, depth):
    if math.pow(DISCOUNT_FACTOR, depth) < EPSILON:
        return 0
    actions = environment.get_possible_actions()
    if not actions:
        return 0
    action = random.choice(actions)  # Random rollout currently being used
    observation, reward = environment.update_state(action)
    new_history = history + action + observation
    return reward + rollout(new_history, depth+1)


def simulate(history, depth):
    if environment.game_over:
        environment.reset()
        return 0
    if math.pow(DISCOUNT_FACTOR, depth) < EPSILON:
        return 0
    if history == "":
        new_history = environment.get_initial_state()
        if new_history not in tree[history].children:
            tree[history].children.add(new_history)
        return simulate(new_history, depth+1)
    if history not in tree.keys():
        expand(history)
        return rollout(history, depth)
    if len(tree[history].children) != len(environment.get_possible_actions()):
        expand(history)
    action = get_best_action_ucb(history)
    observation, reward = environment.update_state(action)
    new_history = history + action + observation
    reward_update = reward + DISCOUNT_FACTOR * simulate(new_history, depth+1)
    if new_history not in tree.keys():
        tree[new_history] = potree.PoNode()
        tree[new_history].visitation_count = 1
    if new_history not in tree[history].children:
        tree[history].children.add(new_history)
    tree[history].visitation_count += 1
    tree[new_history].visitation_count += 1
    tree[new_history].value += (reward_update - tree[new_history].value) / tree[new_history].visitation_count
    return reward_update


def get_best_action_ucb(history):
    if environment.current_player == -1:
        return random.choice(environment.get_possible_actions())
    else:
        best_value = float('-inf')
        best_action = None
        for action in environment.get_possible_actions():

            next_history = history + action
            exploration_bonus = EXPLORATION_CONSTANT * \
                            math.sqrt(math.log(tree[history].visitation_count) /
                                      tree[next_history].visitation_count)
            node_val = tree[next_history].value + exploration_bonus
            if node_val >= best_value:
                best_action = action
                best_value = node_val
        return best_action


def expand(history):
    if history not in tree.keys():
        tree[history] = potree.PoNode()
    for action in environment.get_possible_actions():
        new_history = history + action
        tree[new_history] = potree.PoNode()
        tree[history].children.add(new_history)


def manual_traverse_tree():
    node = tree[""]
    while node.children != {}:
        print("----------------------------------------------------------------------------------")
        for item in node.children:
            print(item + ": " + str(tree[item]))
        choice = input("choose the child you would like to select: ")
        node = tree[choice]


def print_tree():
    ace_total_value = 0
    king_total_value = 0
    queen_total_value = 0

    for key in sorted(tree.keys()):
        if "1A" in key:
            ace_total_value += tree[key].value
        if "1K" in key:
            king_total_value += tree[key].value
        if "1Q" in key:
            queen_total_value += tree[key].value
        print(key + ": " + str(tree[key]))

    print("value of queen: " + str(queen_total_value))
    print("value of king: " + str(king_total_value))
    print("value of ace: " + str(ace_total_value))

if __name__ == "__main__":
    iterations = 100000
    search("", iterations=iterations)
    print_tree()
    manual_traverse_tree()
    print("NUMBER OF ITERATIONS: " + str(iterations))
    plt.plot(environment.indices, environment.rewards)
    plt.show()
