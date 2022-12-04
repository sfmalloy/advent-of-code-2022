from io import TextIOWrapper
from dataclasses import dataclass
from typing import Self

@dataclass
class Interval:
    start: int
    end: int

    def full_overlap(self, other: Self) -> bool:
        return self.start >= other.start and self.end <= other.end
    def partial_overlap(self, other: Self) -> bool:
        return self.end >= other.start and self.start <= other.end

def main(file: TextIOWrapper):
    full = 0
    partial = 0
    for line in file.readlines():
        a, b = map(lambda s: Interval(*map(int, s.split('-'))), line.strip().split(','))
        if a.full_overlap(b) or b.full_overlap(a):
            full += 1
            partial += 1
        elif a.partial_overlap(b) or b.partial_overlap(a):
            partial += 1
    print(full)
    print(partial)
