IN_FILE = "01/input.txt"


class Elf:
    def __init__(self):
        self.food = []

    def total_calories(self):
        calories = 0
        for item in self.food:
            calories += item
        return calories


if __name__ == "__main__":
    elves = []

    with open(IN_FILE) as f:
        elf = Elf()  # create first elf
        for line in f:
            if len(line.strip()) > 0:
                elf.food.append(int(line))
            else:
                elves.append(elf)
                elf = Elf()

    elves.append(elf)  # append last elf
    elves.sort(key=lambda x: x.total_calories(), reverse=True)

    print(elves[0].total_calories())
