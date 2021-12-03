import argparse
import os.path
from collections import Counter

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""


def compute(s: str) -> int:
    lines = s.splitlines()
    transposed = zip(*lines)

    mcb_list = []
    lcb_list = []

    for column in transposed:
        c = Counter({'0': 0, '1': 0})
        c.update(Counter(column))
        mc_bit = c.most_common()
        mcb_list.append(mc_bit[0][0])
        lcb_list.append(mc_bit[1][0])

    gama = int(''.join(mcb_list), 2)
    epsilon = int(''.join(lcb_list), 2)

    return gama * epsilon


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 198),
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
