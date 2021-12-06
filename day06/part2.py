import argparse
import os.path
from collections import Counter

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
3,4,3,1,2
"""


class FishCounter(Counter):

    def advance(self):
        new = self[0]
        # advance regulars
        for n in range(8):
            self[n] = self[n + 1]
        # advance special
        self[8] = new
        self[6] += new

    @property
    def total_count(self):
        return sum(self.values())


def compute(s: str) -> int:
    # parse numbers
    nums = [int(n) for n in s.split(',')]
    fc = FishCounter(nums)

    for _ in range(256):
        fc.advance()

    return fc.total_count


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 26984457539),
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
