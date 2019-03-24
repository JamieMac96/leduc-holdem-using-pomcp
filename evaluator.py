import hand_evaluator
import util
from card import Card

# This module has a number of functions that support evaluation of game
# outcome based on the history supplied


def calculate_reward_full_info(history):
    if not util.is_terminal(history):
        return 0

    return get_pot(history) * get_winner(history)


def get_pot(history):
    reward = 2
    round = -1
    bet_amount = 2

    modified_history = history.replace("r", "cc")

    for char in modified_history:
        if char in {"Q", "K", "A"}:
            round += 1
        if char in {"c", "b"}:
            reward += bet_amount * round
    return reward


def average_reward(histories):
    if not histories:
        return 0
    reward_sum = float()

    for history in histories:
        reward_sum += calculate_reward_full_info(history)

    return reward_sum / len(histories)


def get_cards_from_history(history):
    remove_items = ['1', '-', 'c', 'r', 'b', 'f']
    cards = history.translate({ord(x): '' for x in remove_items})
    pc_rank, pc_suit = cards[0], cards[1]
    oc_rank, oc_suit = cards[2], cards[3]
    pub_rank, pub_suit = cards[4], cards[5]

    pc = Card(Card.STRING_TO_RANK[pc_rank], Card.STRING_TO_SUIT[pc_suit])
    oc = Card(Card.STRING_TO_RANK[oc_rank], Card.STRING_TO_SUIT[oc_suit])
    pub = Card(Card.STRING_TO_RANK[pub_rank], Card.STRING_TO_SUIT[pub_suit])

    return pc, oc, pub


def get_winner(history):
    if history.endswith("c"):
        pc, oc, pub = get_cards_from_history(history)
        winner = get_showdown_winner(pc, oc, pub)
    else:
        winner = get_fold_winner(history)
    return winner


def get_showdown_winner(pc, oc, pub):
    hand_player = [pc, pub]
    hand_opponent = [oc, pub]
    player_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_player)
    opp_val = hand_evaluator.HandEvaluator.Two.evaluate_percentile(hand_opponent)

    if player_val >= opp_val:
        return 1
    else:
        return -1


def get_fold_winner(history):
    prefix = util.get_prefix(history)
    last_actions = util.get_last_history_actions(history)
    index = last_actions.index("f")
    if index % 2 == 0:
        return -prefix
    else:
        return prefix
