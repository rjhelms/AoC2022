IN_FILE = "03/input.txt"


def score_item(item):
    ascii = ord(item)
    if ascii <= 90:
        return ascii - 38  # ascii 65 (A) is score 27
    else:
        return ascii - 96  # ascii 97 (a) is score 1


class Elf:
    def __init__(self, line):
        tmp = line.strip()
        half = int(len(tmp) / 2)
        self.bag = [tmp[0:half], tmp[half:]]

    def common(self):
        common = set(self.bag[0]).intersection(self.bag[1])
        return list(common)


if __name__ == "__main__":
    elves = []
    with open(IN_FILE) as f:
        for line in f:
            elves.append(Elf(line))

    score = 0
    for elf in elves:
        score += score_item(elf.common()[0])

    print(score)
