import operator
from time import perf_counter

IN_FILE = "18/input.txt"

NEIGHBOURS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]

if __name__ == "__main__":
    start_time = perf_counter()
    min_coord = (999, 999, 999)
    max_coord = (0, 0, 0)
    cube_set = set()

    # build a set of all cubes in input
    # also get min and max coordinates
    with open(IN_FILE) as f:
        for line in [x.strip() for x in f]:
            cube_tuple = tuple([int(x) for x in line.split(",")])
            min_coord = tuple(map(min, min_coord, cube_tuple))
            max_coord = tuple(map(max, max_coord, cube_tuple))
            cube_set.add(cube_tuple)

    # convert min and max coordinates to single values
    min_coord = min(min_coord) - 1
    max_coord = max(max_coord) + 2

    # simulate steam explanding from outside
    steam = set()
    steam.add(((min_coord, min_coord, min_coord)))
    last_new_steam = steam.copy()

    # starting from one corner, simulate steam expanding
    expanding = True
    while expanding:
        new_steam = set()
        for cube in last_new_steam:
            for offset in NEIGHBOURS:
                # for each cube where steam was last iteration, check each neighbour
                new_cube = tuple(map(operator.add, cube, offset))
                min_new = max_coord
                max_new = min_coord

                # check bounds
                for val in new_cube:
                    if val < min_new:
                        min_new = val
                    elif val > max_new:
                        max_new = val

                # if in bounds, and is empty, expand steam there
                if (
                    min_new >= min_coord
                    and max_new <= max_coord
                    and new_cube not in steam
                    and new_cube not in cube_set
                ):
                    new_steam.add(new_cube)

        # keep going until an iteration with no new steam
        if len(new_steam) == 0:
            expanding = False
        else:
            last_new_steam = new_steam
            steam.update(new_steam)

    # everywhere steam didn't reach is the solid version of the droplet
    filled_set = set()
    for x in range(min_coord, max_coord):
        for y in range(min_coord, max_coord):
            for z in range(min_coord, max_coord):
                if (x, y, z) not in steam:
                    filled_set.add((x, y, z))

    # so can do count from part 1
    open_faces = 0
    for cube in filled_set:
        for offset in NEIGHBOURS:
            new_cube = tuple(map(operator.add, cube, offset))
            if new_cube not in filled_set:
                open_faces += 1

    print(open_faces)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
