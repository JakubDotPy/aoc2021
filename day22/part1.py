import argparse
import itertools
import os.path
import re

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S_1 = """\
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
"""
EXPECTED_1 = 39
INPUT_S_2 = """\
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
"""
EXPECTED_2 = 590784


def parse_line(line):
    state, coords = line.split()
    on = True if state == 'on' else False
    nums = re.findall(r'-?\d+', coords)

    # break early due to lim 50
    if not all(-50 <= c <= 50 for c in map(int, nums)):
        return None, None

    x_min, x_max, y_min, y_max, z_min, z_max = map(int, nums)
    x_range = range(x_min, x_max + 1)
    y_range = range(y_min, y_max + 1)
    z_range = range(z_min, z_max + 1)
    coords = set(itertools.product(x_range, y_range, z_range))
    return on, coords


def lim50_filter(coord):
    return all(-50 <= c <= 50 for c in coord)


def compute(s: str) -> int:
    on_coords = set()

    lines = s.splitlines()
    for line in lines:
        on, coords = parse_line(line)

        if not coords:
            continue

        coords = set(filter(lim50_filter, coords))

        if on:
            on_coords |= coords
        else:
            on_coords -= coords

    return len(on_coords)

@pytest.mark.solved
@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
            (INPUT_S_1, EXPECTED_1),
            (INPUT_S_2, EXPECTED_2),
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
