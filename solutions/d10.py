from io import TextIOWrapper

def main(file: TextIOWrapper):
    clock = 0
    prog = [line.strip().split() for line in file.readlines()]
    ip = 0
    free = 0
    strength = 0
    curr_op = 0
    x = 1
    check = 20
    crt = [False for _ in range(240)]
    while ip < len(prog):
        if clock == check:
            strength += x * clock
            check += 40
        if clock >= free:
            x += curr_op
            match prog[ip]:
                case ['noop']:
                    curr_op = 0
                    free += 1
                case ['addx', a]:
                    curr_op = int(a)
                    free += 2
            ip += 1
        hpos = clock % 40
        crt[clock] = x-1 == hpos or x == hpos or x+1 == hpos
        clock += 1

    s = ''
    for i,r in enumerate(crt):
        if i > 0 and i % 40 == 0:
            s += '\n'
        s += '█' if r else ' '
    print(strength)
    print(s)
