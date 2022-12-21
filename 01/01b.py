from time import perf_counter

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
    start_time = perf_counter()

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

    calories = 0
    for elf in elves[:3]:
        calories += elf.total_calories()
    print(calories)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
