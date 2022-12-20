from collections import defaultdict
from time import perf_counter

IN_FILE = "15/input.txt"

MAX_COORD = 4000000


class Sensor:
    def __init__(self, position: tuple, distance: int):
        self.position = position
        self.distance = distance

    def __repr__(self):
        return f"Sensor @ {self.position}: distance {self.distance}"

    def point_in_range(self, check_position: tuple) -> bool:
        check_distance = calculate_manhattan(self.position, check_position)
        if check_distance <= self.distance:
            return True
        return False


def calculate_manhattan(first: tuple, second: tuple) -> int:
    x = abs(first[0] - second[0])
    y = abs(first[1] - second[1])
    return x + y


def coord_in_range(coord: tuple):
    for axis in coord:
        if axis < 0 or axis > MAX_COORD:
            return False
    return True


def perimiter_walk(sensor: Sensor, sensor_list: list):
    walk_distance = sensor.distance + 1
    start_position = (sensor.position[0] - walk_distance, sensor.position[1])

    phase = 0
    current_position = start_position
    step = (1, 1)
    while phase < 4:
        current_position = (
            current_position[0] + step[0],
            current_position[1] + step[1],
        )
        if (
            current_position[0] == sensor.position[0]
            or current_position[1] == sensor.position[1]
        ):
            phase += 1
            if phase == 1:
                step = (1, -1)
            elif phase == 2:
                step = (-1, -1)
            elif phase == 3:
                step = (-1, 1)
        if coord_in_range(current_position):
            overlap = False
            for other_sensor in sensor_list:
                if other_sensor is sensor:
                    continue
                if other_sensor.point_in_range(current_position):
                    overlap = True
                    break
            if not overlap:
                return current_position

    return None


if __name__ == "__main__":
    start_time = perf_counter()
    sensors = []

    with open(IN_FILE) as f:
        for line in f:
            coords = [
                x.split(": closest beacon is at ")
                for x in line.strip().split("Sensor at ")
            ][-1]
            sensor_position = tuple(
                [int(x) for x in coords[0].strip("x=").split(", y=")]
            )
            beacon = tuple([int(x) for x in coords[1].strip("x=").split(", y=")])
            sensors.append(
                Sensor(sensor_position, calculate_manhattan(sensor_position, beacon))
            )

    for sensor in sensors:
        result = perimiter_walk(sensor, sensors)
        if result:
            print(result, result[0] * 4000000 + result[1])
            break

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.2f}s")
