from time import perf_counter

IN_FILE = "08/input.txt"


def score_direction(height, list):
    count = 0
    for item in list:
        count += 1
        if item >= height:
            break
    return count


if __name__ == "__main__":
    start_time = perf_counter()

    grid = []
    with open(IN_FILE) as f:
        for line in f:
            row = []
            for char in line.strip():
                row.append(int(char))
            grid.append(row)

    max_score = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            score = 1
            # check for edges
            if (
                row == 0
                or col == 0
                or row == len(grid) - 1
                or col == len(grid[row]) - 1
            ):
                score = 0
            else:

                height = grid[row][col]
                print(row, col, height)

                # check left
                score *= score_direction(height, reversed(grid[row][0:col]))

                # check right
                score *= score_direction(height, grid[row][col + 1 :])

                column = [row[col] for row in grid]

                # check above
                score *= score_direction(height, reversed(column[0:row]))

                # check below
                score *= score_direction(height, column[row + 1 :])

            if score > max_score:
                max_score = score
    print(max_score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
