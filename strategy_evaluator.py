import potree
import util

EPSILON = .99
policy = {}
full_tree = {"": potree.PoNode()}


def calculate_exploitability(tree):
    return get_best_response_tree(tree)[""].value


def get_best_response_tree(tree):
    full_tree = generate_full_game_tree(tree, "")
    best_response_tree = {}
    best_response_tree = apply_mcts_strategy(tree, full_tree, best_response_tree, "")
    evaluate_terminals(best_response_tree)
    add_parents(best_response_tree)
    propagate_rewards(best_response_tree)
    return best_response_tree


def generate_full_game_tree(tree, current_history):
    if not current_history:
        for child in tree[current_history].children:
            generate_full_tree_branching(tree, child)

    return full_tree


def apply_mcts_strategy(tree, full_tree, best_response_tree, current_history):
    if current_history not in full_tree:
        return best_response_tree

    best_response_tree[current_history] = potree.PoNode()
    histories = full_tree[current_history].children

    if util.player(current_history) == 1:
        player_history = util.information_function(current_history, 1)
        best_child = util.get_best_child(tree, player_history)  # TODO: have chance as separate player/independent nodes
        if best_child is not None:
            action = best_child.replace(player_history, "")
            histories = [current_history + action]
            best_response_tree[current_history].children = {current_history + action}
        else:
            histories = []
    else:
        best_response_tree[current_history].children = set(histories)

    for history in histories:
        apply_mcts_strategy(tree, full_tree, best_response_tree, history)

    return best_response_tree


def evaluate_terminals(best_response_tree):
    for history, node in best_response_tree.items():
        if util.is_terminal(history):
            best_response_tree[history].value = util.calculate_reward_full_info(history)


def add_parents(best_response_tree):
    for history, node in best_response_tree.items():
        for child in node.children:
            # TODO: Fix error that is forcing this check
            if child in best_response_tree:
                best_response_tree[child].parent = history


def propagate_rewards(best_response_tree):
    leaf_parents = list()

    for history, node in best_response_tree.items():
        if util.is_terminal(history):
            parent = node.parent
            leaf_parents.append(parent)
            if util.player(history) == 1:
                eq_nodes = util.get_information_equivalent_nodes(best_response_tree, history, -1)
                average_reward = util.average_reward(eq_nodes)
                best_response_tree[parent].value = average_reward
            else:
                best_response_tree[parent].value = best_response_tree[history].value

    for history in leaf_parents:
        propagate_rewards_recursive(best_response_tree, history)


def propagate_rewards_recursive(best_response_tree, history):
    if history == "":
        return
    parent = best_response_tree[history].parent
    if util.player(parent) == 0:
        value_to_propagate = util.get_average_child_value(best_response_tree, parent)
    else:
        best_sibling = util.get_best_child_full_tree(best_response_tree, parent, player=-1)
        value_to_propagate = best_response_tree[best_sibling].value
    best_response_tree[parent].value = value_to_propagate
    propagate_rewards_recursive(best_response_tree, parent)


def generate_full_tree_branching(tree, current_history):
    cards = ["Qh", "Kh", "Ah", "Qs", "Ks", "As"]
    player_one_card = util.get_player_card(current_history, 1)
    cards_to_be_added = list(cards)
    cards_to_be_added.remove(player_one_card)

    split_history = current_history.split(player_one_card)

    for card in cards_to_be_added:
        public_history = split_history[0] + player_one_card + card + split_history[1]
        full_tree[""].children.add(public_history)
        generate_subtree(tree, current_history, public_history, card)


def generate_subtree(tree, history, full_tree_history, p2_card):
    full_tree[full_tree_history] = potree.PoNode()

    for child in tree[history].children:
        if p2_card not in child:
            full_tree_child = add_p2_card(child, p2_card)
            full_tree[full_tree_history].children.add(full_tree_child)
            generate_subtree(tree, child, full_tree_child, p2_card)


def add_p2_card(history, p2_card):
    player_one_card = util.get_player_card(history)
    split_history = history.split(player_one_card)
    return split_history[0] + player_one_card + p2_card + split_history[1]
