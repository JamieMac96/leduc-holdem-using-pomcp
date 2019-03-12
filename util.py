import hand_evaluator


def information_function(history, player):
    prefix = "-1" if history.startswith("-1") else "1"
    history_no_prefix = history.replace(prefix, "", 1)
    if player == -1:
        return prefix + history_no_prefix[2:]
    else:
        return history[:2] + history[4:]


def is_terminal(history):
    if history.endswith("f") or (history.endswith("c") and len(history) > 6):
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


def player(history):
    prefix = -1 if history.startswith("-1") else 1
    actions = get_last_history_actions(history)
    if len(actions) % 2 == 0:
        return prefix
    else:
        return -prefix


def get_winner(history, environment):
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
