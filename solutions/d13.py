from io import TextIOWrapper

import json
from enum import Enum
from copy import deepcopy

class Comp(Enum):
    LESS = 0
    GREATER = 1
    EQUAL = 2

def compare(left: list, right: list, level=0) -> Comp:
    for l,r in zip(left, right):
        if isinstance(l, int):
            if isinstance(r, int):
                if l > r:
                    return Comp.GREATER
                elif l < r:
                    return Comp.LESS
            else:
                v = compare([l], r, level+4)
                if v != Comp.EQUAL:
                    return v
        else:
            if isinstance(r, int):
                v = compare(l, [r], level+4)
                if v != Comp.EQUAL:
                    return v
            else:
                v = compare(l, r, level+4)
                if v != Comp.EQUAL:
                    return v
    if len(left) < len(right):
        return Comp.LESS
    elif len(right) < len(left):
        return Comp.GREATER
    return Comp.EQUAL


def insertion_sort(lst: list) -> list:
    for i in range(1, len(lst)):
        j = i
        elem = lst[i]
        while compare(lst[j-1], elem) == Comp.GREATER:
            lst[j] = lst[j - 1]
            if j == 0:
                break
            j -= 1
        lst[j] = elem
    return lst


def merge(lhs: list, rhs: list) -> list:
    lptr = 0
    rptr = 0
    final = []
    while lptr < len(lhs) and rptr < len(rhs):
        if compare(lhs[lptr], rhs[rptr]):
            final.append(lhs)
            lptr += 1
        else:
            final.append(rhs)
            rptr += 1
    if lptr == len(lhs):
        return final + rhs[rptr:]
    elif rptr == len(rhs):
        return final + lhs[lptr:]
    return final


def merge_sort(lst: list) -> list:
    if len(lst) <= 3:
        return insertion_sort(lst)
    lhs = merge_sort(lst[0:len(lst)//2])
    rhs = merge_sort(lst[len(lst)//2:])
    print(lhs,rhs)
    return merge(lhs, rhs)


def main(file: TextIOWrapper):
    lines = file.read()
    pairs = [(lambda pair: (json.loads(pair[0]), json.loads(pair[1])))(pair.strip().split('\n')) for pair in lines.split('\n\n')]
    s = 0
    packets = [[[2]],[[6]]]
    for i, (left, right) in enumerate(pairs):
        if compare(left, right) == Comp.LESS:
            s += i + 1
        packets.append(left)
        packets.append(right)

    isort = insertion_sort(packets)
    prod = 1
    for i,elem in enumerate(isort):
        if elem == [[2]] or elem == [[6]]:
            prod *= i + 1
    return s,prod
