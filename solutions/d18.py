from io import TextIOWrapper
from dataclasses import dataclass
from typing import Self
from collections import deque

@dataclass(frozen=True, eq=True)
class Cube:
    x: int
    y: int
    z: int

    def dist(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


@dataclass
class Vec3:
    x: int
    y: int
    z: int


def print_dim(start_a: int, end_a: int, start_b: int, end_b: int, valid: set):
    print(start_a, end_a, start_b, end_b)
    xy_str = ''
    for x in range(start_a - 1, end_a + 2):
        for y in range(start_b - 1, end_b + 2):
            if (x,y) in valid:
                xy_str += '#'
            else:
                xy_str += '.'
        xy_str += '\n'
    print(xy_str)


def main(file: TextIOWrapper):
    cubes = set(Cube(*map(int, line.strip().split(','))) for line in file.readlines())
    overlaps = 0
    smallest = Vec3(1000000000, 1000000000, 1000000000)
    largest = Vec3(-1000000000, -1000000000, -1000000000)
    for src in cubes:
        smallest.x = min(src.x, smallest.x)
        smallest.y = min(src.y, smallest.y)
        smallest.z = min(src.z, smallest.z)

        largest.x = max(src.x, largest.x)
        largest.y = max(src.y, largest.y)
        largest.z = max(src.z, largest.z)
        if Cube(src.x + 1, src.y, src.z) in cubes:
            overlaps += 1
        if Cube(src.x - 1, src.y, src.z) in cubes:
            overlaps += 1
        if Cube(src.x, src.y + 1, src.z) in cubes:
            overlaps += 1
        if Cube(src.x, src.y - 1, src.z) in cubes:
            overlaps += 1
        if Cube(src.x, src.y, src.z + 1) in cubes:
            overlaps += 1
        if Cube(src.x, src.y, src.z - 1) in cubes:
            overlaps += 1
    surface_area = (6 * len(cubes)) - overlaps

    smallest.x -= 1
    smallest.y -= 1
    smallest.z -= 1

    largest.x += 1
    largest.y += 1
    largest.z += 1

    exterior_area = 0
    q: deque[Cube] = deque([Cube(smallest.x, smallest.y, smallest.z)])
    seen: set[Cube] = set()
    exterior_cubes: set[Cube] = set()
    while len(q) > 0:
        curr = q.pop()
        while curr in seen:
            curr = q.pop()
        if curr in cubes:
            exterior_cubes.add(curr)
            exterior_area += 1
        elif (curr.x >= smallest.x and curr.x <= largest.x 
                and curr.y >= smallest.y and curr.y <= largest.y 
                and curr.z >= smallest.z and curr.z <= largest.z):
            seen.add(curr)
            if Cube(curr.x + 1, curr.y, curr.z) not in seen:
                q.appendleft(Cube(curr.x + 1, curr.y, curr.z))
            if Cube(curr.x - 1, curr.y, curr.z) not in seen:
                q.appendleft(Cube(curr.x - 1, curr.y, curr.z))
            if Cube(curr.x, curr.y + 1, curr.z) not in seen:
                q.appendleft(Cube(curr.x, curr.y + 1, curr.z))
            if Cube(curr.x, curr.y - 1, curr.z) not in seen:
                q.appendleft(Cube(curr.x, curr.y - 1, curr.z))
            if Cube(curr.x, curr.y, curr.z + 1) not in seen:
                q.appendleft(Cube(curr.x, curr.y, curr.z + 1))
            if Cube(curr.x, curr.y, curr.z - 1) not in seen:
                q.appendleft(Cube(curr.x, curr.y, curr.z - 1))

    return surface_area, exterior_area
