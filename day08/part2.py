import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""


def parse_reading(row):
    part1, part2 = row.split(' | ')
    end_parts = [''.join(sorted(s)) for s in part2.split()]
    digits = sorted((''.join(sorted(part)) for part in part1.split()), key=len)
    return digits, end_parts


def compute(s: str) -> int:
    # parse readings

    readings = s.splitlines()

    total = 0
    for line in readings:
        start, end = parse_reading(line)

        n_to_s = {}  # numbers to string mapping

        # find unique lengths
        n_to_s[1], n_to_s[7], n_to_s[4], *start, n_to_s[8] = start

        # numbers with length 6 -> n_len6 6, 0, 9
        n_len6 = {s for s in start if len(s) == 6}

        # six has only 1 overlap with one
        n_to_s[6] = next(s for s in n_len6 if len(set(s) & set(n_to_s[1])) == 1)
        # nine has 4 overlaps with four
        n_to_s[9] = next(s for s in n_len6 if len(set(s) & set(n_to_s[4])) == 4)
        # zero is the remaining of len 6
        n_to_s[0] = list(n_len6 - {n_to_s[6], n_to_s[9]})[0]

        # numbers with length 5 -> 5, 3, 2
        n_len5 = {s for s in start if len(s) == 5}

        # do the same overlapping as above
        n_to_s[5] = next(s for s in n_len5 if len(set(s) & set(n_to_s[6])) == 5)
        n_to_s[3] = next(s for s in n_len5 if len(set(s) & set(n_to_s[1])) == 2)
        n_to_s[2] = list(n_len5 - {n_to_s[5], n_to_s[3]})[0]

        # reverse dictionary
        s_to_n = {v: k for k, v in n_to_s.items()}

        total += sum(10 ** (3 - i) * s_to_n[end[i]] for i in range(4))

    return total


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 61229),
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
