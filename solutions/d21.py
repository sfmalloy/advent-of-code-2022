from io import TextIOWrapper
from abc import ABC, abstractmethod
from typing import Self
from enum import Enum, auto


class Token(Enum):
    ADD = auto()
    SUB = auto()
    MUL = auto()
    DIV = auto()
    NUM = auto()


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
    humn.value = 3353687996514
    print(root.yell())

    # while not monkeys['root'].yell():
    #     monkeys['humn'].value += 1
    #     print(monkeys['root'].lhs_value, monkeys['root'].rhs_value)

    # figure out which side 'humn' is on

    # monkeys['root'].yell()
    # lhs_start = root.lhs_value
    # rhs_start = root.rhs_value
    # start = humn.value
    # humn.value -= 1
    # monkeys['root'].yell()
    # curr = humn.value
    # lhs_curr = root.lhs_value
    # rhs_curr = root.rhs_value

    # humn.value = lhs_curr // (lhs_curr - lhs_start)
    # root.yell()
    # print(root.lhs_value, root.rhs_value, humn.value)
    # print(humn.value)
    # humn.value -= 250000000000
    # root.yell()
    # print(root.lhs_value, root.rhs_value)
    # while root.lhs_value > root.rhs_value:
    #     humn.value += 1000000
    #     root.yell()
    
    # while root.lhs_value < root.rhs_value:
    #     humn.value -= 100000
    #     print(1, root.lhs_value, root.rhs_value)
    #     root.yell()

    # while root.lhs_value > root.rhs_value:
    #     humn.value += 10000
    #     print(2, root.lhs_value, root.rhs_value)
    #     root.yell()

    # while root.lhs_value < root.rhs_value:
    #     humn.value -= 1000
    #     print(3, root.lhs_value, root.rhs_value)
    #     root.yell()

    # while root.lhs_value > root.rhs_value:
    #     humn.value += 100
    #     print(4, root.lhs_value, root.rhs_value)
    #     root.yell()

    # while root.lhs_value < root.rhs_value:
    #     humn.value -= 10
    #     print(5, root.lhs_value, root.rhs_value)
    #     root.yell()

    # while root.lhs_value > root.rhs_value:
    #     humn.value += 1
    #     print(5, root.lhs_value, root.rhs_value)
    #     root.yell()
    # humn.value += 1
    print(root.lhs_value, root.rhs_value)

    # p2 = monkeys['root'].yell()

    return p1,humn.value
