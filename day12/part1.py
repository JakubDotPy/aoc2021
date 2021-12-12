import argparse
import collections
import os.path

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
# NOTE: paste test text here
INPUT_S = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""
EXPECTED = 10


def compute(s: str) -> int:
    graph = collections.defaultdict(list)
    for line in s.splitlines():
        a, b = line.split('-')
        graph[a].append(b)
        graph[b].append(a)  # bidirectional

    complete_paths = set()
    paths_to_do = collections.deque([('start',)])
    while paths_to_do:
        path = paths_to_do.popleft()
        if path[-1] == 'end':
            # path leading to end found
            complete_paths.add(path)
            continue
        for choice in graph[path[-1]]:
            if choice.isupper() or choice not in path:
                paths_to_do.append((*path, choice))  # append the extended path

    return len(complete_paths)


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
