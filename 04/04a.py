IN_FILE = "04/input.txt"

if __name__ == "__main__":
    with open(IN_FILE) as f:
        contained = 0
        for line in f:
            pair = [[int(y) for y in x.split("-")] for x in line.strip().split(",")]

            # check if first contains second
            if pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]:
                print(pair)
                contained += 1
            # check is second contains first
            elif pair[1][0] <= pair[0][0] and pair[1][1] >= pair[0][1]:
                print(pair)
                contained += 1

    print(contained)
