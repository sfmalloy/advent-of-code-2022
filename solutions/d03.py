from io import TextIOWrapper

def priority(c):
    return ord(c) - ((ord('a') - 1) if c.islower() else (ord('A') - 27))

def main(file: TextIOWrapper):
    rucksacks = [line.strip() for line in file.readlines()]
    s1 = 0
    s2 = 0
    for i in range(0, len(rucksacks), 3):
        groups = rucksacks[i:i+3]
        for g in groups:
            begin = g[:len(g)//2]
            end = g[len(g)//2:]
            s1 += priority((set(begin) & set(end)).pop())
        s2 += priority((set(groups[0]) & set(groups[1]) & set(groups[2])).pop())
    print(s1)
    print(s2)
