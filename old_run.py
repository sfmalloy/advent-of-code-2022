import os
import sys
from timeit import default_timer as timer
from argparse import ArgumentParser
from io import StringIO

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
    d09.main
]

def day_num_file(day_num):
    if day_num < 10:
        return f'0{day_num}'
    return day_num

def run_all():
    day_num = 1
    total_time = 0
    curr_time = 0
    table = StringIO()
    print(f'╭{"─"*7}┬{"─"*14}╮', file=table)
    print(f'│ Day # │     {"Time":<9}│', file=table)
    print(f'├{"─"*7}┼{"─"*14}┤', file=table)
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    while day_num <= 25:
        curr_time = run_single(day_num)
        if curr_time > 0:
            print(f'│ {day_num_file(day_num):>5} │ {curr_time:>9.3f} ms │', file=table)
            total_time += curr_time
        day_num += 1
    print(f'├{"─"*7}┼{"─"*14}┤', file=table)
    sys.stdout = old_stdout
    print(table.getvalue(), end='')
    return total_time

def run_single(day_num, input_file=None):
    day_name = day_num_file(day_num)

    if input_file is None:
        input_file = os.path.join('inputs', f'd{day_name}.in')
    solution_file = os.path.join('solutions', f'd{day_name}.py')

    if not os.path.exists(solution_file):
        print(f'Day {day_name} solution file not found')
        return -1
    elif not os.path.exists(input_file):
        print(f'Input file {input_file} not found')
        return -1

    solution = DAYS[day_num]
    start = timer()
    with open(input_file) as f:
        solution(f)
    end = timer()

    return 1000 * (end - start)

def run_average(day_num, num_runs, input_file=None):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    s = 0
    for _ in range(num_runs):
        s += run_single(day_num, input_file)
    sys.stdout = old_stdout
    return s / num_runs

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '\
        'default uses input file from inputs directory.')
    parser.add_argument('-a', '--all', action='store_true', dest='run_all', 
        default=False, help='Run all days')
    parser.add_argument('-f', '--file', dest='file', help='Specify different input file from default')
    parser.add_argument('-n', '--numruns', dest='num_runs', help='Specify number of runs to get an average time', default=1)

    options = parser.parse_args()

    if options.run_all:
        time = run_all()
        print(f'│ Total │ {time:>9.3f} ms │')
        print(f'╰{"─"*7}┴{"─"*14}╯')
    elif options.day is not None:
        time = 0
        if options.num_runs == 1:
            time = run_single(int(options.day), options.file)
        else:
            time = run_average(int(options.day), int(options.num_runs), options.file)
            print(f'Day {options.day} | {options.num_runs} runs')
        if time > 0:
            print(f'Time: {time:.3f}ms')

if __name__ == '__main__':
    main()