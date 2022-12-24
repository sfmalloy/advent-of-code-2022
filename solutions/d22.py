import re
from io import TextIOWrapper
from enum import Enum
from dataclasses import dataclass
from typing import Self


class Dir(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    def __add__(self, other: int) -> Self:
        return Dir((self.value + other) % 4)


@dataclass
class Me:
    facing: Dir
    r: int
    c: int
    curr_side: int = 0


@dataclass
class Neighbor:
    side_num: int
    facing: Dir


@dataclass
class Side:
    r_min: int
    r_max: int
    c_min: int
    c_max: int

    right: Neighbor
    down: Neighbor
    left: Neighbor
    up: Neighbor


def print_grid(grid: list[str], me: Me):
    s = ''
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if me.r == r and me.c == c:
                s += 'O'
            else:
                s += grid[r][c]
        s += '\n'
    
    # os.system('clear')
    print(s, end='\n\n\n')
    # time.sleep(0.25)


def walk_cube(grid: list[str], dirs: list[tuple[int, int]]):
    walk = {
        Dir.UP: (-1, 0),
        Dir.RIGHT: (0, 1),
        Dir.DOWN: (1, 0),
        Dir.LEFT: (0, -1)
    }

    # 3 x 4 cube net
    # I made my IRL paper cube 1-indexed by accident so this has to be 1-indexed now :)
    sides: list[Side] = [
        None,
        Side(0,49,100,149,right=Neighbor(4,Dir.LEFT),down=Neighbor(3,Dir.LEFT),left=Neighbor(2,Dir.LEFT),up=Neighbor(6,Dir.UP)),       # 1
        Side(0,49,50,99,right=Neighbor(1,Dir.RIGHT),down=Neighbor(3,Dir.DOWN),left=Neighbor(5,Dir.RIGHT),up=Neighbor(6,Dir.RIGHT)),    # 2
        Side(50,99,50,99,right=Neighbor(1,Dir.UP),down=Neighbor(4,Dir.DOWN),left=Neighbor(5,Dir.DOWN),up=Neighbor(2,Dir.UP)),          # 3
        Side(100,149,50,99,right=Neighbor(1,Dir.LEFT),down=Neighbor(6,Dir.LEFT),left=Neighbor(5,Dir.LEFT),up=Neighbor(3,Dir.UP)),      # 4
        Side(100,149,0,49,right=Neighbor(4,Dir.RIGHT),down=Neighbor(6,Dir.DOWN),left=Neighbor(2,Dir.RIGHT),up=Neighbor(3,Dir.RIGHT)),  # 5
        Side(150,199,0,49,right=Neighbor(4,Dir.UP),down=Neighbor(1,Dir.DOWN),left=Neighbor(2,Dir.DOWN),up=Neighbor(5,Dir.UP))          # 6
    ]
    me = Me(Dir.RIGHT, 0, grid[0].index('.'), curr_side=2)

    for dist, rot in dirs:
        walked = 0
        
        while walked < dist:
            dr, dc = walk[me.facing]
            r = me.r + dr
            c = me.c + dc
            side = sides[me.curr_side]
            old_facing = me.facing
            old_side = me.curr_side
            if r > side.r_max: # going off down
                assert old_facing == Dir.DOWN
                me.facing = side.down.facing
                me.curr_side = side.down.side_num
                if me.facing == Dir.LEFT:
                    r = sides[me.curr_side].r_min + (c % 50)
                    c = sides[me.curr_side].c_max
                elif me.facing == Dir.DOWN:
                    r = sides[me.curr_side].r_min
                    c = sides[me.curr_side].c_min + (c % 50)
            elif r < side.r_min: # going off up
                assert old_facing == Dir.UP
                me.facing = side.up.facing
                me.curr_side = side.up.side_num
                if me.facing == Dir.RIGHT:
                    r = sides[me.curr_side].r_min + (c % 50)
                    c = sides[me.curr_side].c_min
                elif me.facing == Dir.UP:
                    r = sides[me.curr_side].r_max
                    c = sides[me.curr_side].c_min + (c % 50)
            elif c > side.c_max: # going off right
                assert old_facing == Dir.RIGHT
                me.facing = side.right.facing
                me.curr_side = side.right.side_num
                if me.facing == Dir.LEFT:
                    r = sides[me.curr_side].r_max - (r % 50)
                    c = sides[me.curr_side].c_max
                elif me.facing == Dir.UP:
                    c = sides[me.curr_side].c_min + (r % 50)
                    r = sides[me.curr_side].r_max
                elif me.facing == Dir.RIGHT:
                    c = sides[me.curr_side].c_min
            elif c < side.c_min: # going off left
                assert old_facing == Dir.LEFT
                me.facing = side.left.facing
                me.curr_side = side.left.side_num
                if me.facing == Dir.RIGHT:
                    r = sides[me.curr_side].r_max - (r % 50)
                    c = sides[me.curr_side].c_min
                elif me.facing == Dir.DOWN:
                    c = sides[me.curr_side].c_min + (r % 50)
                    r = sides[me.curr_side].r_min
                elif me.facing == Dir.LEFT:
                    c = sides[me.curr_side].c_max
            assert r >= 0
            assert c >= 0
            if grid[r][c] == '#':
                me.facing = old_facing
                me.curr_side = old_side
                break
            assert grid[r][c] != '#'
            me.r = r
            me.c = c
            walked += 1
        me.facing += rot

    return 1000 * (me.r+1) + 4 * (me.c+1) + me.facing.value


def walk_flat(grid: list[str], dirs: list[tuple[int, int]]):
    me = Me(Dir.RIGHT, 0, grid[0].index('.'))

    walk = {
        Dir.UP: (-1, 0),
        Dir.RIGHT: (0, 1),
        Dir.DOWN: (1, 0),
        Dir.LEFT: (0, -1)
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
    p2 = walk_cube(grid, dirs)

    return p1,p2

