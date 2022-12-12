from io import TextIOWrapper


def main(file: TextIOWrapper):
    full = 0
    partial = 0
    for line in file.readlines():
        ranges = line.strip().split(',')
        start_a, end_a = map(int, ranges[0].split('-'))
        start_b, end_b = map(int, ranges[1].split('-'))
        if (start_a >= start_b and end_a <= end_b
                or start_b >= start_a and end_b <= end_a):
            full += 1
            partial += 1
        elif (end_a >= start_b and start_a <= end_b
                or end_b >= start_a and start_b <= end_a):
            partial += 1

    print(full)
    print(partial)
