from io import TextIOWrapper
import heapq

def main(file: TextIOWrapper):
    totals = heapq.nlargest(3, [sum(map(int, c.split())) for c in file.read().split('\n\n')])
    return totals[-1], sum(totals)
