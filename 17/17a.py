from collections import defaultdict
from time import perf_counter

IN_FILE = "17/input.txt"


BLOCKS = [
    # height, width, [list of tiles]
    [4, 1, [(0, 0), (1, 0), (2, 0), (3, 0)]],
    [3, 3, [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]],
    [3, 3, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]],
    [1, 4, [(0, 0), (0, 1), (0, 2), (0, 3)]],
    [2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]],
]


def do_fall(well, highest, wind_pattern, wind_idx, i):
    x = 2
    y = highest + 3
    block = BLOCKS[i % len(BLOCKS)]
    falling = True

    while falling:
        # get the current wind
        wind = wind_pattern[wind_idx]
        if wind == ">" and x + block[0] < 7:
            new_x = x + 1
        elif wind == "<" and x > 0:
            new_x = x - 1
        else:
            new_x = x

            # increment wind_idx
        wind_idx = (wind_idx + 1) % len(wind_pattern)

        # check if wind move can happen
        for tile in block[2]:
            if well[(tile[0] + new_x, tile[1] + y)]:
                new_x = x
                break

            # apply wind move, and check fall
        x = new_x
        new_y = y - 1

        # check if we're at the bottom
        if new_y < 0:
            falling = False
            break

            # check if any of the tiles are occupied
        for tile in block[2]:
            if well[(tile[0] + x, tile[1] + new_y)]:
                falling = False
                break
        if not falling:
            break

            # if neither, do the move and keep iterating
        y = new_y

    top = y + block[1]
    if top > highest:
        highest = top
    for tile in block[2]:
        well[(tile[0] + x, tile[1] + y)] = True

    return wind_idx, highest


if __name__ == "__main__":
    start_time = perf_counter()

    well = defaultdict(lambda: False)
    highest = 0
    wind_pattern = []
    with open(IN_FILE) as f:
        wind_pattern = f.readline()

    wind_idx = 0
    cycles = 2022
    for i in range(cycles):
        wind_idx, highest = do_fall(well, highest, wind_pattern, wind_idx, i)

    print(highest)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
