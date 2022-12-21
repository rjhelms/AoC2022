import math
from time import perf_counter

IN_FILE = "12/input.txt"


class Node:
    def __init__(self, position: tuple[int, int], height: int) -> None:
        self.position = position
        self.height = height
        self.neighbours = []
        self.distance = math.inf

    def find_neighbours(self, node_dict: dict) -> None:
        x_coord = self.position[0]
        y_coord = self.position[1]
        for possible_neighbour in [
            (x_coord - 1, y_coord),
            (x_coord + 1, y_coord),
            (x_coord, y_coord - 1),
            (x_coord, y_coord + 1),
        ]:
            # for 2nd puzzle, starting at end point so logic is reversed
            # not if we can get there from here - but if we could have gotten here from there
            if (
                possible_neighbour in node_dict
                and self.height <= node_dict[possible_neighbour].height + 1
            ):
                self.neighbours.append(node_dict[possible_neighbour])


if __name__ == "__main__":
    start_time = perf_counter()

    start_node = None
    end_node = None
    node_dict = {}
    with open(IN_FILE) as f:
        y_coord = 0
        for line in [x.strip() for x in f]:
            x_coord = 0
            for character in line:
                node = Node((x_coord, y_coord), ord(character) - 97)
                if character == "S":
                    node.height = 0
                    start_node = node
                elif character == "E":
                    node.height = 25
                    end_node = node
                node_dict[(x_coord, y_coord)] = node
                x_coord += 1
            y_coord += 1

    for coords in node_dict:
        node_dict[coords].find_neighbours(node_dict)

    unvisited_set = list(node_dict.values())
    end_node.distance = 0   # start at end node
    finished = False
    while not finished:
        unvisited_set.sort(key=lambda x: x.distance)
        current_node = unvisited_set[0]
        if current_node.height == 0:
            # finish at the first height-0 node reached
            finished = True
            break
        neighbour_distance = current_node.distance + 1
        for neighbour in current_node.neighbours:
            if neighbour.distance > neighbour_distance:
                neighbour.distance = neighbour_distance
        unvisited_set.remove(current_node)

    print(unvisited_set[0].distance)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
