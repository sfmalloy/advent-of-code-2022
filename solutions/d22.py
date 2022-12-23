import re
import math
from io import TextIOWrapper
from enum import Enum
from dataclasses import dataclass
from typing import Self
from collections import defaultdict


class Direction(Enum):
    NORTH = 3
    EAST = 0
    SOUTH = 1
    WEST = 2

    def __add__(self, other: int) -> Self:
        return Direction((self.value + other) % 4)


@dataclass
class Me:
    facing: Direction
    r: int
    c: int


def print_grid(grid: list[str], me: Me):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if me.r == r and me.c == c:
                s += 'O'
            else:
                s += grid[r][c]
        s += '\n'
    print(s)


def walk_flat(grid: list[str], dirs: list[tuple[int, int]]):
    me = Me(Direction.EAST, 0, grid[0].index('.'))

    walk = {
        Direction.NORTH: (-1, 0),
        Direction.EAST: (0, 1),
        Direction.SOUTH: (1, 0),
        Direction.WEST: (0, -1)
    }

    for dist, rot in dirs:
        walked = 0
        dr, dc = walk[me.facing]

        while walked < dist:
            r = (me.r + dr) % len(grid)
            c = (me.c + dc) % len(grid[r])
            walked += 1
            while grid[r][c] == ' ':
                r = (r + dr) % len(grid)
                c = (c + dc) % len(grid[r])
            if grid[r][c] == '#':
                break
            me.r = r
            me.c = c
        me.facing += rot

    return 1000 * (me.r+1) + 4 * (me.c+1) + me.facing.value


def main(file: TextIOWrapper):
    tiles, path_line = file.read().rstrip().split('\n\n')
    grid = [line for line in tiles.split('\n')]
    me = Me(Direction.EAST, 0, grid[0].index('.'))

    dirs = []
    dir_iter = re.finditer(r'[0-9]*(R|L){0,1}', path_line)
    for matched in dir_iter:
        direction = matched.group(0)
        rot = 0
        dist = 0
        if len(direction) > 0:
            if direction[-1] == 'R' or direction[-1] == 'L':
                rot = 1 if direction[-1] == 'R' else -1
                direction = direction[:-1]
            if len(direction) > 0:
                dist = int(direction)
            dirs.append((dist, rot))
    p1 = walk_flat(grid, dirs)

    return p1,-1

