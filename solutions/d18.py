from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque

@dataclass(frozen=True, eq=True)
class Cube:
    x: int
    y: int
    z: int


@dataclass
class Vec3:
    x: int
    y: int
    z: int


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
    while len(q) > 0:
        curr = q.pop()
        while curr in seen:
            curr = q.pop()
        if curr in cubes:
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
