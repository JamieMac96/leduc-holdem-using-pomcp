import game
import potree

EPSILON = .99
policy = {}
environment = game.Game()


def calculate_exploitability(tree):
    pass


def apply_mcts_strategy(tree):
    strategy_applied = {"": potree.PoNode()}


# Based on Lanctot et al 2011 (Computing approximate nash
# equilibria and robust best-responses using sampling)
# The action probabilities should be based on the
# relative visitation of of the child nodes in the tree.
#
#
#
def generate_action_selection_probabilites():
    pass