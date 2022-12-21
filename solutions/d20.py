from io import TextIOWrapper
from typing import Self
from math import log2, ceil

class Node:
    next: list[Self]
    prev: list[Self]
    data: int

    def __init__(self, data):
        self.data = data
        self.next = []
        self.prev = []

    def __str__(self):
        return f'{self.data}'

    def __repr__(self):
        return f'{self.data}'
    
    def detach(self):
        for i in range(len(self.next)):
            for j in range(i, len(self.next)):
                self.next[i].prev[j] = self.next[i].prev[j].prev[0]
                self.prev[i].next[j] = self.prev[i].next[j].next[0]
        self.next = [None] * len(self.next)
        self.prev = [None] * len(self.prev)

    def slide(self, list_len: int):
        if self.data % list_len == 0:
            print(f'0 does not move')
            return

        curr = self
        # if self.data > 0:
        move_amt = self.data % list_len
        idx = 0
        while move_amt > 0:
            if move_amt & 1:
                curr = curr.next[idx]
            move_amt >>= 1
            idx += 1
        print(f'{self} moves between {curr} and {curr.next[0]} ({self.data % list_len}):')
        # else:
        #     move_amt = -self.data % list_len
        #     print(f'move_amt={move_amt}')
        #     idx = 0
        #     while move_amt > 0:
        #         if move_amt & 1:
        #             curr = curr.prev[idx]
        #         move_amt >>= 1
        #         idx += 1
        #     curr = curr.prev[0]
        #     print(f'insert {self.data} after {curr.data}')

        self.detach()
        # self.prev[0] = curr
        # self.next[0] = curr.next[0]
        # self.next[0].prev[0] = self
        # self.prev[0].next[0] = self

        before = curr
        after = curr.next[0]trying
        # TODO set the rest of the pointers o-o

        for i in range(0, len(self.next)):
            self.next[i] = before.next[i]
            self.prev[i] = after.prev[i]
        
            before.next[i] = self
            after.prev[i] = self

        # before.update_next(1)
        # after.update_prev(1)
        self.update_connections(before, after, 1)
        # for i in range(1, len(self.next)):
        #     before.next[i] = before.next[i].prev[0]
        #     after.prev[i] = after.prev[i].next[0]
        #     for j in range(i, len(self.next)):
        #         before.next[i].next[j] = before.next[i].next[j].next[0]
        #         before.next[i].next[j] = before.next[i].next[j].next[0]

        # for i in range(len(self.next)):
        #     after.prev[i] = after.prev[i]
        #     before.next[i] = before.next[i]
        
    def grove_coords(self):
        s = 0
        curr = self
        for _ in range(3):
            for _ in range(1000):
                curr = curr.next[0]
            s += curr.data
        return s

    @classmethod    
    def update_connections(cls, rhs: Self, lhs: Self, depth: int):
        for i in range(depth, len(rhs.next)):
            rhs.next[i] = rhs.next[i].next[0]
            lhs.prev[i] = lhs.prev[i].prev[0]
            cls.update_connections(rhs.next[i], lhs.prev[i], depth + 1)

    # def update_next(self, depth: int):
    #     print(' '*depth, end='')
    #     print(self)
    #     for i in range(depth, len(self.next)):
    #         self.next[i] = self.next[i].next[0]
    #         if depth % 2 != 0:
    #             self.next[i].update_next(depth + 1)
    #         else:
    #             self.next[i].update_prev(depth + 1)
    
    # def update_prev(self, depth: int):
    #     print(' '*depth, end='')
    #     print(self)
    #     for i in range(depth, len(self.prev)):
    #         self.prev[i] = self.prev[i].prev[0]
    #         if depth % 2 != 0:
    #             self.prev[i].update_prev(depth + 1)
    #         else:
    #             self.prev[i].update_next(depth + 1)


def main(file: TextIOWrapper):
    lines = list(map(int, file.readlines()))
    nodes = [Node(n) for n in lines]
    big_nodes = [Node(n * 811589153) for n in lines]
    zero = None
    bit_len = int(log2(len(nodes)))+1
    max_pow = 2**bit_len
    for i, n in enumerate(nodes):
        pow2 = 1
        while pow2 < max_pow:
            n.next.append(nodes[(i+pow2) % len(nodes)])
            n.prev.append(nodes[(i-pow2) % len(nodes)])
            pow2 *= 2
        if n.data == 0:
            zero = n

    nums = []
    nodes[0].slide(len(nodes)-1)
    for i in range(len(nodes)):
        print(nodes[i].data, nodes[i].next, nodes[i].prev)
        print()
    print(', '.join(map(str, nums)))
    print()

    # p1 = zero.grove_coords()
    p1=-1
    # curr = n
    # for _ in range(len(nodes)):
    #     print(curr, end=' ')
    #     curr = curr.prev[0]
    # print()

    # L = len(nodes) - 1
    # for n in nodes:
    #     curr = n
    #     for _ in range(len(nodes)):
    #         print(curr, end=' ')
    #         curr = curr.next[0]
    #     print()
    #     n.slide(L)
    #     curr = n
    #     for _ in range(len(nodes)):
    #         print(curr, end=' ')
    #         curr = curr.next[0]
    #     print('\n\n')
    # p1 = zero.grove_coords()
    
    # for i, n in enumerate(big_nodes):
    #     n.next = big_nodes[i+1 if i+1 < len(big_nodes) else 0]
    #     n.prev = big_nodes[i-1]
    #     if n.data == 0:
    #         zero = n

    # for i in range(10):
    #     for n in big_nodes:
    #         n.slide(L)
    # p2 = zero.grove_coords()

    return p1,-1





# from io import TextIOWrapper
# from typing import Self

# class Node:
#     next: Self
#     prev: Self
#     data: int

#     def __init__(self, data):
#         self.data = data

#     def __str__(self):
#         return f'{self.data}'

#     def __repr__(self):
#         return f'{self.data}'

#     def slide(self, list_len: int):
#         if self.data == 0:
#             return
#         curr = self
#         if self.data > 0:
#             move_amt = self.data % list_len
#             for _ in range(move_amt):
#                 curr = curr.next
#                 if curr == self:
#                     curr = curr.next
#             # detach
#             self.next.prev = self.prev
#             self.prev.next = self.next

#             # insert
#             self.prev = curr
#             self.next = curr.next
#             self.next.prev = self
#             self.prev.next = self
#             print(f'insert {self.data} after {curr.data}')
#         else:
#             move_amt = -(-self.data % list_len)
#             for _ in range(move_amt, 0):
#                 curr = curr.prev
#                 if curr == self:
#                     curr = curr.prev
#             # detach
#             self.next.prev = self.prev
#             self.prev.next = self.next

#             # insert
#             self.prev = curr.prev
#             self.next = curr
#             self.next.prev = self
#             self.prev.next = self
#             print(f'insert {self.data} after {curr.data}')

#     def grove_coords(self):
#         s = 0
#         curr = self
#         for _ in range(3):
#             for _ in range(1000):
#                 curr = curr.next
#             s += curr.data
#         return s


# def main(file: TextIOWrapper):
#     lines = list(map(int, file.readlines()))
#     nodes = [Node(n) for n in lines]
#     big_nodes = [Node(n * 811589153) for n in lines]
#     zero = None
    
#     for i, n in enumerate(nodes):
#         n.next = nodes[i+1 if i+1 < len(nodes) else 0]
#         n.prev = nodes[i-1]
#         if n.data == 0:
#             zero = n

#     L = len(nodes) - 1
#     for n in nodes:
#         n.slide(L)
#     p1 = zero.grove_coords()
    
#     for i, n in enumerate(big_nodes):
#         n.next = big_nodes[i+1 if i+1 < len(big_nodes) else 0]
#         n.prev = big_nodes[i-1]
#         if n.data == 0:
#             zero = n

#     for i in range(10):
#         for n in big_nodes:
#             n.slide(L)
#     p2 = zero.grove_coords()

#     return p1,p2

