from io import TextIOWrapper

def main(file: TextIOWrapper):
    cals = file.read().split('\n\n')
    m = 0
    totals = []
    for c in cals:
        s = sum(map(int,c.split()))
        m = max(s, m)
        totals.append(s)
    print(m)
    print(sum(sorted(totals)[-3:]))
