import argparse
import itertools
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
Player 1 starting position: 4
Player 2 starting position: 8
"""
EXPECTED = 739785


class Pawn:
    def __init__(self, position):
        self.score = 0
        self.board = itertools.cycle(range(1, 11))
        # initial move
        for _ in range(position):
            self.position = next(self.board)

    def move(self, steps):
        for _ in range(steps):
            self.position = next(self.board)
        self.score += self.position

    @property
    def is_winner(self):
        return self.score >= 1_000

    def __repr__(self):
        return f'Pawn({self.position})'


class DeterministicDice:
    def __init__(self, sides):
        self.nums = itertools.cycle(range(1, sides + 1))
        self.times_rolled = 0

    def get_result(self, num_rols):
        """Get result by suming next three numbers."""
        self.times_rolled += num_rols
        return sum(itertools.islice(self.nums, num_rols))


def parse_players(s):
    positions = (
        int(row.split()[-1])
        for row in s.splitlines()
        )
    return [Pawn(pos) for pos in positions]


def compute(s: str) -> int:
    players = parse_players(s)
    dice = DeterministicDice(100)

    winner_found = False
    while True:
        for p in players:
            steps = dice.get_result(num_rols=3)
            p.move(steps)
            if p.is_winner:
                winner_found = True
                break
        if winner_found:
            break

    loser_score = next(p.score for p in players if not p.is_winner)

    return loser_score * dice.times_rolled


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
