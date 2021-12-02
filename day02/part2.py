import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""


def compute(s: str) -> int:
    # parse lines
    lines = s.splitlines()

    horizontal = 0
    depth = 0
    aim = 0

    for line in lines:
        direction, num = line.split()
        num = int(num)

        if direction == 'forward':
            horizontal += num
            depth += aim * num
        elif direction == 'down':
            aim += num
        elif direction == 'up':
            aim -= num

    return horizontal * depth


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 900),
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
