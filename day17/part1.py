import argparse
import itertools
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
target area: x=20..30, y=-10..-5
"""
EXPECTED = 45


def parse_area(s):
    coords = re.findall(r'-?\d+', s)
    x1, x2, y1, y2 = map(int, coords)
    return set(itertools.product(range(x1, x2 + 1), range(y1, y2 + 1)))


def compute(s: str) -> int:
    target_area = parse_area(s)

    # NOTE: calculated manually on whiteboard

    low_y = min(p[1] for p in target_area)
    low_bound = abs(low_y) - 1

    max_height = (low_bound * (low_bound + 1)) // 2

    return max_height


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
