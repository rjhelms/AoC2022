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
    head_pos = [0, 0]
    tail_pos = [0, 0]
    set_tail_pos = set([tuple(tail_pos)])

    with open(IN_FILE) as f:
        for line in f:
            dir, dist = line.split()
            dist = int(dist)
            for _ in range(dist):
                match dir:
                    case "L":
                        head_pos[0] -= 1
                    case "R":
                        head_pos[0] += 1
                    case "U":
                        head_pos[1] -= 1
                    case "D":
                        head_pos[1] += 1

                if (
                    largest_distance(head_pos, tail_pos) >= 2
                    or manhattan_distance(head_pos, tail_pos) > 2
                ):
                    x_mag = head_pos[0] - tail_pos[0]
                    y_mag = head_pos[1] - tail_pos[1]

                    if x_mag > 0:
                        tail_pos[0] += 1
                    if x_mag < 0:
                        tail_pos[0] -= 1
                    if y_mag > 0:
                        tail_pos[1] += 1
                    if y_mag < 0:
                        tail_pos[1] -= 1
                    set_tail_pos.add(tuple(tail_pos))

    print(len(set_tail_pos))
