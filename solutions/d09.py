from io import TextIOWrapper
from dataclasses import dataclass

@dataclass
class Move:
    dir: str
    dist: int

@dataclass
class Knot:
    x: int = 0
    y: int = 0

    def pos(self) -> tuple[int, int]:
        return (self.x, self.y)

def init_head(head: Knot, dirs: list[Move]) -> list[tuple[int, int]]:
    path = []
    for d in dirs:
        match d.dir:
            case 'R':
                for _ in range(d.dist):
                    head.x += 1
                    path.append(head.pos())
            case 'L':
                for _ in range(d.dist):
                    head.x -= 1
                    path.append(head.pos())
            case 'U':
                for _ in range(d.dist):
                    head.y += 1
                    path.append(head.pos())
            case 'D':
                for _ in range(d.dist):
                    head.y -= 1
                    path.append(head.pos())
    return path

def simulate(num_knots: int, dirs: list[Move]) -> int:
    head = init_head(Knot(), dirs)
    tail: list[tuple[int, int]] = []
    for _ in range(num_knots-1):
        tail = []
        curr = Knot()
        for x,y in head:
            if x - curr.x > 1:
                curr.x += 1
                curr.y += 1 if y > curr.y else (-1 if y < curr.y else 0)
            elif curr.x - x > 1:
                curr.x -= 1
                curr.y += 1 if y > curr.y else (-1 if y < curr.y else 0)
            elif y - curr.y > 1:
                curr.y += 1
                curr.x += 1 if x > curr.x else (-1 if x < curr.x else 0)
            elif curr.y - y > 1:
                curr.y -= 1
                curr.x += 1 if x > curr.x else (-1 if x < curr.x else 0)
            tail.append(curr.pos())
        head = tail

    return len(set(tail))

def main(file: TextIOWrapper):
    dirs = [(lambda d: Move(d[0], int(d[1])))(l.strip().split()) for l in file.readlines()]
    short = simulate(2, dirs)
    long = simulate(10, dirs)
    print(short)
    print(long)
