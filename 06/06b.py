IN_FILE = "06/input.txt"

if __name__ == "__main__":
    with open(IN_FILE) as f:
        for line in f:
            for i in range(len(line)):
                sub = line[i : i + 14]
                subset = set(sub)
                if len(subset) == 14:
                    print(i + 14)
                    break
