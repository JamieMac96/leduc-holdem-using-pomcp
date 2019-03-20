class PoNode:

    def __init__(self):
        self.visitation_count = 1
        self.value = 0
        self.parent = ""
        # List of histories that correspond to children
        self.children = set()

    def __str__(self):
        return "N(h): " + str(self.visitation_count) \
               + "  V(h): " + str(self.value)

