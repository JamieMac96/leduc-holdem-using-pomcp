import time

import potree
import util
import evaluator

EPSILON = .99
policy = {}


def calculate_exploitability(tree):
    return get_best_response_tree(tree)[""].value


def get_best_response_tree(tree):
    full_tree = build_tree("", {})
    terminals = []
    best_response_tree = {}
    best_response_tree = apply_mcts_strategy(tree, full_tree, best_response_tree, terminals)
    evaluate_terminals(best_response_tree, terminals)
    add_parents(best_response_tree)
    propagate_rewards(best_response_tree, terminals)
    # util.print_tree(best_response_tree)
    # util.manual_traverse_tree(best_response_tree)
    return best_response_tree


def build_tree(history, tree):
    if history not in tree:
        tree[history] = potree.PoNode()

    if not util.is_terminal(history):
        actions = util.get_available_actions(history)
        for action in actions:
            child = history + action
            tree[child] = potree.PoNode()
            tree[child].parent = history
            tree[history].children.add(child)
            build_tree(child, tree)

    return tree


def apply_mcts_strategy(strategy_source, full_tree, best_response_tree, terminals):
    if "" in strategy_source and isinstance(strategy_source[""], potree.PoNode):
        return apply_mcts_strategy_from_tree(strategy_source, full_tree, best_response_tree, "", terminals)
    else:
        return apply_mcts_strategy_from_deterministic_strategy(strategy_source, full_tree, best_response_tree, "", terminals)


def apply_mcts_strategy_from_deterministic_strategy(strategy, full_tree, best_response_tree, current_history, terminals):
    if current_history not in full_tree:
        return best_response_tree

    best_response_tree[current_history] = potree.PoNode()
    children = full_tree[current_history].children
    if util.is_terminal(current_history):
        terminals.append(current_history)

    if util.player(current_history) == 1:
        player_history = util.information_function(current_history, 1)
        if player_history in strategy:
            child = current_history + strategy[player_history]
            best_response_tree[current_history].children = [current_history + strategy[player_history]]
            children = [child]
        else:
            children = []
    else:
        best_response_tree[current_history].children = set(children)

    for history in children:
        apply_mcts_strategy_from_deterministic_strategy(strategy, full_tree, best_response_tree, history, terminals)

    return best_response_tree


def apply_mcts_strategy_from_tree(tree, full_tree, best_response_tree, current_history, terminals):
    if current_history not in full_tree:
        return best_response_tree

    best_response_tree[current_history] = potree.PoNode()
    children = full_tree[current_history].children
    if util.is_terminal(current_history):
        terminals.append(current_history)

    if util.player(current_history) == 1:
        player_history = util.information_function(current_history, 1)
        best_child = util.get_best_child(tree, player_history)
        if best_child is not None:
            action = best_child.replace(player_history, "")
            children = [current_history + action]
            best_response_tree[current_history].children = {current_history + action}
        else:
            children = []
    else:
        best_response_tree[current_history].children = set(children)

    for history in children:
        apply_mcts_strategy_from_tree(tree, full_tree, best_response_tree, history, terminals)

    return best_response_tree


def evaluate_terminals(best_response_tree, terminals):
    for history in terminals:
        if history.endswith("f"):
            best_response_tree[history].value = evaluator.calculate_reward_full_info(history)
        else:
            eq_nodes = util.get_information_equivalent_nodes(best_response_tree, history, -1)
            avg = evaluator.average_reward(eq_nodes)
            best_response_tree[history].value = avg


def add_parents(best_response_tree):
    for history, node in best_response_tree.items():
        for child in node.children:
            # TODO: Fix error that is forcing this check
            if child in best_response_tree:
                best_response_tree[child].parent = history


def propagate_rewards(best_response_tree, terminals):
    for history in terminals:
        propagate_rewards_recursive(best_response_tree, history)


def propagate_rewards_recursive(best_response_tree, history):
    if history == "":
        return
    parent = best_response_tree[history].parent
    player = util.player(parent)
    if player == 0:
        value_to_propagate = util.get_average_child_value(best_response_tree, parent)
    elif player == 1:
        value_to_propagate = best_response_tree[next(iter(best_response_tree[parent].children))].value
    else:
        best_sibling = util.get_best_child(best_response_tree, parent, -1)
        value_to_propagate = best_response_tree[best_sibling].value
    best_response_tree[parent].value = value_to_propagate
    propagate_rewards_recursive(best_response_tree, parent)


def add_p2_card(history, p2_card):
    player_one_card = util.get_player_card(history, 1)
    split_history = history.split(player_one_card)
    return split_history[0] + player_one_card + p2_card + split_history[1]
