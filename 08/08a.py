IN_FILE = "08/input.txt"


def check_direction(height, list):
    for item in list:
        if item >= height:
            return False
    return True


if __name__ == "__main__":
    grid = []
    with open(IN_FILE) as f:
        for line in f:
            row = []
            for char in line.strip():
                row.append(int(char))
            grid.append(row)

    total = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            visible = False
            # check for edges
            if (
                row == 0
                or col == 0
                or row == len(grid) - 1
                or col == len(grid[row]) - 1
            ):
                visible = True
            else:
                height = grid[row][col]

                # check left
                visible = check_direction(height, grid[row][0:col])

                # check right
                if not visible:
                    visible = check_direction(height, grid[row][col + 1 :])

                column = [row[col] for row in grid]

                # check above
                if not visible:
                    visible = check_direction(height, column[0:row])

                # check below
                if not visible:
                    visible = check_direction(height, column[row + 1 :])

            if visible:
                total += 1
    print(total)
