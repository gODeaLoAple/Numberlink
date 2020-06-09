class Node:
    TERMINAL_ZERO = None
    TERMINAL_ONE = None

    def __init__(self, edge, mate, arc_name):
        self.edge = edge
        self.mate = mate
        self.arc = arc_name
        self.zero_child = None
        self.one_child = None

    def add_children(self, zero_child, one_child):
        self.zero_child = zero_child
        self.one_child = one_child

    @property
    def children(self):
        return self.zero_child, self.one_child


Node.TERMINAL_ONE = Node(None, None, 1)
Node.TERMINAL_ZERO = Node(None, None, 0)
