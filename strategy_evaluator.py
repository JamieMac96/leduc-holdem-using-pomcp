import game
import potree
import util

EPSILON = .99
policy = {}
environment = game.Game()
full_tree = {"": potree.PoNode()}


def calculate_exploitability(tree):
    generate_full_game_tree(tree, "")

    best_response_tree = apply_mcts_strategy(tree)


def generate_full_game_tree(tree, current_history):
    if not current_history:
        for child in tree[current_history].children:
            generate_full_tree_branching(tree, child)


def apply_mcts_strategy(tree):
    best_response_tree = {"": potree.PoNode()}



def generate_full_tree_branching(tree, current_history):
    cards = ["Qh", "Kh", "Ah", "Qs", "Ks", "As"]
    player_one_card = util.get_player_one_card(current_history)
    cards_to_be_added = list(cards)
    cards_to_be_added.remove(player_one_card)

    split_history = current_history.split(player_one_card)
    public_histories = list()

    for card in cards_to_be_added:
        public_history = split_history[0] + player_one_card + card + split_history[1]
        public_histories.append(public_history)
        generate_subtree(tree, current_history, public_history, card)


def generate_subtree(tree, history, full_tree_history, p2_card):

    full_tree[full_tree_history] = potree.PoNode()

    for child in tree[history].children:
        full_tree_child = add_p2_card(child, p2_card)
        full_tree[full_tree_history].children.add(full_tree_child)
        if p2_card not in child:
            generate_subtree(tree, child, full_tree_child, p2_card)


def add_p2_card(history, p2_card):
    player_one_card = util.get_player_one_card(history)
    split_history = history.split(player_one_card)
    return split_history[0] + player_one_card + p2_card + split_history[1]
