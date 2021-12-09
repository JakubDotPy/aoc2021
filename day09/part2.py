import argparse
import collections
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
2199943210
3987894921
9856789892
8767896789
9899965678
"""

directions = [
    (0, -1),  # up
    (0, 1),  # down
    (1, 0),  # right
    (-1, 0)  # left
    ]


def parse_map(lines):
    heat_map = collections.defaultdict(lambda: 9)
    for row, line in enumerate(lines):
        for col, digit in enumerate(line):
            heat_map[(row, col)] = int(digit)
    return heat_map


def find_adjacent(point, heat_map):
    x, y = point
    return [
        (x + dx, y + dy)
        for dx, dy in directions
        if (x + dx, y + dy) in heat_map
        ]


def find_low_points(heat_map):
    low_points = []
    for (x, y), height in heat_map.items():
        adjacent = find_adjacent((x, y), heat_map)

        if all(heat_map[adj] > height for adj in adjacent):
            low_points.append((x, y))
    return low_points


def find_basin(low_point, heat_map):
    basin = set()
    to_do = {low_point}
    while to_do:
        x, y = to_do.pop()
        basin.add((x, y))
        for point in find_adjacent((x, y), heat_map):
            if point not in basin and heat_map[point] != 9:
                to_do.add(point)
    return basin


def compute(s: str) -> int:
    heat_map = parse_map(s.splitlines())
    low_points = find_low_points(heat_map)
    basins = [
        find_basin(low_point, heat_map)
        for low_point in low_points
        ]

    sizes = sorted(len(b) for b in basins)

    return sizes[-3] * sizes[-2] * sizes[-1]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 1134),
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
