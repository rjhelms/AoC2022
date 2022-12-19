IN_FILE = "13/input.txt"


def compare(left, right) -> bool:
    for i in range(len(left)):
        if len(right) <= i:
            return False
        if type(left[i]) is int and type(right[i]) is int:
            if left[i] < right[i]:
                return True
            if left[i] > right[i]:
                return False
        else:
            compare_l = left[i]
            compare_r = right[i]
            if type(compare_l) is int:
                compare_l = [left[i]]
            if type(compare_r) is int:
                compare_r = [right[i]]
            result = compare(compare_l, compare_r)
            if result != None:
                return result

    if len(left) == len(right):
        return None
    else:
        return True


def partition(array, low, high):
    pivot = array[high]

    i = low - 1
    for j in range(low, high):
        if compare(array[j], pivot):
            i += 1
            array[i], array[j] = array[j], array[i]
    array[i + 1], array[high] = array[high], array[i + 1]
    return i + 1


def quicksort(array, low, high):
    if low < high:
        pi = partition(array, low, high)
        quicksort(array, low, pi - 1)
        quicksort(array, pi + 1, high)


if __name__ == "__main__":
    rows = []
    with open(IN_FILE) as f:
        text = f.readlines()
        for line in text:
            if len(line.strip()) > 0:
                rows.append(eval(line))
    rows.append([[2]])
    rows.append([[6]])
    quicksort(rows, 0, len(rows) - 1)
    print((rows.index([[2]]) + 1) * (rows.index([[6]]) + 1))
