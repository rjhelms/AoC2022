IN_FILE = "03/input.txt"


def score_item(item):
    ascii = ord(item)
    if ascii <= 90:
        return ascii - 38  # ascii 65 (A) is score 27
    else:
        return ascii - 96  # ascii 97 (a) is score 1


def common_to_elves(elf_list):
    s = {}
    for elf in elf_list:
        if len(s) == 0:
            s = set(elf.bag)
        else:
            s = s.intersection(elf.bag)
    return list(s)


class Elf:
    def __init__(self, line):
        self.bag = line.strip()


if __name__ == "__main__":
    elves = []
    with open(IN_FILE) as f:
        for line in f:
            elves.append(Elf(line))

    score = 0
    i = 0
    while i < len(elves):
        score += score_item(common_to_elves(elves[i : i + 3])[0])
        i += 3

    print(score)
