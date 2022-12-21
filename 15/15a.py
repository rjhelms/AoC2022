from collections import defaultdict
from time import perf_counter

IN_FILE = "15/input.txt"

ROW_TO_CHECK = 2000000


def calculate_manhattan(first: tuple, second: tuple) -> int:
    x = abs(first[0] - second[0])
    y = abs(first[1] - second[1])
    return x + y


def set_false_by_manhattan(center: tuple, distance: int, spaces: dict):
    distance = distance - (abs(center[1] - ROW_TO_CHECK))
    if distance < 0:
        return center[0], center[0]

    x_start = center[0] - distance
    x_end = center[0] + distance

    for x in range(x_start, x_end + 1):
        spaces[(x, ROW_TO_CHECK)] = False

    return x_start, x_end


if __name__ == "__main__":
    start_time = perf_counter()
    min_x = 0
    max_x = 0
    spaces = defaultdict(lambda: None)
    with open(IN_FILE) as f:
        for line in f:
            coords = [
                x.split(": closest beacon is at ")
                for x in line.strip().split("Sensor at ")
            ][-1]
            sensor = tuple([int(x) for x in coords[0].strip("x=").split(", y=")])
            beacon = tuple([int(x) for x in coords[1].strip("x=").split(", y=")])
            loc_min_x, loc_max_x = set_false_by_manhattan(
                sensor, calculate_manhattan(sensor, beacon), spaces
            )
            spaces[sensor] = False
            spaces[beacon] = True
            if loc_min_x < min_x:
                min_x = loc_min_x
            if loc_max_x > max_x:
                max_x = loc_max_x

    count = 0
    for x in range(min_x, max_x + 1):
        if spaces[(x, ROW_TO_CHECK)] == False:
            count += 1

    print(count)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
