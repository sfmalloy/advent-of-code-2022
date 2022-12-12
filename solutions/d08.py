from io import TextIOWrapper


def visible_outside(grid: list[list[int]]):
    max_up = [grid[0][c] for c in range(len(grid[0]))]
    max_down = [grid[-1][c] for c in range(len(grid[-1]))]
    max_left = [grid[r][0] for r in range(len(grid))]
    max_right = [grid[r][-1] for r in range(len(grid))]
    len_r = len(grid)-1
    len_c = len(grid[0])-1
    seen = set()

    for r in range(1, len_r):
        for c in range(1, len_c):
            if grid[r][c] > max_up[c]:
                seen.add((r, c))
                max_up[c] = grid[r][c]
            if grid[r][c] > max_left[r]:
                seen.add((r, c))
                max_left[r] = grid[r][c]

    for r in range(len_r-1, 0, -1):
        for c in range(len_c-1, 0, -1):
            if grid[r][c] > max_right[r]:
                seen.add((r, c))
                max_right[r] = grid[r][c]
            if grid[r][c] > max_down[c]:
                seen.add((r, c))
                max_down[c] = grid[r][c]

    return 2 * (len(grid[0])+len(grid)-2) + len(seen)


def visible_inside(grid: list[list[int]]):
    best = 0
    done = set()
    stack = [
        (1, 1),
        (len(grid)-2, 1),
        (1, len(grid[0])-2),
        (len(grid)-2, len(grid[0])-2)
    ]
    len_r = len(grid)-1
    len_c = len(grid[0])-1
    while len(stack) > 0:
        r, c = stack.pop()
        if (r, c) in done:
            continue
        done.add((r, c))
        r_up = r - 1
        while r_up > 0 and grid[r_up][c] < grid[r][c]:
            r_up -= 1
        if r_up > 0:
            stack.append((r_up, c))

        r_down = r + 1
        while r_down < len_r and grid[r_down][c] < grid[r][c]:
            r_down += 1
        if r_down < len_r:
            stack.append((r_down, c))

        c_left = c - 1
        while c_left > 0 and grid[r][c_left] < grid[r][c]:
            c_left -= 1
        if c_left > 0:
            stack.append((r, c_left))

        c_right = c + 1
        while c_right < len_c and grid[r][c_right] < grid[r][c]:
            c_right += 1
        if c_right < len_c:
            stack.append((r, c_right))

        best = max(best, (r-r_up) * (r_down-r) * (c-c_left) * (c_right-c))
    return best


def main(file: TextIOWrapper):
    grid = [list(map(int, list(row.strip()))) for row in file.readlines()]
    print(visible_outside(grid))
    print(visible_inside(grid))
