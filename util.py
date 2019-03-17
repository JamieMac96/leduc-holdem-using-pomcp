from card import Card
import hand_evaluator


def information_function(history, player):
    prefix = "-1" if history.startswith("-1") else "1"
    history_no_prefix = history.replace(prefix, "", 1)
    if player == -1:
        return prefix + history_no_prefix[2:]
    else:
        return history[:2] + history[4:]


def is_terminal(history):
    history_copy = history.replace("1", "")
    if history_copy.endswith("f") or (history_copy.endswith("c") and history.count("c") > 1):
        return True
    else:
        return False


def calculate_reward(history, environment):
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

    winner = get_winner(history, environment)

    return reward * winner


def calculate_reward_full_info(history):
    if not is_terminal(history):
        return 0
    reward = 2
    round = -1
    bet_amount = 2

    # In terms of reward, a raise==2 calls. This also simplifies the algorithm
    modified_history = history.replace("r", "cc")

    for char in modified_history:
        if char in {"Q", "K", "A"}:
            round += 1
        if char in {"c", "b"}:
            reward += bet_amount * round

    if history.endswith("c"):
        remove_items = ['1', '-', 'c', 'r', 'b', 'f']
        cards = history.translate({ord(x): '' for x in remove_items})
        pc_rank, pc_suit = cards[0], cards[1]
        oc_rank, oc_suit = cards[2], cards[3]
        pub_rank, pub_suit = cards[4], cards[5]

        pc = Card(Card.STRING_TO_RANK[pc_rank], Card.STRING_TO_SUIT[pc_suit])
        oc = Card(Card.STRING_TO_RANK[oc_rank], Card.STRING_TO_SUIT[oc_suit])
        pub = Card(Card.STRING_TO_RANK[pub_rank], Card.STRING_TO_SUIT[pub_suit])

        winner = get_showdown_winner(pc, oc, pub)
    else:
        winner = get_fold_winner(history)

    return reward * winner


def player(history):
    if history == "" or (not is_terminal(history) and history.endswith("c")):
        return 0  # Chance node

    prefix = get_prefix(history)
    actions = get_last_history_actions(history)
    if len(actions) % 2 == 0:
        return prefix
    else:
        return -prefix


def get_winner(history, environment):
    if history.endswith("f"):
        return get_fold_winner(history)
    elif history.endswith("c"):
        pc = environment.dealer.deal_private()[0]
        oc = environment.dealer.deal_private()[1]
        pub = environment.dealer.deal_public()
        return get_showdown_winner(pc, oc, pub)


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
    prefix = get_prefix(history)
    last_actions = get_last_history_actions(history)
    index = last_actions.index("f")
    if index % 2 == 0:
        winner = -prefix
    else:
        winner = prefix
    return winner


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


def get_player_one_card(history):
    prefix = get_prefix(history)
    return history[1:3] if prefix == 1 else history[2:4]


def get_best_child(tree, history, player=1):
    if history not in tree or not tree[history].children:
        return None

    best_child = None
    best_value = float('-inf')
    for child in tree[history].children:
        if tree[child].value * player > best_value:
            best_value = tree[child].value * player
            best_child = child

    return best_child


def get_average_child_value(tree, history):
    value_sum = float()
    for child in tree[history].children:
        value_sum += tree[child].value

    return value_sum / len(tree[history].children)


def get_prefix(history):
    return -1 if history.startswith("-1") else 1


def get_information_equivalent_nodes(tree, history, player):
    cards = ["Ah", "As", "Kh", "Ks", "Qh", "Qs"]
    prefix = get_prefix(history)
    player_history = information_function(history, player)
    history_copy = player_history.replace(str(prefix), "")
    player_card = history_copy[0:2]
    cards.remove(player_card)

    information_equivalent_histories = list()
    for card in cards:
        if player == 1:
            eq_history = str(prefix) + history_copy[0:2] + card + history_copy[2:]
        else:
            eq_history = str(prefix) + card + history_copy
        if eq_history in tree:
            information_equivalent_histories.append(eq_history)

    return information_equivalent_histories


def get_available_actions(history):
    if history.endswith("b"):
        return ["f", "c", "r"]
    elif history.endswith("r"):
        return ["c", "f"]
    elif history.endswith("h") or history.endswith("s"):
        return ["b", "f"]
    else:
        return []


def average_reward(histories):
    reward_sum = float()

    for history in histories:
        reward_sum += calculate_reward_full_info(history)

    return reward_sum / len(histories)


def manual_traverse_tree(tree):
    node = tree[""]
    while node.children != {}:
        print("----------------------------------------------------------------------------------")
        for item in node.children:
            print(item + ": " + str(tree[item]))
        choice = input("choose the child you would like to select: ")
        node = tree[choice]


def print_tree(tree):
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
