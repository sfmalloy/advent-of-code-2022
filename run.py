import os
import sys
from timeit import default_timer as timer
from argparse import ArgumentParser
from io import StringIO

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
    ]


def day_num_file(day_num) -> str:
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'

def run_all() -> tuple[dict[int,float], list[str]]:
    day_num = 1
    times: dict[int,float] = {}

    # Hide stdout from printing to console
    old_stdout = sys.stdout
    sys.stdout = StringIO()

    while day_num <= 25:
        curr_time = run_single(day_num)
        if curr_time > 0:
            times[day_num] = curr_time
        day_num += 1
    
    # Revert stdout
    s = sys.stdout
    sys.stdout = old_stdout
    s.seek(0)
    outputs = list(filter(lambda s: 'not found' not in s, s.read().splitlines()))

    return times, outputs

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

# ASCII tables are fun...
def print_table(times: dict[int, float], outputs: list[str]):
    part1_width = max([len(outputs[i])+2 for i in range(0, len(outputs), 2)])-1
    part2_width = max([len(outputs[i])+2 for i in range(1, len(outputs), 2)])-1
    time_width = 11
    day_width = 5
    part1 = 0
    part2 = 1
    print( '╭{}┬{}┬{}┬{}╮'.format('─'*(day_width+2), '─'*(part1_width+2), '─'*(part2_width+2), '─'*(time_width+2)))

    print('│ {:^{day}} │ {:^{part1}} │ {:^{part2}} │ {:^{time}} │'
        .format('Day #', 'Part 1', 'Part 2', 'Time (ms)', 
        day=day_width, part1=part1_width, part2=part2_width, time=time_width))
    print('├{}┼{}┼{}┼{}┤'.format('─'*(day_width+2), '─'*(part1_width+2), '─'*(part2_width+2), '─'*(time_width+2)))

    for d, t in times.items():
        if '█' in outputs[part2]:
            for _ in range(2):
                print('│ {:>{day}} │ {:>{part1}} │ {:>{part2}} │ {:>{time}} │'
                    .format(' ', ' ', outputs[part2], ' ', day=day_width, part1=part1_width, part2=part2_width, time=time_width))
                part2 += 1
            print('│ {:>{day}} │ {:>{part1}} │ {:>{part2}} │ {:>{time}.3f} │'
                .format(day_num_file(d), outputs[part1], outputs[part2], t, day=day_width, part1=part1_width, part2=part2_width, time=time_width))
            part2 += 1
            for _ in range(3):
                print('│ {:>{day}} │ {:>{part1}} │ {:>{part2}} │ {:>{time}} │'
                    .format(' ', ' ', outputs[part2], ' ', day=day_width, part1=part1_width, part2=part2_width, time=time_width))
                part2 += 1
        else:
            print('│ {:>{day}} │ {:>{part1}} │ {:>{part2}} │ {:>{time}.3f} │'
                .format(day_num_file(d), outputs[part1], outputs[part2], t, day=day_width, part1=part1_width, part2=part2_width, time=time_width))
            part1 += 2
            part2 += 2
    print('├{}┴{}┴{}┼{}┤'.format('─'*(day_width+2), '─'*(part1_width+2), '─'*(part2_width+2), '─'*(time_width+2)))
    print(f'│ {"Total Time":^{day_width+part1_width+part2_width+6}} │ {sum(times.values()):>{time_width}.3f} │')
    print(f'╰{"─"*(day_width+part1_width+part2_width+8)}┴{"─"*(time_width+2)}╯')

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
        times, outputs = run_all()
        print_table(times, outputs)
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
    if sys.version_info.minor < 11:
        print('Min version Python 3.11 required')
        exit()
    main()
