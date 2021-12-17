import argparse
import itertools
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
target area: x=20..30, y=-10..-5
"""
EXPECTED = 112


class Probe:
    def __init__(self, start_pos, start_velocity):
        self.x, self.y = start_pos
        self.vx, self.vy = start_velocity

    @property
    def pos(self):
        return self.x, self.y


class Simulation:

    def __init__(self, area):
        self.probe = None
        self.area = area
        self.lim_x = max(p[0] for p in area)
        self.lim_y = min(p[1] for p in area)

        self.hits = 0
        self.misses = 0

    def step(self):
        self.probe.x += self.probe.vx
        self.probe.y += self.probe.vy
        if self.probe.vx != 0:
            self.probe.vx = self.probe.vx + 1 if self.probe.vx < 0 else self.probe.vx - 1
        self.probe.vy -= 1

    @property
    def overshoot(self):
        # return self.probe.x > self.lim_x or self.probe.y < self.lim_y
        return self.probe.y < self.lim_y

    @property
    def in_area(self):
        return self.probe.pos in self.area

    def run(self, velocity):
        max_y = 0
        self.probe = Probe((0, 0), velocity)

        while True:
            max_y = max(max_y, self.probe.y)
            self.step()
            if self.in_area:
                self.hits += 1
                break
            if self.overshoot:
                self.misses += 1
                break


def parse_area(s):
    coords = re.findall(r'-?\d+', s)
    x1, x2, y1, y2 = map(int, coords)
    return set(itertools.product(range(x1, x2 + 1), range(y1, y2 + 1)))


def compute(s: str) -> int:
    target_area = parse_area(s)
    s = Simulation(target_area)

    for attempt, (vx, vy) in enumerate(itertools.product(range(1, s.lim_x * 3), range(s.lim_y * 3, -s.lim_y * 3))):
        # if attempt % 500 == 0:
        #     print(f'{attempt=}, {s.hits=}, {s.misses=}')
        s.run((vx, vy))

    return s.hits


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
