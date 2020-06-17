from numberlink import HexLink, HexagonalField
from algorithms.structures import Node, Bucket
from algorithms.generator import generate_hexagonal_field
import itertools

"""
Алгоритм был построены на основании статьи, которую можно скачать по ссылке:
http://www.mdpi.com/1999-4893/5/2/176/pdf
Огромная благодарность авторам статьи.
"""


def get_right_path(edge, paths):
    for path in paths:
        if any(v in path for v in edge):
            return path
    return None


def make_field_from_solution(field: HexLink, solution):
    result = HexagonalField(generate_hexagonal_field(field.size))

    for pair in field.get_targets()["pairs"]:
        start, end = tuple(pair)
        number = field[start]
        while start != end:
            for edge in solution:
                if start in edge:
                    result[start] = number
                    start = get_opposite(start, edge)
        result[end] = number
    return result.field


def make_solutions(root, path=None):
    """
    Принимает на вход корень ZDD-диаграммы Numberlink.
    Генерирует все решения задачи Numberlink.
    """
    path = path or []
    if root is Node.TERMINAL_ONE:
        yield path
    elif root is not Node.TERMINAL_ZERO:
        yield from itertools.chain(
                make_solutions(root.zero_child, path),
                make_solutions(root.one_child, path + [root.edge])
        )


def get_path(path, node):
    return path if node.arc == 0 else path + [node.edge]


def solve(instance: HexLink):
    """
    Принимает на вход задачу Numberlink.
    Возвращает диаграмму решений задачи.
    """
    graph = instance.make_graph()
    targets = instance.get_targets()
    vertices = Bucket(graph.vertices())
    edges = graph.edges()

    root = Node(edges[0], {v: v for v in vertices.active}, 1)

    def get_node(node_edge, mate, arc):
        return Node(node_edge, mate, arc) if node_edge else Node.TERMINAL_ONE

    nodes = [root]
    while edges:
        edge = edges.pop(0)
        next_edge = edges[0] if edges else None
        update_vertices(vertices, edge, edges)
        new_nodes = []
        for node in nodes:
            children = []
            if is_zero_incompatible(node, targets, vertices):
                children.append(Node.TERMINAL_ZERO)
            else:
                new_mate = update_domain(node.mate, vertices.active)
                children.append(get_node(next_edge, new_mate, 0))
            if is_one_incompatible(node, targets, vertices):
                children.append(Node.TERMINAL_ZERO)
            else:
                new_mate = update_domain(update_mate(node), vertices.active)
                children.append(get_node(next_edge, new_mate, 1))
            new_nodes.extend(n for n in children if not is_terminal(n))
            node.add_children(*children)
        nodes = new_nodes
    return make_solutions(root)


def is_zero_incompatible(node, targets, vertices):
    filtered = (v for v in node.edge if v not in vertices.active)

    def condition(v):
        return (node.mate[v] == v
                or v not in targets["vertices"] and node.mate[v] not in [0, v])

    return any(condition(v) for v in filtered)


def is_one_incompatible(node, targets, vertices):
    union = targets["vertices"] | vertices.thrown
    pair = {node.mate[v] for v in node.edge}

    def condition(v):
        return (v in targets["vertices"] and node.mate[v] != v
                or node.mate[v] in [0, get_opposite(v, node.edge)])

    return (pair <= union and pair not in targets["pairs"]
            or any(condition(v) for v in node.edge))


def is_terminal(node):
    return node in [Node.TERMINAL_ZERO, Node.TERMINAL_ONE]


def is_not_terminal(node):
    return not is_terminal(node)


def update_domain(mate, domain):
    """
    Принимает на вход вспомогательную функцию и вершины.
    Возвращает ограничение функции на данные вершины.
    """
    return {v: mate[v] for v in domain}


def update_mate(parent):
    """
    Принимает на вход узел родителя.
    Возвращает словарь-функцию узла, определенную на вершинах родителя.
    """
    mate = {}

    for vertex in parent.mate:
        if vertex in parent.edge and parent.mate[vertex] != vertex:
            mate[vertex] = 0
        elif parent.mate[vertex] in parent.edge:
            opposite = get_opposite(parent.mate[vertex], parent.edge)
            mate[vertex] = parent.mate[opposite]
        else:
            mate[vertex] = parent.mate[vertex]

    return mate


def update_vertices(vertices, edge, edges):
    """
    Принимает на вход ребро, словарь вершин, которые делятся на
    активные/неактивные, список других ребер.
    Перемещает в неактивные те вершины, которые инцидентны только ребру
    edge и никакому другому ребру из edges.
    """
    vertices_in_edges = set(itertools.chain(*edges))
    for vertex in (v for v in edge if v not in vertices_in_edges):
        vertices.throw(vertex)


def get_opposite(x, pair):
    """
    Принимает на вход элемент и список/tuple из двух элементов.
    Возвращает парный элемент для x из pair, если x находится в списке,
    иначе возвращает None.
    """
    return pair[0] if x == pair[1] else pair[1] if x == pair[0] else None
