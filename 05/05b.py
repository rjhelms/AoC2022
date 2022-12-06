from enum import Enum

IN_FILE = "05/input.txt"


class ParsingState(Enum):
    INITIAL = 1
    MOVES = 2


if __name__ == "__main__":
    state = ParsingState.INITIAL
    stack_count = 0
    stacks = []
    with open(IN_FILE) as f:
        for line in f:
            if state == ParsingState.INITIAL:

                # if on first, line determine number of stacks
                if stack_count == 0:
                    stack_count = int(len(line.strip("\n")) / 4) + 1
                    stacks = [[] for x in range(stack_count)]

                if len(line) == 1:
                    state = ParsingState.MOVES
                else:
                    for idx in range(stack_count):
                        if line[1 + idx * 4] >= "A":
                            stacks[idx].insert(0, line[1 + idx * 4])
            elif state == ParsingState.MOVES:
                stack_to = int(line.split("to")[1]) - 1
                stack_from = int(line.split("to")[0].split("from")[1]) - 1
                move_count = int(line.split("to")[0].split("from")[0].split("move")[1])
                move_list = stacks[stack_from][-move_count:]
                stacks[stack_to] += move_list
                stacks[stack_from] = stacks[stack_from][:-move_count]

    answer = ""
    for stack in stacks:
        answer += stack[-1]
    print(answer)
