from algorithms.solver import *
from graph_tools import Graph
from numberlink import HexLink
import unittest


class SolverTest(unittest.TestCase):
    def setUp(self):
        self.instance_one_solution = HexLink([
            [1, 0],      # 1 0
            [0, 2, 1],  # 0 2 1
            [0, 2]       # 0 2
        ])
        self.instance_many_solutions = HexLink([
            [1, 2],      # 1 2
            [0, 0, 0],  # 0 0 0
            [1, 2],      # 1 2
        ])
        self.instance_no_solutions = HexLink([
            [1, 2],      # 1 2
            [0, 0, 0],  # 0 0 0
            [2, 1]       # 2 1
        ])

        self.graph = Graph(directed=False)
        self.graph.add_edge("p", "q")  # e_1
        self.graph.add_edge("p", "r")  # e_2
        self.graph.add_edge("r", "q")  # e_3
        self.graph.add_edge("q", "s")  # e_4

    def test_update_mate(self):
        self.update_mate_tester(
            expected={
                "p": "q",
                "q": "p",
                "r": "r",
                "s": "s"
            },
            parent_node=Node(
                self.graph.edges()[0],
                {v: v for v in self.graph.vertices()},
                1),
            domain=list("pqrs")
        )

        self.update_mate_tester(
            expected={
                "q": "r",
                "r": "q",
                "s": "s"
            },
            parent_node=Node(
                self.graph.edges()[1],
                {
                    "p": "q",
                    "q": "p",
                    "r": "r",
                    "s": "s"
                },
                1),
            domain=list("qrs")
        )

        self.update_mate_tester(
            expected={
                "q": 0,
                "s": "s"
            },
            parent_node=Node(
                self.graph.edges()[2],
                {
                    "q": "p",
                    "r": "r",
                    "s": "s"
                },
                1),
            domain=list("qs")
        )

    def update_mate_tester(self, expected, parent_node, domain):
        actual = update_domain(update_mate(parent_node), domain)
        self.assertDictEqual(expected, actual)

    def test_solve_one_solution(self):
        expected = [
            [(0, 0), (0, 1)],
            [(0, 1), (1, 2)],
            [(1, 0), (1, 1)],
            [(1, 0), (2, 0)],
            [(2, 0), (2, 1)]
        ]
        actual = list(solve(self.instance_one_solution))
        self.assertTrue(len(actual) == 1)
        self.assertListEqual(expected, actual[0])

    def test_solve_many_solutions(self):
        expected = [
            [[(0, 0), (1, 0)],
             [(0, 1), (1, 1)],
             [(1, 0), (2, 0)],
             [(1, 1), (1, 2)],
             [(1, 2), (2, 1)]],
            [[(0, 0), (1, 0)],
             [(0, 1), (1, 2)],
             [(1, 0), (2, 0)],
             [(1, 1), (1, 2)],
             [(1, 1), (2, 1)]],
            [[(0, 0), (1, 0)],
             [(0, 1), (1, 2)],
             [(1, 0), (1, 1)],
             [(1, 1), (2, 0)],
             [(1, 2), (2, 1)]],
            [[(0, 0), (1, 1)],
             [(0, 1), (1, 2)],
             [(1, 0), (1, 1)],
             [(1, 0), (2, 0)],
             [(1, 2), (2, 1)]]
        ]
        actual = list(solve(self.instance_many_solutions))

        self.assertListEqual(expected, actual)

    def test_solve_no_solutions(self):
        expected = []
        actual = list(solve(self.instance_no_solutions))
        self.assertListEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
