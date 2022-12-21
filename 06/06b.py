from time import perf_counter

IN_FILE = "06/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        for line in f:
            for i in range(len(line)):
                sub = line[i : i + 14]
                subset = set(sub)
                if len(subset) == 14:
                    print(i + 14)
                    break

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
