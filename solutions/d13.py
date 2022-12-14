from io import TextIOWrapper

import json
from functools import cmp_to_key


def compare(left: list, right: list, level=0) -> int:
    for l,r in zip(left, right):
        if isinstance(l, int):
            if isinstance(r, int):
                if l > r:
                    return 1
                elif l < r:
                    return -1
            else:
                v = compare([l], r, level+4)
                if v != 0:
                    return v
        elif isinstance(r, int):
            v = compare(l, [r], level+4)
            if v != 0:
                return v
        else:
            v = compare(l, r, level+4)
            if v != 0:
                return v
    if len(left) < len(right):
        return -1
    elif len(right) < len(left):
        return 1
    return 0


def main(file: TextIOWrapper):
    packets = [[[2]], [[6]]]
    num_less = 0
    for i, line in enumerate(file.read().split('\n\n')):
        left, right = map(json.loads, line.strip().split('\n'))
        if compare(left, right) < 0:
            num_less += i + 1
        packets.append(left)
        packets.append(right)

    isort = sorted(packets, key=cmp_to_key(compare))
    prod = 1
    for i,elem in enumerate(isort):
        if elem == [[2]] or elem == [[6]]:
            prod *= i + 1
    return num_less, prod

# def old():
#     lines = file.read()
#     pairs = [(lambda pair: (json.loads(pair[0]), json.loads(pair[1])))(pair.strip().split('\n')) for pair in lines.split('\n\n')]
#     s = 0
#     packets = [[[2]],[[6]]]
#     for i, (left, right) in enumerate(pairs):
#         if compare(left, right) < 0:
#             s += i + 1
#         packets.append(left)
#         packets.append(right)

#     isort = sorted(packets, key=cmp_to_key(compare))
#     prod = 1
#     for i,elem in enumerate(isort):
#         if elem == [[2]] or elem == [[6]]:
#             prod *= i + 1
#     return s,prod
