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

num_length = 0  # will be reassigned later


def count_bits(lines):
    transposed = zip(*lines)
    mcb_list = []
    lcb_list = []

    for column in transposed:
        c = Counter({'0': 0, '1': 0})
        c.update(Counter(column))
        mc_bit = c.most_common()
        mcb_list.append(mc_bit[0])
        lcb_list.append(mc_bit[1])

    return lcb_list, mcb_list


def oxy_filter(mcb, lcb, pos, number):
    char = '1' if mcb[1] == lcb[1] else mcb[0]
    return number[pos] == char


def co2_filter(mcb, lcb, pos, number):
    char = '0' if mcb[1] == lcb[1] else lcb[0]
    return number[pos] == char


def reduce_list(nums, filter_fn):
    for i in range(num_length):
        # count new significances
        lcb_list, mcb_list = count_bits(nums)

        # filter the list
        nums = [
            num for num in nums
            if filter_fn(mcb_list[i], lcb_list[i], i, num)
            ]

        # halt condition
        if len(nums) == 1:
            return nums


def compute(s: str) -> int:
    global num_length

    lines = s.splitlines()
    num_length = len(lines[0])

    oxy_list = reduce_list(lines.copy(), oxy_filter)
    co2_list = reduce_list(lines.copy(), co2_filter)

    gama = int(''.join(oxy_list), 2)
    epsilon = int(''.join(co2_list), 2)

    return gama * epsilon


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 230),
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
