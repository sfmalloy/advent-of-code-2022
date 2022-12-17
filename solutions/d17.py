from io import TextIOWrapper
from collections import defaultdict


def left(piece: list[list[int]], tower: list[list[int]], height: int) -> bool:
    for r in range(len(piece)):
        for c in range(len(piece[r])):
            if piece[r][c] and (c-1 < 0 or tower[height-r][c-1]):
                return False

    for r in piece:
        for c in range(len(r)-1):
            r[c] = r[c+1]
        r[-1] = 0

    return True


def right(piece: list[list[int]], tower: list[list[int]], height: int) -> bool:
    for r in range(len(piece)):
        for c in range(len(piece[r])):
            if piece[r][c] and (c+1 > len(piece[r])-1 or tower[height-r][c+1]):
                return False

    for r in piece:
        for c in range(len(r)-1,0,-1):
            r[c] = r[c-1]
        r[0] = 0

    return True


def test_drop(piece: list[list[int]], tower: list[list[int]], height: int) -> bool:
    for r in range(len(piece)):
        for c in range(len(piece[0])):
            if piece[r][c] and tower[height-r-1][c]:
                return False

    return True


def find_cycle(pieces: list[list[list[int]]], moves: str):
    i = 0
    move_ptr = 0
    seen = defaultdict(int)
    tower = [
        [2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    total = 0
    cycle = (0, 0)
    test = (0, 0)
    while True:
        seen[(i % 5, move_ptr % len(moves))] += 1
        if seen[(i % 5, move_ptr % len(moves))] == 2:
            total = len(tower)-1
            while 1 not in tower[total]:
                total -= 1
            cycle = (i, move_ptr)
            test = (i % 5, move_ptr % len(moves))
            break
        while tower[-3] == [0, 0, 0, 0, 0, 0, 0]:
            tower.pop()
        while len(tower) < 3 + len(pieces[i%5]) or tower[-(3+len(pieces[i % 5]))] != [0, 0, 0, 0, 0, 0, 0]:
            tower.append([0] * 7)
        height = len(tower)-1
        piece = [[c for c in r] for r in pieces[i % 5]]
        while True:
            moves[move_ptr % len(moves)](piece, tower, height)
            move_ptr += 1
            if not test_drop(piece, tower, height):
                break
            height -= 1
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                tower[height-r][c] = int(piece[r][c] or tower[height-r][c])
        i += 1
    seen[test] = 1

    test2 = (0, 0)
    while True:
        seen[(i % 5, move_ptr % len(moves))] += 1
        if seen[test] == 3:
            test2 = (i, move_ptr)
            break
        while tower[-3] == [0, 0, 0, 0, 0, 0, 0]:
            tower.pop()
        while len(tower) < 3 + len(pieces[i%5]) or tower[-(3+len(pieces[i % 5]))] != [0, 0, 0, 0, 0, 0, 0]:
            tower.append([0] * 7)
        height = len(tower)-1
        piece = [[c for c in r] for r in pieces[i % 5]]
        while True:
            moves[move_ptr % len(moves)](piece, tower, height)
            move_ptr += 1
            if not test_drop(piece, tower, height):
                break
            height -= 1
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                tower[height-r][c] = int(piece[r][c] or tower[height-r][c])
        i += 1
    
    new_total = len(tower)-1
    while 1 not in tower[new_total]:
        new_total -= 1
    return (test2[0] - cycle[0], new_total - total)


def stack(num_drops: int, pieces: list[list[list[int]]], moves: list):
    tower = [
        [2, 2, 2, 2, 2, 2, 2],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    move_ptr = 0

    for i in range(num_drops):
        while tower[-3] == [0, 0, 0, 0, 0, 0, 0]:
            tower.pop()
        while len(tower) < 3 + len(pieces[i%5]) or tower[-(3+len(pieces[i % 5]))] != [0, 0, 0, 0, 0, 0, 0]:
            tower.append([0] * 7)
        height = len(tower)-1
        piece = [[c for c in r] for r in pieces[i % 5]]
        while True:
            moves[move_ptr % len(moves)](piece, tower, height)
            move_ptr += 1
            if not test_drop(piece, tower, height):
                break
            height -= 1
        for r in range(len(piece)):
            for c in range(len(piece[0])):
                tower[height-r][c] = int(piece[r][c] or tower[height-r][c])
        i += 1

    total = len(tower)-1
    while 1 not in tower[total]:
        total -= 1
    
    return total

def main(file: TextIOWrapper):
    pieces: list[list[list[int]]] = [
        [
            [0, 0, 1, 1, 1, 1, 0]
        ],
        [
            [0, 0, 0, 1, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ],
        [
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 1, 0, 0]
        ],
        [
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0]
        ],
        [
            [0, 0, 1, 1, 0, 0, 0],
            [0, 0, 1, 1, 0, 0, 0],
        ]
    ]

    moves = [left if wind == '<' else right for wind in file.read().strip()]
    cycle_len, cycle_height = find_cycle(pieces, moves)
    big = (cycle_height * (1000000000000 // cycle_len))

    return stack(2022, pieces, moves), big + stack(1000000000000 % cycle_len, pieces, moves)
