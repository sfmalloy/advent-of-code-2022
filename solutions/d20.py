from io import TextIOWrapper
from typing import Self

class Node:
    next: Self
    prev: Self
    data: int

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f'{self.data}'

    def __repr__(self):
        return f'{self.data}'

    def slide(self, list_len: int):
        if self.data == 0:
            return
        curr = self
        if self.data > 0:
            move_amt = self.data % list_len
            for _ in range(move_amt):
                curr = curr.next
                if curr == self:
                    curr = curr.next
            # detach
            self.next.prev = self.prev
            self.prev.next = self.next

            # insert
            self.prev = curr
            self.next = curr.next
            self.next.prev = self
            self.prev.next = self
        else:
            move_amt = -(-self.data % list_len)
            for _ in range(move_amt, 0):
                curr = curr.prev
                if curr == self:
                    curr = curr.prev
            # detach
            self.next.prev = self.prev
            self.prev.next = self.next

            # insert
            self.prev = curr.prev
            self.next = curr
            self.next.prev = self
            self.prev.next = self

    def grove_coords(self):
        s = 0
        curr = self
        for _ in range(3):
            for _ in range(1000):
                curr = curr.next
            s += curr.data
        return s


def main(file: TextIOWrapper):
    lines = list(map(int, file.readlines()))
    nodes = [Node(n) for n in lines]
    big_nodes = [Node(n * 811589153) for n in lines]
    zero = None
    
    for i, n in enumerate(nodes):
        n.next = nodes[i+1 if i+1 < len(nodes) else 0]
        n.prev = nodes[i-1]
        if n.data == 0:
            zero = n

    L = len(nodes) - 1
    for n in nodes:
        n.slide(L)
    p1 = zero.grove_coords()
    
    for i, n in enumerate(big_nodes):
        n.next = big_nodes[i+1 if i+1 < len(big_nodes) else 0]
        n.prev = big_nodes[i-1]
        if n.data == 0:
            zero = n

    for i in range(10):
        for n in big_nodes:
            n.slide(L)
    p2 = zero.grove_coords()

    return p1,p2
