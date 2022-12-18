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
    is_valid: bool = True


def filter_ranges(ranges: list[Interval]):
    for i, outer in enumerate(ranges):
        for j, inner in enumerate(ranges):
            if not outer.is_valid:
                break
            elif i != j and inner.is_valid and (outer.start >= inner.start and outer.start <= inner.stop):
                outer.start = inner.stop + 1
                outer.is_valid = outer.start <= outer.stop
        for j, inner in enumerate(ranges):
            if not outer.is_valid:
                break
            elif i != j and inner.is_valid and (outer.stop >= inner.start and outer.stop <= inner.stop):
                outer.stop = inner.start - 1
                outer.is_valid = outer.start <= outer.stop


def main(file: TextIOWrapper):
    beacons: defaultdict[Point, list[Sensor]] = defaultdict(list)
    for line in file.readlines():
        tokens = line.split()
        beacon = Point(int(tokens[8][2:-1]), int(tokens[9][2:]))
        sensor_pos = Point(int(tokens[2][2:-1]), int(tokens[3][2:-1]))
        beacon_dist = abs(beacon.x - sensor_pos.x) + abs(beacon.y - sensor_pos.y)
        beacons[beacon].append(Sensor(sensor_pos, beacon_dist))

    beacon_vals = beacons.values()
    y = 2000000
    ranges: list[Interval] = []
    for sensors in beacon_vals:
        for s in sensors:
            dy = abs(y - s.pos.y)
            if dy <= s.beacon_dist:
                dx = s.beacon_dist - dy
                ranges.append(Interval(s.pos.x - dx, s.pos.x + dx))
    filter_ranges(ranges)

    total = 0
    for r in ranges:
        total += (r.stop - r.start + 1) if r.is_valid else 0
    for b in beacons:
        if b.y == y:
            total -= 1

    hidden_y = 0
    for y in range(4000001):
        ranges = []
        for sensors in beacon_vals:
            for s in sensors:
                dy = abs(y - s.pos.y)
                if dy <= s.beacon_dist:
                    dx = s.beacon_dist - dy
                    ranges.append(Interval(max(0, s.pos.x - dx), min(4000000, s.pos.x + dx)))
        filter_ranges(ranges)

        covered = 0
        for r in ranges:
            covered += (r.stop - r.start + 1) if r.is_valid else 0
        if covered < 4000001:
            hidden_y = y
            break
    
    hidden_x = 0
    for x in range(4000001):
        found = False
        for r in ranges:
            if r.is_valid:
                if x >= r.start and x <= r.stop:
                    found = True
                    break
        if not found:
            hidden_x = x
            break

    return total, hidden_x * 4000000 + hidden_y
