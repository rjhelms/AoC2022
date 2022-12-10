IN_FILE = "09/input.txt"


def largest_distance(pos1, pos2):
    x = abs(pos1[0] - pos2[0])
    y = abs(pos1[1] - pos2[1])
    return max(x, y)


def manhattan_distance(pos1, pos2):
    x = abs(pos1[0] - pos2[0])
    y = abs(pos1[1] - pos2[1])
    return x + y


if __name__ == "__main__":
    knots = []
    for i in range(10):  # head and 9 tails, 1-9
        knots.append([0, 0])

    set_tail_pos = set([tuple(knots[-1])])

    with open(IN_FILE) as f:
        for line in f:
            dir, dist = line.split()
            dist = int(dist)
            for _ in range(dist):
                match dir:
                    case "L":
                        knots[0][0] -= 1
                    case "R":
                        knots[0][0] += 1
                    case "U":
                        knots[0][1] -= 1
                    case "D":
                        knots[0][1] += 1

                for i in range(0, 9):
                    if (
                        largest_distance(knots[i], knots[i + 1]) >= 2
                        or manhattan_distance(knots[i], knots[i + 1]) > 2
                    ):
                        x_mag = knots[i][0] - knots[i + 1][0]
                        y_mag = knots[i][1] - knots[i + 1][1]

                        if x_mag > 0:
                            knots[i + 1][0] += 1
                        if x_mag < 0:
                            knots[i + 1][0] -= 1
                        if y_mag > 0:
                            knots[i + 1][1] += 1
                        if y_mag < 0:
                            knots[i + 1][1] -= 1

                set_tail_pos.add(tuple(knots[-1]))

    print(len(set_tail_pos))