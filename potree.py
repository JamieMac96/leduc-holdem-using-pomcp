

# Partially observable UCT node as described by Silver and Veness 2010
class PoNode:

    def __init__(self, history):
        self.visitation_count = 0
        self.history = history
        self.children = {}  # Maps from actions to child nodes

