import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""
EXPECTED = 1656


def adjacent(x, y):
    for d_x in (-1, 0, 1):
        for d_y in (-1, 0, 1):
            if not d_x == d_y == 0:
                yield x + d_x, y + d_y


def compute(s: str) -> int:
    squids = {
        (x, y): int(val)
        for y, row in enumerate(s.splitlines())
        for x, val in enumerate(row)
        }

    total_flashes = 0

    for _ in range(100):
        # increment by one
        squids = {k: v + 1 for k, v in squids.items()}

        to_flash = [squid for squid, val in squids.items() if val > 9]

        while to_flash:
            squid = to_flash.pop()
            if squids[squid] == 0:
                continue
            total_flashes += 1
            squids[squid] = 0
            for adj_squid in adjacent(*squid):
                if adj_squid in squids and squids[adj_squid] != 0:
                    squids[adj_squid] += 1
                    if squids[adj_squid] > 9:
                        to_flash.append(adj_squid)

    return total_flashes


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
