import argparse
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
EXPECTED = 40


def compute(s: str) -> int:
    width = height = 0
    weights = {}
    for y, line in enumerate(s.splitlines()):
        width = len(line)
        height += 1
        for x, c in enumerate(line):
            weights[(x, y)] = int(c)

    G = nx.grid_2d_graph(width, height, create_using=nx.DiGraph)
    for u, v in G.edges:
        G[u][v]['weight'] = weights[v]

    return nx.shortest_path_length(
        G,  # graph
        (0, 0), (width - 1, height - 1),  # start, end
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
