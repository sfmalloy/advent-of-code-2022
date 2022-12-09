import os
import requests
from argparse import ArgumentParser

def print_file(filename):
    with open(filename) as f:
        print(f.read())

def create_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)

def day_num_file(day_num):
    if int(day_num) < 10:
        return f'0{day_num}'
    return day_num

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', help='Downloads day <d> input if not already downloaded.')
    try:
        YEAR = 2022

        options = parser.parse_args()
        day_num = options.day
        filename = os.path.join('inputs', f'd{day_num_file(day_num)}.in')
        if os.path.exists(filename):
            print_file(filename)
            print(f'File {filename} exists')
        else:
            request = requests.get(f'https://adventofcode.com/{YEAR}/day/{day_num}/input', headers={'User-Agent': 'https://github.com/sfmalloy Script for downloading input by sfmalloy.dev@gmail.com'}, cookies={'session': os.environ['AOC_SESSION']})
            if not request.ok:
                print(f'Error in retrieving input: Code {request.status_code} (Try resetting your session cookie)')
                return
            create_file(filename, request.text)
            print_file(filename)
            print(f'File saved as {filename}')
    except KeyError as e:
        print(f'Missing environment variable {e}')
    except TypeError as e:
        parser.print_help()

if __name__ == '__main__':
    main()
