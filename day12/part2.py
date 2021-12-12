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
EXPECTED = 36


def compute(s: str) -> int:
    graph = collections.defaultdict(set)
    for line in s.splitlines():
        a, b = line.split('-')
        graph[a].add(b)
        graph[b].add(a)  # bidirectional

    complete_paths = set()
    paths_to_do = collections.deque([(('start',), False)])  # False means small cell was visited twice
    while paths_to_do:
        path, small_twice = paths_to_do.popleft()
        if path[-1] == 'end':
            # path leading to end found
            complete_paths.add(path)
            continue
        for choice in graph[path[-1]] - {'start'}:  # remove the start from possible moves to not return there
            if choice.isupper():
                # continue as usual
                paths_to_do.append(((*path, choice), small_twice))
            elif choice not in path:
                paths_to_do.append(((*path, choice), small_twice))
            elif not small_twice and choice in path:
                paths_to_do.append(((*path, choice), True))

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
