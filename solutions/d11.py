from io import TextIOWrapper
from dataclasses import dataclass
from collections import deque
from enum import Enum
from copy import deepcopy
from collections import defaultdict
from functools import reduce

class Op(Enum):
    ADD = 0
    MUL = 1

@dataclass
class Expr:
    lhs: str
    op: Op
    rhs: str

    def eval(self, old: int) -> int:
        l = old if self.lhs == 'old' else int(self.lhs)
        r = old if self.rhs == 'old' else int(self.rhs)
        if self.op == Op.ADD:
            return l + r
        return l * r

@dataclass
class Monkey:
    items: deque[int]
    op: Expr
    test: int
    true: int
    false: int
    num_inspected = 0

def do_round(monkeys: list[Monkey]):
    for m in monkeys:
        m.num_inspected += len(m.items)
        for _ in range(len(m.items)):
            worry = m.items.popleft()
            worry = m.op.eval(worry) // 3
            if worry % m.test == 0:
                monkeys[m.true].items.append(worry)
            else:
                monkeys[m.false].items.append(worry)

def do_hyper_round(monkeys: list[Monkey], modulo: int):
    for m in monkeys:
        m.num_inspected += len(m.items)
        for _ in range(len(m.items)):
            worry = m.items.popleft()
            worry = m.op.eval(worry) % modulo
            if worry % m.test == 0:
                monkeys[m.true].items.append(worry)
            else:
                monkeys[m.false].items.append(worry)

def main(file: TextIOWrapper):
    notes = file.read().split('\n\n')
    monkeys: list[Monkey] = []
    for m in notes:
        lines = m.split('\n')

        items = deque(map(int, lines[1].split(': ')[1].split(',')))
        
        lhs, str_op, rhs = lines[2].split('= ')[1].split()
        op = Op.ADD if str_op == '+' else Op.MUL
        expr = Expr(lhs, op, rhs)

        test = int(lines[3].split()[-1])
        true = int(lines[4].split()[-1])
        false = int(lines[5].split()[-1])

        monkeys.append(Monkey(items, expr, test, true, false))
    no_div_monkeys: list[Monkey] = deepcopy(monkeys)

    for _ in range(20):
        do_round(monkeys)
    monkeys.sort(key=lambda m:m.num_inspected)
    print(monkeys[-1].num_inspected*monkeys[-2].num_inspected)

    modulo = reduce(lambda a,b: a * b, [m.test for m in monkeys])
    for _ in range(10000):
        do_hyper_round(no_div_monkeys, modulo)
    no_div_monkeys.sort(key=lambda m:m.num_inspected)
    print(no_div_monkeys[-1].num_inspected*no_div_monkeys[-2].num_inspected)
