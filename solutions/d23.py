from io import TextIOWrapper
from dataclasses import dataclass
from typing import Self
from collections import defaultdict


@dataclass(frozen=True, eq=True)
class Point:
    r: int
    c: int

    def __add__(self, other: Self) -> Self:
        return Point(self.r+other.r, self.c+other.c)

    def is_empty(self, ground):
        return self not in ground or ground[self] == '.'
    
    def is_elf(self, ground):
        if self not in ground:
            return False
        return ground[self] == '#'


N = Point(1,0)
S = Point(-1,0)
W = Point(0,-1)
E = Point(0,1)


def north(pos, ground, proposal, potential):
    if (pos+N).is_empty(ground) and (pos+N+W).is_empty(ground) and (pos+N+E).is_empty(ground):
        proposal[pos] = pos+N
        potential[pos+N] += 1
        return True
    return False


def south(pos, ground, proposal, potential):
    if (pos+S).is_empty(ground) and (pos+S+W).is_empty(ground) and (pos+S+E).is_empty(ground):
        proposal[pos] = pos+S
        potential[pos+S] += 1
        return True
    return False


def west(pos, ground, proposal, potential):
    if (pos+W).is_empty(ground) and (pos+S+W).is_empty(ground) and (pos+N+W).is_empty(ground):
        proposal[pos] = pos+W
        potential[pos+W] += 1
        return True
    return False


def east(pos, ground, proposal, potential):
    if (pos+E).is_empty(ground) and (pos+N+E).is_empty(ground) and (pos+S+E).is_empty(ground):
        proposal[pos] = pos+E
        potential[pos+E] += 1
        return True
    return False


def main(file: TextIOWrapper):
    grid = [line.strip() for line in file.readlines()]
    ground: defaultdict[Point, str] = defaultdict(lambda: '.')
    num_elves = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            ground[Point(len(grid)-r,c)] = grid[r][c]
            num_elves += grid[r][c] == '#'

    check = [north, south, west, east]

    for i in range(10):
        proposal = {}
        potential = defaultdict(int)
        for pos, char in ground.items():
            if char == '#':
                found = False
                for r in range(-1,2):
                    for c in range(-1,2):
                        if r == c == 0:
                            continue
                        if Point(pos.r+r,pos.c+c).is_elf(ground):
                            found = True
                            break
                    if found:
                        break
                if not found:
                    continue

                for func in range(i, i+4):
                    if check[func%4](pos, ground, proposal, potential):
                        break

        new_ground = defaultdict(lambda: '.')
        for pos, char in ground.items():
            if char == '#':
                if pos in proposal and potential[proposal[pos]] == 1:
                    new_ground[proposal[pos]] = '#'
                else:
                    new_ground[pos] = '#'
        ground = new_ground

        elf_check = 0
        for char in ground.values():
            elf_check += char == '#'
        assert elf_check == num_elves
 
    min_r = 1e9
    min_c = 1e9
    max_r = -1e9
    max_c = -1e9
    for pt in ground:
        if ground[pt] == '#':
            min_r = min(min_r, pt.r)
            max_r = max(max_r, pt.r)
            min_c = min(min_c, pt.c)
            max_c = max(max_c, pt.c)
    
    count = 0
    for r in range(min_r, max_r+1):
        for c in range(min_c, max_c+1):
            count += ground[Point(r,c)] == '.'
    
    curr_round = 10
    num_moved = 1
    while num_moved > 0:
        curr_round += 1
        proposal = {}
        potential = defaultdict(int)
        for pos, char in ground.items():
            if char == '#':
                found = False
                for r in range(-1,2):
                    for c in range(-1,2):
                        if r == c == 0:
                            continue
                        if Point(pos.r+r,pos.c+c).is_elf(ground):
                            found = True
                            break
                    if found:
                        break
                if not found:
                    continue

                for func in range(curr_round-1, curr_round+3):
                    if check[func%4](pos, ground, proposal, potential):
                        break

        num_moved = 0
        new_ground = defaultdict(lambda: '.')
        for pos, char in ground.items():
            if char == '#':
                if pos in proposal and potential[proposal[pos]] == 1:
                    num_moved += 1
                    new_ground[proposal[pos]] = '#'
                else:
                    new_ground[pos] = '#'
        ground = new_ground

        min_r = 1e9
        min_c = 1e9
        max_r = -1e9
        max_c = -1e9
        for pt in ground:
            if ground[pt] == '#':
                min_r = min(min_r, pt.r)
                max_r = max(max_r, pt.r)
                min_c = min(min_c, pt.c)
                max_c = max(max_c, pt.c)
    
    return count,curr_round

