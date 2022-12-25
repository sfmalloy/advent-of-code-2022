from io import TextIOWrapper


def main(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    s = 0
    fwd = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2
    }

    for n in lines:
        pow5 = 1
        num = 0
        for d in reversed(n):
            num += pow5 * fwd[d]
            pow5 *= 5
        s += num

    rev = {v:k for k,v in fwd.items()}
    snafu = ''
    while s > 0:
        mod = s % 5
        if mod > 2:
            diff = 5-mod
            s += diff
            snafu = rev[-diff] + snafu
        else:
            snafu = rev[mod] + snafu
        s //= 5

    return snafu, 'Merry Christmas :D'
