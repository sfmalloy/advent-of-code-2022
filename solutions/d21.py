from io import TextIOWrapper
from abc import ABC, abstractmethod
from typing import Self


class Monkey(ABC):
    lhs: Self
    rhs: Self
    lhs_name: str
    rhs_name: str

    def __init__(self, lhs_name: str='', rhs_name: str=''):
        self.lhs = None
        self.rhs = None
        self.lhs_name = lhs_name
        self.rhs_name = rhs_name
    
    @abstractmethod
    def yell(self) -> int:
        pass

class NumMonkey(Monkey):
    value: int

    def __init__(self, val: int):
        super().__init__()
        self.value = val

    def yell(self) -> int:
        return self.value

class MulMonkey(Monkey):
    
    def __init__(self, lhs_name: str, rhs_name: str):
        super().__init__(lhs_name, rhs_name)
    
    def yell(self) -> int:
        return self.lhs.yell() * self.rhs.yell()

class DivMonkey(Monkey):
    
    def __init__(self, lhs_name: str, rhs_name: str):
        super().__init__(lhs_name, rhs_name)
    
    def yell(self) -> int:
        return self.lhs.yell() // self.rhs.yell()

class AddMonkey(Monkey):
    
    def __init__(self, lhs_name: str, rhs_name: str):
        super().__init__(lhs_name, rhs_name)
    
    def yell(self) -> int:
        return self.lhs.yell() + self.rhs.yell()

class SubMonkey(Monkey):
    
    def __init__(self, lhs_name: str, rhs_name: str):
        super().__init__(lhs_name, rhs_name)
    
    def yell(self) -> int:
        return self.lhs.yell() - self.rhs.yell()

class TestMonkey(Monkey):
    lhs_value: int
    rhs_value: int

    def __init__(self, lhs_name: str = '', rhs_name: str = ''):
        super().__init__(lhs_name, rhs_name)
        self.lhs_value = 0
        self.rhs_value = 0
    
    def yell(self) -> int:
        self.lhs_value = self.lhs.yell()
        self.rhs_value = self.rhs.yell()
        return int(self.lhs_value == self.rhs_value)

def main(file: TextIOWrapper):
    monkeys: dict[str, Monkey] = {}

    for line in file.readlines():
        tokens = line.strip().split(' ')
        name = tokens[0][:-1]
        match tokens[1:]:
            case [num]:
                monkeys[name] = NumMonkey(int(num))
            case [lhs, '+', rhs]:
                monkeys[name] = AddMonkey(lhs, rhs)
            case [lhs, '-', rhs]:
                monkeys[name] = SubMonkey(lhs, rhs)
            case [lhs, '*', rhs]:
                monkeys[name] = MulMonkey(lhs, rhs)
            case [lhs, '/', rhs]:
                monkeys[name] = DivMonkey(lhs, rhs)
    
    for monkey in monkeys.values():
        if not isinstance(monkey, NumMonkey):
            monkey.lhs = monkeys[monkey.lhs_name]
            monkey.rhs = monkeys[monkey.rhs_name]
    
    p1 = monkeys['root'].yell()

    old_root = monkeys['root']
    monkeys['root'] = TestMonkey()
    root = monkeys['root']
    humn: NumMonkey = monkeys['humn']
    root.lhs = old_root.lhs
    root.rhs = old_root.rhs
    root.yell()
    original_lhs = root.lhs_value
    original_rhs = root.rhs_value

    root.yell()
    magnitude = 10**len(str(root.rhs_value))
    humn.value += magnitude
    humn_is_lhs = original_lhs != root.lhs_value
    greater = False
    if (humn_is_lhs and original_lhs > root.lhs_value) or (not humn_is_lhs and original_rhs > root.rhs_value):
        magnitude *= -1
        greater = True
    
    while not root.yell():
        if greater and ((humn_is_lhs and root.lhs_value < root.rhs_value) or (not humn_is_lhs and root.rhs_value < root.lhs_value)):
            magnitude //= 10
            magnitude *= -1
            greater = False
        elif not greater and ((humn_is_lhs and root.lhs_value > root.rhs_value) or (not humn_is_lhs and root.rhs_value > root.lhs_value)):
            magnitude //= 10
            magnitude *= -1
            greater = True
        humn.value += magnitude
    
    while root.yell():
        humn.value += magnitude
    humn.value -= magnitude

    return p1,humn.value
