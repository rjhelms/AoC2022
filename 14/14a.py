from collections import defaultdict

IN_FILE = "14/input.txt"


def blank_tile():
    return False


def append_tile(tiles, max_y, current):
    tiles[current] = True
    if current[1] > max_y:
        max_y = current[1]
    return max_y


def do_drop(start, tiles, max_y):

    current = start
    while True:
        if not tiles[(current[0], current[1] + 1)]:
            # drop straight down
            current = (current[0], current[1] + 1)
        elif not tiles[(current[0] - 1, current[1] + 1)]:
            # down and to left
            current = (current[0] - 1, current[1] + 1)
        elif not tiles[(current[0] + 1, current[1] + 1)]:
            # down and to right
            current = (current[0] + 1, current[1] + 1)
        else:
            # no where to go, so stop and return True
            tiles[current] = True
            return True

        # check if we're beyond max_y - in which case we're falling forever
        if current[1] > max_y:
            return False


if __name__ == "__main__":
    # parse files
    tiles = defaultdict(blank_tile)

    max_y = 0

    with open(IN_FILE) as f:
        for line in f:
            moves = [
                tuple(int(y) for y in x.strip().split(","))
                for x in line.strip().split(" ->")
            ]
            current = moves[0]
            for move in moves[1:]:
                step = (0, 0)

                if move[0] < current[0]:
                    step = (-1, 0)
                elif move[0] > current[0]:
                    step = (1, 0)
                elif move[1] < current[1]:
                    step = (0, -1)
                elif move[1] > current[1]:
                    step = (0, 1)
                while current != move:
                    max_y = append_tile(tiles, max_y, current)
                    current = (current[0] + step[0], current[1] + step[1])

                max_y = append_tile(tiles, max_y, current)  # and get the last one

    count = 0
    while do_drop((500, 0), tiles, max_y):
        count += 1

    print(count)
