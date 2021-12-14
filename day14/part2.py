import argparse
import os.path
from collections import Counter

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""
EXPECTED = 2188189693529


def parse(s):
    polymer, pair_lines = s.split('\n\n')
    pairs = {}
    for line in pair_lines.splitlines():
        pair, insert = line.split(' -> ')
        pairs[pair] = insert
    return polymer, pairs


def compute(s: str) -> int:
    polymer, pairs = parse(s)

    char_counter = Counter(polymer)
    pair_counter = Counter()
    for m, n in zip(polymer, polymer[1:]):
        pair_counter[m + n] = 1

    for _ in range(40):
        new_pair_counter = Counter()
        for polymer_pair, count in pair_counter.items():
            if subst := pairs.get(polymer_pair):
                new_pair_counter[polymer_pair[0] + subst] += count
                new_pair_counter[subst + polymer_pair[1]] += count
                char_counter[subst] += count
        pair_counter = new_pair_counter

    count_vals = sorted(v for v in char_counter.values())

    return count_vals[-1] - count_vals[0]


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
