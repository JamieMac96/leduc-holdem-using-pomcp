from matplotlib import pyplot as plt

CARDS = ["Qh", "Qs", "Kh", "Ks", "Ah", "As"]


def information_function(history, player):
    prefix = str(get_prefix(history))
    history_no_prefix = history.replace(prefix, "", 1)
    if player == -1:
        return prefix + history_no_prefix[2:]
    elif player == 1:
        return prefix + history_no_prefix[:2] + history_no_prefix[4:]
    else:
        return history


def is_terminal(history):
    if history.endswith("f") or (history.endswith("c") and history.count("c") > 1):
        return True
    else:
        return False


def player(history):
    if history == "" or (not is_terminal(history) and history.endswith("c")):
        return 0  # Chance node

    prefix = get_prefix(history)
    actions = get_last_history_actions(history)
    if len(actions) % 2 == 0:
        return prefix
    else:
        return -prefix


def get_last_history_actions(history):
    split_history = split(history, CARDS)
    return split_history[len(split_history) - 1]


def split(txt, seps):
    default_sep = seps[0]

    # we skip seps[0] because that's the default seperator
    for sep in seps[1:]:
        txt = txt.replace(sep, default_sep)
    return [i.strip() for i in txt.split(default_sep)]


def get_player_card(history, player):
    prefix = get_prefix(history)
    if player == 1:
        return history[1:3] if prefix == 1 else history[2:4]
    else:
        return history[3:5] if prefix == 1 else history[4:6]


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


def get_best_child_full_tree(tree, history, player=1):
    if history not in tree or not tree[history].children:
        return None

    best_child = None
    best_value = float('-inf')
    for child in tree[history].children:
        eq_nodes = get_information_equivalent_nodes(tree, child, player)
        total_val = float()
        for node in eq_nodes:
            total_val += tree[node].value
        avg = total_val / len(eq_nodes)
        if avg * player > best_value:
            best_value = avg * player
            best_child = child

    return best_child


def get_average_child_value(tree, history):
    value_sum = float()
    for child in tree[history].children:
        value_sum += tree[child].value

    return value_sum / len(tree[history].children)


def get_prefix(history):
    if history.startswith("-1"):
        return -1
    elif history.startswith("1"):
        return 1
    else:
        return ""


def get_all_full_histories_from_player_history(history, player):
    prefix = get_prefix(history)
    history_no_prefix = history.replace(str(prefix), "")
    full_histories = []

    for card in get_available_cards(history):
        if player == -1:
            full_histories.append(str(prefix) + card + history_no_prefix)
        elif player == 1:
            full_histories.append(str(prefix) + history_no_prefix[:2] + card + history_no_prefix[2:])

    return full_histories


def get_information_equivalent_nodes(tree, history, player):
    prefix = get_prefix(history)
    player_history = information_function(history, player)
    history_copy = player_history.replace(str(prefix), "")
    cards_copy = get_available_cards(player_history)

    information_equivalent_histories = list()
    for card in cards_copy:
        if player == 1:
            eq_history = str(prefix) + history_copy[0:2] + card + history_copy[2:]
        else:
            eq_history = str(prefix) + card + history_copy
        if eq_history in tree:
            information_equivalent_histories.append(eq_history)

    return information_equivalent_histories


def get_available_actions(history, player=None):
    if history.endswith("b"):
        return ["c", "r", "f"]
    elif history.endswith("r"):
        return ["c", "f"]
    elif history.endswith("h") or history.endswith("s"):
        return ["b", "f"]
    elif history.endswith("c") and not is_terminal(history):
        return get_available_cards(history)
    elif history == "":
        if player is None:
            return get_all_initial_chance_actions()
        else:
            return get_initial_chance_actions()
    else:
        return []


def get_available_cards(history):
    cards_copy = list(CARDS)
    index = 0
    while index < len(cards_copy):
        if cards_copy[index] in history:
            cards_copy.remove(cards_copy[index])
            index -= 1
        index += 1
    return cards_copy


def get_all_initial_chance_actions():
    return ['-1QhQs', '-1QhKh', '-1QhKs', '-1QhAh', '-1QhAs', '-1QsQh',
            '-1QsKh', '-1QsKs', '-1QsAh', '-1QsAs', '-1KhQh', '-1KhQs',
            '-1KhKs', '-1KhAh', '-1KhAs', '-1KsQh', '-1KsQs', '-1KsKh',
            '-1KsAh', '-1KsAs', '-1AhQh', '-1AhQs', '-1AhKh', '-1AhKs',
            '-1AhAs', '-1AsQh', '-1AsQs', '-1AsKh', '-1AsKs', '-1AsAh',
            '1QhQs', '1QhKh', '1QhKs', '1QhAh', '1QhAs', '1QsQh',
            '1QsKh', '1QsKs', '1QsAh', '1QsAs', '1KhQh', '1KhQs',
            '1KhKs', '1KhAh', '1KhAs', '1KsQh', '1KsQs', '1KsKh',
            '1KsAh', '1KsAs', '1AhQh', '1AhQs', '1AhKh', '1AhKs',
            '1AhAs', '1AsQh', '1AsQs', '1AsKh','1AsKs', '1AsAh']


def get_initial_chance_actions():
    return ['-1Qs', '-1Qh', '-1Ks', '-1Kh', '-1As', '-1Ah',
            '1Qs', '1Qh', '1Ks', '1Kh', '1As', '1Ah']


def manual_traverse_tree(tree):
    node = tree[""]
    while node.children != {}:
        print("----------------------------------------------------------------------------------")
        for item in node.children:
            print(item + ": " + str(tree[item]))
        choice = input("choose the child you would like to select: ")
        if choice == "exit":
            break
        if choice in tree:
            node = tree[choice]
        else:
            print("Error choice not in tree, type exit to leave")


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


if __name__ == "__main__":
    pass
