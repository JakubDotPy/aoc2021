import argparse
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""
EXPECTED = 0


def parse(s):
    points_s, folds_s = s.split('\n\n')

    points = set()
    for point in points_s.splitlines():
        x, y = point.split(',')
        points.add((int(x), int(y)))

    folds = []
    for line in folds_s.splitlines():
        fold, num = line.split('=')
        folds.append((fold, int(num)))

    return points, folds


def do_folds(points, folds):
    for direction, split_val in folds:
        if direction.endswith('y'):
            # fold up
            points_to_fold = {point for point in points if point[1] > split_val}
            for point in points_to_fold:
                points.discard(point)
                points.add((point[0], 2 * split_val - point[1]))

        else:
            # fold left
            points_to_fold = {point for point in points if point[0] > split_val}
            for point in points_to_fold:
                points.discard(point)
                points.add((2 * split_val - point[0], point[1]))


def print_result(points):
    max_x = max(point[0] for point in points)
    may_y = max(point[1] for point in points)

    for y in range(may_y + 1):
        for x in range(max_x + 1):
            char = '#' if (x, y) in points else '.'
            print(char, end='')
        print()


def compute(s: str) -> int:
    points, folds = parse(s)
    do_folds(points, folds)
    print_result(points)
    return 0


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
