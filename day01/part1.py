import argparse
import itertools
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
199
200
208
210
200
207
240
269
260
263
"""


def compute(s: str) -> int:
    # parse
    depths = list(map(int, s.splitlines()))

    # prepare iterators
    first_it, second_it = itertools.tee(depths, 2)
    next(second_it)

    # sum the compared depths
    return sum(
        second_depth > first_depth
        for first_depth, second_depth in zip(first_it, second_it)
        )


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 7),
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
