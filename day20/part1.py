import argparse
import os.path
from itertools import chain
from itertools import product

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
EXPECTED = 35


def parse(s):
    iea_chunk, image = s.split('\n\n')

    iea_hash_set = set(
        i
        for i, c in enumerate(
            chain.from_iterable(iea_chunk.splitlines())
            )
        if c == '#'
        )

    img = {
        (x, y): c
        for y, row in enumerate(image.splitlines())
        for x, c in enumerate(row)
        }

    return iea_hash_set, img


def get_enhanced_coords(img):
    x_vals = set(x for x, y in img)
    y_vals = set(y for x, y in img)
    min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
    min_y, max_y = min(y_vals) - 1, max(y_vals) + 1
    return product(range(min_y, max_y + 1), range(min_x, max_x + 1))


def get_surround_str(img, pos, loop_num):
    coords_diff = sorted(product((-1, 0, 1), (-1, 0, 1)), key=lambda x: x[1])
    x, y = pos
    default = '#' if loop_num % 2 else '.'
    img_list = [
        img.get((x + dx, y + dy), default)
        for dx, dy in coords_diff
        ]
    return ''.join(img_list)


def str_to_num(s):
    bin_s = s \
        .replace('#', '1') \
        .replace('.', '0')
    return int(bin_s, base=2)


def print_img(img):
    x_vals = set(x for x, y in img)
    y_vals = set(y for x, y in img)
    min_x, max_x = min(x_vals), max(x_vals)
    min_y, max_y = min(y_vals), max(y_vals)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            print(img[(x, y)], end='')
        print()


def compute(s: str) -> int:
    # image enhancement algorythm
    iea_hash_set, img = parse(s)

    for loop_num in range(2):
        wider_coords = get_enhanced_coords(img)
        new_img = dict()
        for coord in wider_coords:
            coord_str = get_surround_str(img, coord, loop_num)
            iea_index = str_to_num(coord_str)
            new_img[coord] = '#' if iea_index in iea_hash_set else '.'
        img = new_img

    return sum(v == '#' for v in img.values())


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
