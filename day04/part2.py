import argparse
import os.path
from itertools import chain

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


class Board:
    def __init__(self, rows):
        self.rows = [set(map(int, row.split())) for row in rows.splitlines()]
        self.columns = [set(col) for col in zip(*self.rows)]

    def mark_number(self, number):
        for row in self.rows:
            try:
                row.remove(number)
            except KeyError:
                pass
        for col in self.columns:
            try:
                col.remove(number)
            except KeyError:
                pass

    @property
    def remaining_numbers(self):
        return set(
            chain(chain.from_iterable(self.rows),
                  chain.from_iterable(self.columns),
                  )
            )

    @property
    def is_winning(self):
        return any(not row for row in self.rows) \
               or any(not col for col in self.columns)

    def evaluate(self, number):
        return sum(self.remaining_numbers) * number


def compute(s: str) -> int:
    # parse lines
    numbers_s, *blocks = s.split('\n\n')

    numbers = map(int, numbers_s.split(','))

    boards = [Board(block) for block in blocks]

    empty_boards = set()

    for number in numbers:
        boards = [board for board in boards if board not in empty_boards]
        for board in boards:
            board.mark_number(number)
            if board.is_winning:
                if len(boards) == 1:
                    return board.claculate(number)
                empty_boards.add(board)


@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S, 1924),
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
