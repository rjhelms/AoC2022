from time import perf_counter

from enum import Enum


class ProcState(Enum):
    FETCH = 1
    ADD = 2


IN_FILE = "10/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    state = ProcState.FETCH
    x_reg = 1
    cycle = 0
    running = True
    line = None
    param = None
    result = 0
    output = ""
    with open(IN_FILE) as f:
        while running == True:
            # get cycle
            if state == ProcState.FETCH:
                line = f.readline()
                if line == "":
                    running = False
                    break

            # during cycle
            cycle += 1
            disp_cycle = (cycle % 40) - 1
            if abs(disp_cycle - x_reg) <= 1:
                output += "#"
            else:
                output += " "
            if disp_cycle < 0:
                print(output)
                output = ""

            if cycle == 20 or (cycle - 20) % 40 == 0:
                result += cycle * x_reg

            # do cycle
            if state == ProcState.FETCH:
                if line.split()[0] == "addx":
                    param = int(line.split()[1])
                    state = ProcState.ADD
            else:
                x_reg += param
                state = ProcState.FETCH

    print(result)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
