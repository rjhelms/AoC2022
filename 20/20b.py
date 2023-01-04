from time import perf_counter

IN_FILE = "20/input.txt"


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def shift_left(self):
        old_left = self.left
        old_right = self.right
        self.right = old_left
        self.left = old_left.left
        old_left.left.right = self
        old_right.left = old_left
        old_left.right = old_right
        old_left.left = self

    def shift_right(self):
        old_left = self.left
        old_right = self.right
        self.left = old_right
        self.right = old_right.right
        old_right.right.left = self
        old_left.right = old_right
        old_right.left = old_left
        old_right.right = self

    def __repr__(self):
        return f"{self.value} ({self.left.value}, {self.right.value})"


if __name__ == "__main__":
    start_time = perf_counter()

    orig_list = []
    with open(IN_FILE) as f:
        for line in f:
            orig_list.append(int(line))

    zero_node = None
    linked_list = []
    for item in orig_list:
        node = Node(item * 811589153)
        if len(linked_list) > 0:
            node.left = linked_list[-1]
            linked_list[-1].right = node
        linked_list.append(node)
        if item == 0:
            zero_node = node

    linked_list[0].left = linked_list[-1]
    linked_list[-1].right = linked_list[0]

    for _ in range(10):
        print(".", end="", flush=True)
        for item in linked_list:
            shift = item.value
            shift %= len(linked_list) - 1
            while shift > 0:
                item.shift_right()
                shift -= 1
            while shift < 0:
                item.shift_left()
                shift += 1

    print()
    node = zero_node

    score = 0
    for _ in range(3):
        for _ in range(1000):
            node = node.right
        score += node.value

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
