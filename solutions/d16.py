from io import TextIOWrapper
from dataclasses import dataclass, field
from collections import deque
from functools import lru_cache


@dataclass(frozen=True, eq=True)
class Valve:
    name: str
    flow_rate: int
    tunnels: frozenset[str] = field(default_factory=frozenset)


@dataclass
class Node:
    valve: Valve
    time: int = 0
    seen: frozenset[str] = field(default_factory=frozenset)
    flow_rate: int = 0


@dataclass
class DoubleNode:
    me: Node
    elephant: Node
    flow_rate: int = 0


@lru_cache(maxsize=None)
def path_time(start: Valve, goal: Valve, const_tunnels: frozenset[tuple[str, frozenset[Valve]]]):
    tunnels = dict(const_tunnels)
    q = deque([(start, 0)])
    while len(q) > 0:
        curr, time = q.pop()
        if curr.name == goal.name:
            return time
        for tunnel in tunnels[curr.name]:
            q.appendleft((tunnel, time + 1))
    return 0


def get_paths(start: Node, valves: list[Valve], tunnels: frozenset[tuple[str, frozenset[Valve]]], max_time: int):
    paths: list[Node] = []
    for goal in filter(lambda v: v.name not in start.seen, valves):
        time = path_time(start.valve, goal, tunnels)
        if time > 0:
            paths.append(Node(goal, start.time + time, start.seen | {goal.name}, start.flow_rate))
    return [p for p in paths if p.time + 1 <= max_time]


def main(file: TextIOWrapper):
    valves: dict[str, Valve] = {}
    for line in file.readlines():
        tokens = line.strip().split(' ', maxsplit=9)
        name = tokens[1]
        flow_rate = int(tokens[4].split('=')[-1][:-1])
        tunnels = frozenset(tokens[-1].split(', '))
        valves[name] = Valve(name, flow_rate, tunnels)

    tunnels: frozenset[tuple[str, frozenset[Valve]]] = frozenset()
    for v in valves.values():
        v_tunnels: list[Valve] = []
        for t in v.tunnels:
            v_tunnels.append(valves[t])
        tunnels = tunnels | {(v.name, frozenset(v_tunnels))}
    
    filtered = list(filter(lambda v: v.flow_rate > 0, valves.values()))
    q = deque([Node(valves['AA'])])
    best1 = 0
    while len(q) > 0:
        curr = q.pop()
        best1 = max(best1, curr.flow_rate)
        for node in get_paths(curr, filtered, tunnels, 30):
            node.time += 1
            node.flow_rate += node.valve.flow_rate * (30 - node.time)
            if node.flow_rate > best1:
                q.appendleft(node)
    
    q = deque([DoubleNode(Node(valves['AA']), Node(valves['AA']))])
    best2 = 0
    while len(q) > 0:
        curr = q.pop()
        best2 = max(best2, curr.flow_rate)
        me = get_paths(curr.me, filtered, tunnels, 26)
        elephant = get_paths(curr.elephant, filtered, tunnels, 26)
        for p1 in me:
            p1.time += 1
            p1.flow_rate += p1.valve.flow_rate * (26 - p1.time)
        for p2 in elephant:
            p2.time += 1
            p2.flow_rate += p2.valve.flow_rate * (26 - p2.time)
        for p1 in me:
            for p2 in elephant:
                if p1.flow_rate + p2.flow_rate > best2 and p1.valve.name not in p2.seen and p2.valve.name not in p1.seen:
                    q.appendleft(DoubleNode(p1, p2, p1.flow_rate + p2.flow_rate))

    # have to do this or things go horribly wrong running multiple times
    path_time.cache_clear()

    return best1, best2
