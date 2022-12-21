from time import perf_counter

IN_FILE = "13/input.txt"


def parse(left, right) -> bool:
    print(f"Comparing {left} and {right}")

    for i in range(len(left)):
        if len(right) <= i:
            print("Ran out of right items! Out of order")
            return False
        print(f"Check {left[i]} vs {right[i]}")
        if type(left[i]) is int and type(right[i]) is int:
            if left[i] < right[i]:
                print("Left int < right int, in order")
                return True
            if left[i] > right[i]:
                print("Left int > right int, out of order")
                return False
        else:
            if type(left[i]) is int:
                print("Casting left to list")
                left[i] = [left[i]]
            if type(right[i]) is int:
                print("Casting right to list")
                right[i] = [right[i]]
            print("Checking sublist")
            result = parse(left[i], right[i])
            if result != None:
                return result

    print("Ran out of left items")
    if len(left) == len(right):
        print("keep going")
        return None
    else:
        print("in order")
        return True


if __name__ == "__main__":
    start_time = perf_counter()
    score = 0
    with open(IN_FILE) as f:
        text = f.readlines()
        value = 1
        for idx in range(0, len(text), 3):
            left = eval(text[idx])
            right = eval(text[idx + 1])
            print(value, left, right)
            if parse(left, right):
                score += value
            value += 1
            print()
    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
