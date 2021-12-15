import argparse
import itertools
import os.path

import networkx as nx
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
EXPECTED = 315


def compute(s: str) -> int:
    original_weights = [[int(c) for c in row] for row in s.splitlines()]
    size = len(original_weights)
    expanded_weights = {}
    for x, y in itertools.product(range(5 * size), range(5 * size)):
        new_weight = original_weights[y % size][x % size] + x // size + y // size
        new_weight = new_weight - 9 if new_weight > 9 else new_weight
        expanded_weights[(x, y)] = new_weight

    G = nx.grid_2d_graph(size * 5, size * 5, create_using=nx.DiGraph)
    for u, v in G.edges:
        G[u][v]['weight'] = expanded_weights[v]

    return nx.shortest_path_length(
        G,  # graph
        (0, 0), (size * 5 - 1, size * 5 - 1),  # start, end
        weight='weight'  # what to consider as edge's weight
        )


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, EXPECTED),
            ),
    )
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
