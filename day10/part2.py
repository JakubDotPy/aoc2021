import argparse
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
"""
EXPECTED = 288957

pattern = r'\(\)|\[\]|\{\}|\<\>'

points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
    }

complement = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
    }


def compute(s: str) -> int:
    min_s = s

    # reduce using regex
    while re.findall(pattern, min_s):
        min_s = re.sub(pattern, '', min_s)

    total_points = []
    for line in min_s.splitlines():
        if any(c in line for c in points):
            continue
        line_score = 0
        for c in line[::-1]:
            line_score *= 5
            line_score += points[complement[c]]
        total_points.append(line_score)

    result = sorted(total_points)[len(total_points) // 2]

    return result


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
