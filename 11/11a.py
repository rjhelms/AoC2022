from time import perf_counter

IN_FILE = "11/input.txt"


def multiply(item, operand):
    return item * operand


def add(item, operand):
    return item + operand


def square(item, operand):
    return item * item


class Monkey:
    def __init__(self, text):
        self.items = [int(x) for x in text[0].strip()[16:].split(",")]
        oper = text[1].split()[-2:]
        if oper[1] == "old":
            self.operation = square
            self.operand = None
        else:
            self.operand = int(oper[1])
            if oper[0] == "*":
                self.operation = multiply
            else:
                self.operation = add
        self.test_divisble = int(text[2].split()[-1])
        self.true_target = int(text[3].split()[-1])
        self.false_target = int(text[4].split()[-1])
        self.items_handled = 0

    def do_turn(self):
        result = []
        for item in self.items:
            item = self.operation(item, self.operand)
            item = int(item / 3)
            test = item % self.test_divisble == 0
            if test:
                result.append([item, self.true_target])
            else:
                result.append([item, self.false_target])
            self.items_handled += 1

        self.items = []  # empty list after doing the turn

        return result

    def receive_item(self, item):
        self.items.append(item)


if __name__ == "__main__":
    start_time = perf_counter()

    monkeys = []
    with open(IN_FILE) as f:
        lines = f.readlines()
        for i in range(0, len(lines), 7):
            monkeys.append(Monkey(lines[i + 1 : i + 6]))

    round = 0

    while round < 20:
        round += 1
        monkey_number = 0
        for monkey in monkeys:
            result = monkey.do_turn()
            for item in result:
                monkeys[item[1]].receive_item(item[0])

    monkeys.sort(key=lambda x: x.items_handled, reverse=True)

    print(monkeys[0].items_handled * monkeys[1].items_handled)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
