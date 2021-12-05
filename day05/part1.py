import argparse
import itertools
import os.path
from collections import Counter
from itertools import chain

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


class Line:
    def __init__(self, start, end):
        self.x1, self.y1 = self.start = start
        self.x2, self.y2 = self.end = end

        self.x_slope = 1 if self.x1 <= self.x2 else -1
        self.y_slope = 1 if self.y1 <= self.y2 else -1

        self.points = self.calculate_points()

    def calculate_points(self):
        x_points = range(self.x1, self.x2 + self.x_slope, self.x_slope)
        y_points = range(self.y1, self.y2 + self.y_slope, self.y_slope)
        fill_value = x_points[0] if len(x_points) == 1 else y_points[0]
        return itertools.zip_longest(x_points, y_points, fillvalue=fill_value)

    @property
    def is_isometric(self):
        return self.x1 == self.x2 or self.y1 == self.y2

    def __repr__(self):
        return f'Line({self.start}, {self.end})'


def parse_line(row):
    start_s, end_s = row.split(' -> ')
    start = tuple(map(int, start_s.split(',')))
    end = tuple(map(int, end_s.split(',')))
    return start, end


def compute(s: str) -> int:
    lines = [
        Line(*parse_line(row))
        for row in s.splitlines()
        ]

    combined_points = Counter(
        chain.from_iterable(
            l.points
            for l in lines
            if l.is_isometric
            )
        )

    multiple_overlaps = sum(v > 1 for v in combined_points.values())

    return multiple_overlaps


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 5),
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
