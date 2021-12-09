import argparse
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


def parse(heat_map):
    result = {
        (row, col): int(digit)
        for row, line in enumerate(heat_map)
        for col, digit in enumerate(line)
        }

    return result


def compute(s: str) -> int:
    heat_map = parse(s.splitlines())

    directions = [
        (0, -1),  # up
        (0, 1),  # down
        (1, 0),  # right
        (-1, 0)  # left
        ]

    risk_levels = 0

    for (x, y), height in heat_map.items():
        adjacent = []
        for dx, dy in directions:
            try:
                adjacent.append(heat_map[x + dx, y + dy])
            except KeyError:
                continue

        if all(adj > height for adj in adjacent):
            risk_levels += height + 1

    return risk_levels


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 15),
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
