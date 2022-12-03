from io import TextIOWrapper

def main(file: TextIOWrapper):
    rucksacks = [line.strip() for line in file.readlines()]
    s1 = 0
    s2 = 0
    for i in range(0, len(rucksacks), 3):
        groups = rucksacks[i:i+3]
        for g in groups:
            begin = g[:len(g)//2]
            end = g[len(g)//2:]
            same = (set(begin) & set(end)).pop()
            if same.islower():
                s1 += ord(same) - ord('a') + 1
            else:
                s1 += ord(same) - ord('A') + 27
        same = (set(groups[0]) & set(groups[1]) & set(groups[2])).pop()
        if same.islower():
            s2 += ord(same) - ord('a') + 1
        else:
            s2 += ord(same) - ord('A') + 27
    print(s1)
    print(s2)
