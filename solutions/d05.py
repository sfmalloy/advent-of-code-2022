from io import TextIOWrapper
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class Move:
    amt: int
    src: int
    dst: int

def move_one(crates: list[list[str]], m: Move):
    for _ in range(m.amt):
        crates[m.dst].append(crates[m.src].pop())

def move_multi(crates: list[list[str]], m: Move):
    for i in range(m.amt):
        crates[m.dst].append(crates[m.src][-m.amt+i])
    for _ in range(m.amt):
        crates[m.src].pop()

def main(file: TextIOWrapper):
    init,dirs = file.read().split('\n\n')
    crates = [[c for c in reversed(col) if c.isalpha()] for col in list(zip(*init.split('\n'))) if col[-1].isnumeric()]
    moves = [(lambda row:Move(int(row[1]), int(row[3])-1, int(row[5])-1))(r.split()) for r in dirs.split('\n')[:-1]]
    epic_crates = deepcopy(crates)

    for m in moves:
        move_one(crates, m)
        move_multi(epic_crates, m)
    print(''.join([c[-1] for c in crates]))
    print(''.join([c[-1] for c in epic_crates]))
