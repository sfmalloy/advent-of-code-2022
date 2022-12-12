from io import TextIOWrapper

from queue import PriorityQueue
from dataclasses import dataclass, field


@dataclass
class Point:
    r: int
    c: int


@dataclass(order=True)
class Node:
    pos: Point = field(compare=False)
    visited: bool = field(compare=False)
    elevation: int = field(compare=False)
    todo: bool = field(default=False, compare=False)
    dist: int = 1000000


def find_start(grid: list[list[str]]):
    for row_num, row in enumerate(grid):
        for col_num, col in enumerate(row):
            if col == 'S':
                return Point(row_num, col_num)
    return Point(0, 0)


def find_end(grid: list[list[str]]):
    for row_num, row in enumerate(grid):
        for col_num, col in enumerate(row):
            if col == 'E':
                return Point(row_num, col_num)
    return Point(0, 0)


def check_no_reset(src: Node, dst: Node, dist: int, unvisited: PriorityQueue[Node]):
    if not dst.visited and dst.elevation - src.elevation <= 1:
        dst.dist = min(dist, dst.dist)
        if not dst.todo:
            dst.todo = True
            unvisited.put(dst)


def shortest_from_start(letter_grid: list[list[str]], start: Point, end: Point) -> int:
    grid = [[Node(Point(r, c), False, ord(col)-ord('a')) for c, col in enumerate(row)] 
            for r, row in enumerate(letter_grid)]

    grid[start.r][start.c].dist = 0
    unvisited: PriorityQueue[Node] = PriorityQueue()
    unvisited.put(grid[start.r][start.c])

    while not unvisited.empty():
        curr = unvisited.get()
        curr.visited = True
        if curr.pos.r == end.r and curr.pos.c == end.c:
            return curr.dist
        if curr.pos.r + 1 < len(grid):
            check_no_reset(curr, grid[curr.pos.r+1][curr.pos.c], curr.dist + 1, unvisited)
        if curr.pos.r - 1 >= 0:
            check_no_reset(curr, grid[curr.pos.r-1][curr.pos.c], curr.dist + 1, unvisited)
        if curr.pos.c + 1 < len(grid[curr.pos.r]):
            check_no_reset(curr, grid[curr.pos.r][curr.pos.c+1], curr.dist + 1, unvisited)
        if curr.pos.c - 1 >= 0:
            check_no_reset(curr, grid[curr.pos.r][curr.pos.c-1], curr.dist + 1, unvisited)

    return 1000000


def check_reset(src: Node, dst: Node, dist: int, unvisited: PriorityQueue[Node]):
    if not dst.visited and dst.elevation - src.elevation <= 1:
        dst.dist = min(dist if dst.elevation else 0, dst.dist)
        if not dst.todo:
            dst.todo = True
            unvisited.put(dst)


def shortest_from_closest(letter_grid: list[list[str]], start: Point, end: Point) -> int:
    grid = [[Node(Point(r, c), False, ord(col)-ord('a')) for c, col in enumerate(row)] 
              for r, row in enumerate(letter_grid)]

    grid[start.r][start.c].dist = 0
    unvisited: PriorityQueue[Node] = PriorityQueue()
    unvisited.put(grid[start.r][start.c])

    while not unvisited.empty():
        curr = unvisited.get()
        curr.visited = True
        if curr.pos.r == end.r and curr.pos.c == end.c:
            return curr.dist
        if curr.pos.r + 1 < len(grid):
            check_reset(curr, grid[curr.pos.r + 1][curr.pos.c], curr.dist + 1, unvisited)
        if curr.pos.r - 1 >= 0:
            check_reset(curr, grid[curr.pos.r-1][curr.pos.c], curr.dist + 1, unvisited)
        if curr.pos.c + 1 < len(grid[curr.pos.r]):
            check_reset(curr, grid[curr.pos.r][curr.pos.c+1], curr.dist+1, unvisited)
        if curr.pos.c - 1 >= 0:
            check_reset(curr, grid[curr.pos.r][curr.pos.c-1], curr.dist+1, unvisited)

    return 1000000


def main(file: TextIOWrapper) -> tuple:
    letter_grid = [list(line.strip()) for line in file.readlines()]
    start = find_start(letter_grid)
    end = find_end(letter_grid)
    letter_grid[start.r][start.c] = 'a'
    letter_grid[end.r][end.c] = 'z'
    return shortest_from_start(letter_grid, start, end), shortest_from_closest(letter_grid, start, end)
