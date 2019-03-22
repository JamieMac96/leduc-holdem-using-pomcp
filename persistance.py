import json
import util


def save_deterministic_strategy(tree, filename):
    strategy = get_deterministic_strategy(tree)
    save_to_file(strategy, filename)


def save_stochastic_strategy(tree, filename):
    strategy = get_stochastic_strategy(tree)
    save_to_file(strategy, filename)


def save_to_file(strategy, filename):
    file = open(filename, "w+")
    file.write(json.dumps(strategy, indent=4, sort_keys=True))


def get_deterministic_strategy(tree):
    strategy = {}

    for key in tree.keys():
        if util.player(key) == 1:
            if not util.is_terminal(key) and tree[key].children:
                best_child = util.get_best_child(tree, key, 1)
                strategy[key] = best_child[-1]

    return strategy


def get_stochastic_strategy(tree):
    strategy = {}

    for key in tree.keys():
        if util.player(key) == 1:
            if not util.is_terminal(key) and tree[key].children:
                strategy[key] = {}
                total_child_visits = 0
                for child in tree[key].children:
                    total_child_visits += tree[child].visitation_count

                for child in tree[key].children:
                    child_prob = tree[child].visitation_count / total_child_visits
                    strategy[key][child[-1]] = child_prob

    return strategy
