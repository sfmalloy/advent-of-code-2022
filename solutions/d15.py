from io import TextIOWrapper
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True, eq=True)
class Point:
    x: int
    y: int

@dataclass(frozen=True, eq=True)
class Sensor:
    pos: Point
    beacon_dist: int


@dataclass
class Interval:
    start: int
    stop: int

    def valid(self) -> bool:
        return self.start <= self.stop


def dist(a: Point, b: Point) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def get_ranges(y: int, beacons: defaultdict[Point, list[Sensor]]):
    ranges: list[Interval] = []
    for sensors in beacons.values():
        for s in sensors:
            if abs(y - s.pos.y) <= s.beacon_dist:
                dy = abs(y - s.pos.y)
                dx = s.beacon_dist - dy
                ranges.append(Interval(max(0, s.pos.x - dx), min(4000000, s.pos.x + dx)))
    
    for i, curr in enumerate(ranges):
        for j in range(len(ranges)):
            if not curr.valid():
                break
            if i != j and ranges[j].valid() and (curr.start >= ranges[j].start and curr.start <= ranges[j].stop):
                curr.start = ranges[j].stop + 1
        for j in range(len(ranges)):
            if not curr.valid():
                break
            if i != j and ranges[j].valid() and (curr.stop >= ranges[j].start and curr.stop <= ranges[j].stop):
                curr.stop = ranges[j].start - 1
    
    return [r for r in ranges if r.valid()]


def main(file: TextIOWrapper):
    beacons: defaultdict[Point, list[Sensor]] = defaultdict(list)
    for line in file.readlines():
        tokens = line.split()
        beacon = Point(int(tokens[8][2:-1]), int(tokens[9][2:]))
        sensor_pos = Point(int(tokens[2][2:-1]), int(tokens[3][2:-1]))
        beacon_dist = dist(beacon, sensor_pos)
        beacons[beacon].append(Sensor(sensor_pos, beacon_dist))

    y = 2000000
    ranges: list[Interval] = []
    for beacon, sensors in beacons.items():
        for s in sensors:
            if abs(y - s.pos.y) <= s.beacon_dist:
                dy = abs(y - s.pos.y)
                dx = s.beacon_dist - dy
                ranges.append(Interval(s.pos.x - dx, s.pos.x + dx))
    
    for i, curr in enumerate(ranges):
        for j in range(len(ranges)):
            if not curr.valid():
                break
            if i != j and ranges[j].valid() and (curr.start >= ranges[j].start and curr.start <= ranges[j].stop):
                curr.start = ranges[j].stop + 1
        for j in range(len(ranges)):
            if not curr.valid():
                break
            if i != j and ranges[j].valid() and (curr.stop >= ranges[j].start and curr.stop <= ranges[j].stop):
                curr.stop = ranges[j].start - 1

    total = 0
    for r in ranges:
        if r.valid():
            total += r.stop - r.start + 1
    for b in beacons:
        if b.y == 2000000:
            total -= 1

    hidden_y = 0
    y = 0
    for y in range(4000001):
        ranges = get_ranges(y, beacons)
        covered = 0
        for r in ranges:
            covered += r.stop - r.start + 1
        if covered < 4000001:
            hidden_y = y
            break
    
    hidden_x = 0
    for x in range(4000001):
        found = False
        for r in ranges:
            if x >= r.start and x <= r.stop:
                found = True
                break
        if not found:
            hidden_x = x
            break
    
    return total, hidden_x * 4000000 + hidden_y
