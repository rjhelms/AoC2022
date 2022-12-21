from collections import defaultdict
from time import perf_counter

IN_FILE = "17/input.txt"

ROCK_COUNT = 1000000000000

BLOCKS = [
    # height, width, [list of tiles]
    [4, 1, [(0, 0), (1, 0), (2, 0), (3, 0)]],
    [3, 3, [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]],
    [3, 3, [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]],
    [1, 4, [(0, 0), (0, 1), (0, 2), (0, 3)]],
    [2, 2, [(0, 0), (0, 1), (1, 0), (1, 1)]],
]


def do_fall(well, highest, wind_pattern, wind_idx, i, old, rock_set, idx_dict):
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

    # checking for cycles
    cycle_tuple = (None, None)

    # when at block 0
    if i % len(BLOCKS) == 0:
        # if this pair of block and wind_idx have appeared before, maybe a cycle?
        if wind_idx in rock_set:
            # return the length and height of the cycle
            cycle_tuple = (i - idx_dict[wind_idx][0], highest - idx_dict[wind_idx][1])
        else:
            # otherwise add to the cycle
            rock_set.add(wind_idx)

        # update the dictionary of indexes
        idx_dict[wind_idx] = (i, highest)
        old = highest
    return wind_idx, highest, old, cycle_tuple


if __name__ == "__main__":
    start_time = perf_counter()
    rock_set = set()
    idx_dict = {}

    well = defaultdict(lambda: False)
    highest = 0
    wind_pattern = []
    with open(IN_FILE) as f:
        wind_pattern = f.readline()

    wind_idx = 0
    old = 0
    i = -1  # hacky
    cycle_found = False
    cycle_tuple = (None, None)
    cycle_tuple_set = set()

    # find a cycle
    while not cycle_found:
        i += 1
        wind_idx, highest, old, cycle_tuple = do_fall(
            well, highest, wind_pattern, wind_idx, i, old, rock_set, idx_dict
        )
        if cycle_tuple[0]:
            # check if this cycle length and height have appeared before
            # if so, this is the real cycle
            if cycle_tuple in cycle_tuple_set:
                cycle_found = True
            cycle_tuple_set.add(cycle_tuple)

    print(f"Cycle found at iteration {i}")
    print(f"Height after first cycle is {highest}")
    print(f"cycle length is {cycle_tuple[0]}, increases height by {cycle_tuple[1]}")

    remaining = ROCK_COUNT - i
    full_cycles = int(remaining / cycle_tuple[0])
    extra_iter = remaining % cycle_tuple[0]
    height_post_full = highest + (full_cycles * cycle_tuple[1])
    print(f"After {full_cycles} more cycles, height {height_post_full}")

    extra_base_height = highest
    i += 1
    end = i + extra_iter
    for extra_i in range(i, end):
        wind_idx, highest, old, cycle_tuple = do_fall(
            well, highest, wind_pattern, wind_idx, extra_i, old, rock_set, idx_dict
        )

    print(f"{extra_iter} more rocks adds {highest-extra_base_height}")
    print(f"total: {height_post_full+(highest-extra_base_height-1)}")
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.2f}s")
