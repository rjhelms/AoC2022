IN_FILE = "04/input.txt"

if __name__ == "__main__":
    with open(IN_FILE) as f:
        overlap = 0
        for line in f:
            pair = [[int(y) for y in x.split("-")] for x in line.strip().split(",")]
            s1 = {x for x in range(pair[0][0], pair[0][1] + 1)}
            s2 = {x for x in range(pair[1][0], pair[1][1] + 1)}
            if len(s1.intersection(s2)) > 0:
                overlap += 1

    print(overlap)
