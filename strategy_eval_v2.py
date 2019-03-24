import potree
import util
import evaluator


def build_tree(node, tree):
    if not node in tree:
        tree[node] = potree.PoNode()

    if not util.is_terminal(node):
        actions = util.get_available_actions(node)
        for action in actions:
            child = node + action
            tree[child] = potree.PoNode()
            tree[child].parent = node
            tree[node].children.add(child)
            build_tree(child, tree)

    return tree


def evaluate_terminals(tree):
    for history in tree.keys():
        if util.is_terminal(history):
            tree[history].value = calculate_average_value_of_terminal(history)


def calculate_average_value_of_terminal(history):
    histories = util.get_all_full_histories_from_player_history(history, -1)

    value_sum = 0.0
    for history in histories:
        value_sum += evaluator.calculate_reward_full_info(history)

    return value_sum / len(histories)

if __name__ == "__main__":
    tree = build_tree("", {})
    evaluate_terminals(tree)
    util.print_tree(tree)
    util.manual_traverse_tree(tree)