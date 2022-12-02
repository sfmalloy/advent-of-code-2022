from io import TextIOWrapper

def main(file: TextIOWrapper):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    games = [l.strip().split() for l in file.readlines()]

    win = {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER
    }

    lose = {
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK
    }
    
    part1 = 0
    part2 = 0
    for a,b in games:
        me = ord(b) - ord('X') + 1
        other = ord(a) - ord('A') + 1
        if me == other:
            part1 += 3
        elif win[me] == other:
            part1 += 6
        
        if me == 1:
            part2 += win[other]
        elif me == 2:
            part2 += 3 + other
        elif me == 3:
            part2 += 6 + lose[other]
        part1 += me
    
    print(part1)
    print(part2)