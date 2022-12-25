import os
import sys
from time import perf_counter
from argparse import ArgumentParser
from dataclasses import dataclass

DAYS = []
if sys.version_info.minor >= 11:
    from solutions import *
    DAYS = [
        None,
        d01.main,
        d02.main,
        d03.main,
        d04.main,
        d05.main,
        d06.main,
        d07.main,
        d08.main,
        d09.main,
        d10.main,
        d11.main,
        d12.main,
        d13.main,
        d14.main,
        d15.main,
        d16.main,
        d17.main,
        d18.main,
        d19.main,
        d20.main,
        d21.main,
        d22.main,
        d23.main,
        d24.main,
        d25.main,
    ]

@dataclass
class Output:
    day: int = 0
    part1: str | int = -1
    part2: str | int = -1
    time: float = -1


def day_num_file(day_num) -> str:
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def run_all(num_runs=1) -> list[Output]:
    day_num = 1
    times: dict[int, float] = {}
    outputs: list[Output] = []

    while day_num <= len(DAYS)-1:
        if num_runs == 1:
            out = run_single(day_num)
        else:
            out = run_average(day_num, num_runs)
        if out.time > 0:
            times[day_num] = out.time
            outputs.append(out)
        day_num += 1
    return outputs


def run_single(day_num: int, input_file=None) -> Output:
    day_name = day_num_file(day_num)

    if input_file is None:
        input_file = os.path.join('inputs', f'd{day_name}.in')
    solution_file = os.path.join('solutions', f'd{day_name}.py')

    out = Output()

    if not os.path.exists(solution_file):
        print(f'Day {day_name} solution file not found')
        return out
    elif not os.path.exists(input_file):
        print(f'Input file {input_file} not found')
        return out

    solution = DAYS[day_num]
    start = perf_counter()
    with open(input_file) as f:
        ans = solution(f)
    end = perf_counter()

    out.part1 = ans[0]
    if len(ans) > 0:
        out.part2 = ans[1]
    out.time = 1000 * (end - start)
    out.day = day_num

    return out


def run_average(day_num, num_runs, input_file=None):
    out = run_single(day_num, input_file)
    s = out.time
    for _ in range(num_runs-1):
        s += run_single(day_num, input_file).time
    out.time = s / num_runs
    return out


def print_table(outputs: list[Output]):
    part1_lines = [str(out.part1).splitlines() for out in outputs]
    part2_lines = [str(out.part2).splitlines() for out in outputs]
    width1 = max(8, len(max(part1_lines, key=lambda l: len(l[0]))[0]))
    width2 = max(8, len(max(part2_lines, key=lambda l: len(l[0]))[0]))
    day_width = 5
    time_width = 12
    print('╭{}┬{}┬{}┬{}╮'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    print('│ {:^{day}} │ {:^{part1}} │ {:^{part2}} │ {:^{time}} │'
          .format('Day #', 'Part 1', 'Part 2', 'Time (ms)',
                  day=day_width, part1=width1, part2=width2, time=time_width))
    print('├{}┼{}┼{}┼{}┤'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    for p1, p2, out in zip(part1_lines, part2_lines, outputs):
        if len(p1) < len(p2):
            for l in range(len(p2)//2):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[len(p2)//2], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
            for l in range(1+len(p2)//2, len(p2)):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
        else:
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[0], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
    
    if len(outputs) > 1:
        print('├{}┴{}┴{}┼{}┤'.format('─'*(day_width+2), '─' *
            (width1+2), '─'*(width2+2), '─'*(time_width+2)))
        print(f'│ {"Total Time":^{day_width+width1+width2+6}} │ {sum([out.time for out in outputs]):>{time_width}.3f} │')
        print(f'╰{"─"*(day_width+width1+width2+8)}┴{"─"*(time_width+2)}╯')
    else:
        print(f'╰{"─"*(day_width+2)}┴{"─"*(width1+2)}┴{"─"*(width2+2)}┴{"─"*(time_width+2)}╯')



def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '
                        'default uses input file from inputs directory.')
    parser.add_argument('-a', '--all', action='store_true', dest='run_all',
                        default=False, help='Run all days')
    parser.add_argument('-f', '--file', dest='file',
                        help='Specify different input file from default')
    parser.add_argument('-n', '--numruns', dest='num_runs',
                        help='Specify number of runs to get an average time', default=1)
    parser.add_argument('-x', '--hide', action='store_true', dest='hide',
                        help='Replace output with a bunch of X\'s', default=False)

    options = parser.parse_args()
    options.num_runs = int(options.num_runs)
    if options.run_all:
        outputs = run_all(options.num_runs)
        if options.hide:
            for out in outputs:
                out.part1 = 'X'*min(40, len(str(out.part1)))
                out.part2 = 'X'*min(40, len(str(out.part2)))
        print_table(outputs)
    elif options.day is not None:
        time = 0
        if options.num_runs == 1:
            output = run_single(int(options.day), options.file)
            if options.hide:
                output.part1 = 'X'*len(str(output.part1))
                output.part2 = 'X'*len(str(output.part2))
            print_table([output])
        else:
            output = run_average(int(options.day), int(
                options.num_runs), options.file)
            if options.hide:
                output.part1 = 'X'*len(str(output.part1))
                output.part2 = 'X'*len(str(output.part2))
            print_table([output])
        if time > 0:
            print(f'Time: {time:.3f}ms')


if __name__ == '__main__':
    if sys.version_info.minor < 11:
        print('Min version Python 3.11 required')
        exit()
    main()
