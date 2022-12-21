import operator
from time import perf_counter

IN_FILE = "18/input.txt"

NEIGHBOURS = [(-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, 1), (0, 0, -1)]

if __name__ == "__main__":
    start_time = perf_counter()
    cube_set = set()

    # build a set of all cubes in input
    with open(IN_FILE) as f:
        for line in [x.strip() for x in f]:
            cube_tuple = tuple([int(x) for x in line.split(",")])
            cube_set.add(cube_tuple)

    open_faces = 0

    # for each cube in the set, check orthogonal neighbours
    # if no cube there, face is exposed
    for cube in cube_set:
        for offset in NEIGHBOURS:
            new_cube = tuple(map(operator.add, cube, offset))
            if new_cube not in cube_set:
                open_faces += 1

    print(open_faces)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
