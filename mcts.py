import time
import math
import random
from matplotlib import pyplot as plt
import seaborn as sbn
from leduc import game
from leduc import potree
from pycfr import hand_evaluator

DISCOUNT_FACTOR = .95
EPSILON = .01
EXPLORATION_CONSTANT = 18
environment = game.Game()
tree = {"": potree.PoNode()}  # Root node of tree


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


def rollout(history):
    if not environment.get_possible_actions():
        return 0
    action = random.choice(environment.get_possible_actions())
    observation = environment.update_state(action)
    new_history = history + action + observation
    return simulate(new_history)


def simulate(history, out_of_tree=False):
    if is_terminal(history):
        reward = calculate_reward(history)
        environment.reset()
        environment.cumulative_reward += reward
        environment.rewards.append(environment.cumulative_reward)
        return reward
    if out_of_tree:
        return rollout(history)
    if history == "":
        return handle_initial_states(history)
    if history not in tree.keys():
        expand(history)
        action = rollout_policy(environment.get_possible_actions())
        out_of_tree = True
    else:
        ensure_node_is_expanded(history)
        action = get_best_action_ucb(history)

    new_history = get_next_history(history, action)
    running_reward = calculate_reward(history) + DISCOUNT_FACTOR * simulate(new_history, out_of_tree)
    add_new_history(history, new_history)
    update(history, new_history, running_reward)

    return running_reward


def get_next_history(history, action):
    observation = environment.update_state(action)
    new_history = history + action + observation
    return new_history


def add_new_history(history, new_history):
    if new_history not in tree.keys():
        tree[new_history] = potree.PoNode()
        tree[new_history].visitation_count = 1
    if new_history not in tree[history].children:
        tree[history].children.add(new_history)


def update(history, new_history, running_reward):
    tree[history].visitation_count += 1
    tree[new_history].visitation_count += 1
    tree[new_history].value += (running_reward - tree[new_history].value) / tree[new_history].visitation_count


def handle_initial_states(history):
    new_history = environment.get_initial_state()
    tree[new_history] = potree.PoNode()
    if new_history not in tree[history].children:
        tree[history].children.add(new_history)
    return simulate(new_history)


def ensure_node_is_expanded(history):
    if len(tree[history].children) != len(environment.get_possible_actions()):
        expand(history)


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


def is_terminal(history):
    if history.endswith("f") or (history.endswith("c") and len(history) > 6):
        return True
    else:
        return False


def calculate_reward(history):
    if not is_terminal(history):
        return 0
    reward = 2
    round = 0
    bet_amount = 2

    # In terms of reward, a raise==2 calls. This also simplifies the algorithm
    modified_history = history.replace("r", "cc")

    for char in modified_history:
        if char in {"Q", "K", "A"}:
            round += 1
        if char in {"c", "b"}:
            reward += bet_amount * round

    winner = get_winner(history)

    return reward * winner


def get_winner(history):
    prefix = -1 if history.startswith("-1") else 1
    if history.endswith("f"):
        last_actions = get_last_history_actions(history)
        index = last_actions.index("f")
        if index % 2 == 0:
            winner = -prefix
        else:
            winner = prefix
        return winner
    elif history.endswith("c"):
        pc = environment.player_card
        oc = environment.opponent_card
        pub = environment.public_card

        hand_player = [pc, pub]
        hand_opponent = [oc, pub]
        player_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_player)
        opp_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_opponent)

        if player_val >= opp_val:
            return 1
        else:
            return -1


def get_last_history_actions(history):
    cards = ["Qh", "Kh", "Ah", "Qs", "Ks", "As"]
    split_history = split(history, cards)
    return split_history[len(split_history) - 1]


def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default seperator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


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
    num_searches = 1
    sbn.set_style("darkgrid")
    list_of_rewards = list()
    for i in range(num_searches):
        environment.rewards = list()
        environment.cumulative_reward = 0
        environment.count = 0
        environment.indices = list()
        tree = {"": potree.PoNode()}
        search("", iterations=iterations)
        list_of_rewards.append(environment.rewards)

    avg_rewards = list()
    reward_sum = 0
    for i in range(len(environment.indices)):
        for reward in list_of_rewards:
            reward_sum += reward[i]
        avg_rewards.append(reward_sum / num_searches)
        reward_sum = 0

    plt.plot(environment.indices, avg_rewards)
    plt.xlabel("Iterations")
    plt.ylabel("Cumulative reward")

    plt.show()
    print_tree()
    manual_traverse_tree()
    print("NUMBER OF ITERATIONS: " + str(iterations))