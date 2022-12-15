from io import TextIOWrapper
from dataclasses import dataclass
from time import sleep
from os import system


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int


def walk(start: Point, end: Point) -> set[Point]:
    res = set()
    if start.x == end.x:
        step = -1 if start.y > end.y else 1
        for y in range(start.y, end.y + step, step):
            res.add(Point(start.x, y))
    else:
        step = -1 if start.x > end.x else 1
        for x in range(start.x, end.x + step, step):
            res.add(Point(x, start.y))
    return res


def print_cave(min_x, min_y, max_x, max_y, walls, sand):
    s = ''
    for y in range(min_y-10, max_y+10):
        for x in range(min_x-10, max_x+10):
            curr = Point(x, y)
            if curr in walls:
                s += '#'
            elif curr in sand:
                s += 'o'
            else:
                s += '.'
        s += '\n'
    system('clear')
    print(s)
    sleep(0.1)


def is_wall(pt: Point, walls: set[Point], max_y: int, part2: bool) -> bool:
    return pt in walls or (part2 and pt.y == max_y)


def drop(src: Point, walls: set[Point], sand: set[Point], max_y: int, part2: bool):
    x = src.x
    y = src.y
    curr = Point(x, y)
    while not is_wall(curr, walls, max_y, part2) and curr not in sand and y <= max_y:
        y += 1
        curr = Point(x, y)
    if y > max_y:
        return False
    
    if is_wall(curr, walls, max_y, part2):
        y -= 1
        sand.add(Point(curr.x, y))
        return True
    while is_wall(curr, walls, max_y, part2) or curr in sand and curr.y <= max_y:
        left = Point(curr.x - 1, curr.y)
        right = Point(curr.x + 1, curr.y)
        if is_wall(left, walls, max_y, part2) or left in sand:
            if is_wall(right, walls, max_y, part2) or right in sand:
                sand.add(Point(curr.x, curr.y - 1))
                return True
            else:
                curr = Point(right.x, right.y + 1)
        else:
            curr = Point(left.x, left.y + 1)
            
    if not is_wall(Point(curr.x, curr.y + 1), walls, max_y, part2) or Point(curr.x, curr.y + 1) not in sand:
        return drop(curr, walls, sand, max_y, part2)
    return False


def main(file: TextIOWrapper):
    walls = set()
    min_x = 1000000
    min_y = 1000000
    max_x = -1000000
    max_y = -1000000
    for line in file.readlines():
        path = line.strip().split(' -> ')
        for i in range(len(path)-1):
            start = Point(*map(int, path[i].split(',')))
            end = Point(*map(int, path[i+1].split(',')))
            walls |= walk(start, end)

            min_x = min(min_x, start.x, end.x)
            max_x = max(max_x, start.x, end.x)
            min_y = min(min_y, start.y, end.y)
            max_y = max(max_y, start.y, end.y)

    src = Point(500, 0)
    sand = set()
    dropping = drop(src, walls, sand, max_y, False)
    while dropping:
        dropping = drop(src, walls, sand, max_y, False)
    part1 = len(sand)

    max_y += 2
    while src not in sand:
        drop(src, walls, sand, max_y, True)

    return part1, len(sand)
