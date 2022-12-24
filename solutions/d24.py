from io import TextIOWrapper
from dataclasses import dataclass, field
from collections import defaultdict, deque
from typing import Self
from math import lcm


@dataclass(frozen=True, eq=True)
class Vec2:
    r: int
    c: int

    def __add__(self, other: Self) -> Self:
        return Vec2(self.r+other.r, self.c+other.c)

    def __mul__(self, scale: int) -> Self:
        if not isinstance(scale, int):
            return NotImplemented
        return Vec2(scale*self.r, scale*self.c)

    def mdist(self, other: Self) -> Self:
        return abs(self.r-other.r) + abs(self.c-other.c)


@dataclass(frozen=True, eq=True)
class State:
    me: Vec2=field(compare=True,hash=True)
    blizzard_state: int=field(default=0,compare=False,hash=True)
    steps: int=field(default=0,compare=True,hash=True)


DOWN = Vec2(1, 0)
RIGHT = Vec2(0, 1)
LEFT = Vec2(0, -1)
UP = Vec2(-1, 0)


def go(init: State, goal: Vec2, blizzard_states: list[dict[Vec2, set[Vec2]]], walls: set[Vec2], height: int):
    q: deque[State] = deque()
    q.append(init)
    seen = set()
    
    while True:
        curr: State = q.popleft()
        while curr in seen:
            curr = q.popleft()
        seen.add(curr)
        if curr.me == goal:
            return curr

        u = curr.me + UP
        d = curr.me + DOWN
        l = curr.me + LEFT
        r = curr.me + RIGHT
        next_blizzard = (curr.blizzard_state+1) % len(blizzard_states)
        if r not in blizzard_states[next_blizzard] and r not in walls:
            s = State(r, next_blizzard, curr.steps+1)
            if s not in seen:
                q.append(s)
        if d.r <= height+1 and d not in blizzard_states[next_blizzard] and d not in walls:
            s = State(d, next_blizzard, curr.steps+1)
            if s not in seen:
                q.append(s)
        if l not in blizzard_states[next_blizzard] and l not in walls:
            s = State(l, next_blizzard, curr.steps+1)
            if s not in seen:
                q.append(s)
        if u.r >= 0 and u not in blizzard_states[next_blizzard] and u not in walls:
            s = State(u, next_blizzard, curr.steps+1)
            if s not in seen:
                q.append(s)
        if curr.me not in blizzard_states[next_blizzard]:
            s = State(curr.me, next_blizzard, curr.steps+1)
            if s not in seen:
                q.append(s)

def main(file: TextIOWrapper):
    bvel = {
        'v': Vec2(1, 0),
        '>': Vec2(0, 1),
        '<': Vec2(0, -1),
        '^': Vec2(-1, 0)
    }

    # different moves
    lines = [line.strip() for line in file.readlines()]
    height = len(lines)-2
    width = len(lines[0])-2

    goal = Vec2(0, 1)
    blizzards = defaultdict(set)
    walls = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '#':
                walls.add(Vec2(row, col))
            elif char != '.':
                blizzards[Vec2(row, col)].add(bvel[char])
            else:
                goal = Vec2(row, col)

    blizzard_states = []
    upper_bound = lcm(width, height)
    while len(blizzard_states) < upper_bound:
        blizzard_states.append({k:v for k,v in blizzards.items()})
        new_blizzards = defaultdict(set)
        for pos, bset in blizzards.items():
            for b in bset:
                if pos+b not in walls:
                    new_blizzards[pos+b].add(b)
                elif b == DOWN:
                    new_blizzards[Vec2(1, pos.c)].add(b)
                elif b == UP:
                    new_blizzards[Vec2(height, pos.c)].add(b)
                elif b == LEFT:
                    new_blizzards[Vec2(pos.r, width)].add(b)
                elif b == RIGHT:
                    new_blizzards[Vec2(pos.r, 1)].add(b)
        blizzards = new_blizzards

    start = Vec2(0, 1)
    end = goal
    curr = go(State(start), end, blizzard_states, walls, height)
    p1 = curr.steps
    back = go(curr, Vec2(0, 1), blizzard_states, walls, height)
    end_again = go(back, end, blizzard_states, walls, height)
    p2 = end_again.steps

    return p1,p2
