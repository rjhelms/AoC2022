from time import perf_counter
IN_FILE = "04/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        overlap = 0
        for line in f:
            pair = [[int(y) for y in x.split("-")] for x in line.strip().split(",")]
            s1 = {x for x in range(pair[0][0], pair[0][1] + 1)}
            s2 = {x for x in range(pair[1][0], pair[1][1] + 1)}
            if len(s1.intersection(s2)) > 0:
                overlap += 1

    print(overlap)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
