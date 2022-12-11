from io import TextIOWrapper

import heapq
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
from functools import reduce

class Op(Enum):
    ADD = 0
    MUL = 1

class Expr:
    op: Op
    rhs: int

    def __init__(self, op: Op, rhs: str):
        self.op = op
        self.rhs = -1 if rhs == 'old' else int(rhs)

    def eval(self, old: int) -> int:
        r = old if self.rhs < 0 else self.rhs
        return old + r if self.op == Op.ADD else old * r

@dataclass
class Monkey:
    items: list[int]
    op: Expr
    test: int
    true: int
    false: int
    num_inspected: int = 0

def do_div_round(monkeys: list[Monkey]):
    for m in monkeys:
        m.num_inspected += len(m.items)
        for i in m.items:
            worry = m.op.eval(i) // 3
            if worry % m.test == 0:
                monkeys[m.true].items.append(worry)
            else:
                monkeys[m.false].items.append(worry)
        m.items.clear()

def do_mod_round(monkeys: list[Monkey], modulo: int):
    for m in monkeys:
        m.num_inspected += len(m.items)
        for i in m.items:
            worry = m.op.eval(i) % modulo
            if worry % m.test == 0:
                monkeys[m.true].items.append(worry)
            else:
                monkeys[m.false].items.append(worry)
        m.items.clear()

def main(file: TextIOWrapper):
    notes = file.read().split('\n\n')
    div_monkeys: list[Monkey] = []
    for m in notes:
        lines = m.split('\n')

        items = list(map(int, lines[1].split(': ')[1].split(',')))
        
        _, str_op, rhs = lines[2].split('= ')[1].split()
        op = Op.ADD if str_op == '+' else Op.MUL
        expr = Expr(op, rhs)

        test = int(lines[3].split()[-1])
        true = int(lines[4].split()[-1])
        false = int(lines[5].split()[-1])

        div_monkeys.append(Monkey(items, expr, test, true, false))
    mod_monkeys: list[Monkey] = deepcopy(div_monkeys)

    for _ in range(20):
        do_div_round(div_monkeys)
    largest = heapq.nlargest(2, div_monkeys, key=lambda m: m.num_inspected)
    print(largest[0].num_inspected * largest[1].num_inspected)

    modulo = reduce(lambda a,b: a * b, [m.test for m in mod_monkeys])
    for _ in range(10000):
        do_mod_round(mod_monkeys, modulo)
    largest = heapq.nlargest(2, mod_monkeys, key=lambda m: m.num_inspected)
    print(largest[0].num_inspected * largest[1].num_inspected)
