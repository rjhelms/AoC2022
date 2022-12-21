import math
import itertools
from time import perf_counter

IN_FILE = "16/input.txt"

TOTAL_TIME = 30

class Node:
    def __init__(self, name: str, rate: int, neighbours: list):
        self.name = name
        self.rate = rate
        self.neighbours = neighbours
        self.routes = {}
        self.eval_distance = math.inf

    def __repr__(self):
        return f"Valve {self.name}; rate={self.rate}; neighbours {self.neighbours}"


def evaluate_route(all_nodes, start_node_name, end_note_name):
    # Dijkstra's algorithm from day 12
    for node in list(all_nodes.values()):
        node.eval_distance = math.inf
    start_node = all_nodes[start_node_name]
    start_node.eval_distance = 0
    end_node = all_nodes[end_note_name]
    unvisited_set = list(all_nodes.values())
    finished = False

    while not finished:
        unvisited_set.sort(key=lambda x: x.eval_distance)
        current_node = unvisited_set[0]
        if current_node == end_node:
            finished = True
            break
        neighbour_distance = current_node.eval_distance + 1
        for neighbour in current_node.neighbours:
            neighbour_node = all_nodes[neighbour]
            if neighbour_node.eval_distance > current_node.eval_distance:
                neighbour_node.eval_distance = neighbour_distance
        unvisited_set.remove(current_node)
    start_node.routes[end_node.name] = end_node.eval_distance


def walk_path(all_nodes, pump_nodes, start_node, time, flow, total_flow):
    best_flow = total_flow

    # try each possible next step
    for target in pump_nodes:
        new_flow = flow
        new_total_flow = total_flow
        new_time = time
        target_time = all_nodes[start_node].routes[target] + 1

        # check if there's time to go to that node
        if new_time + target_time <= TOTAL_TIME:
            # if so, calculate new flows
            new_time += target_time
            new_total_flow += new_flow * target_time
            new_flow += all_nodes[target].rate
            # and recurse
            new_pump_nodes = pump_nodes.copy()
            new_pump_nodes.pop(target)
            new_total_flow = walk_path(
                all_nodes,
                new_pump_nodes,
                target,
                new_time,
                new_flow,
                new_total_flow,
            )

        # is this the new best route?
        if new_total_flow > best_flow:
            best_flow = new_total_flow

    # check the do-nothing case too:
    # no nodes left to visit, or no time to visit any of them
    remaining = TOTAL_TIME - time
    total_flow += remaining * flow
    if total_flow > best_flow:
        best_flow = total_flow

    # return the flow of the best route - which will propagate up recursion levels
    return best_flow


if __name__ == "__main__":
    start_time = perf_counter()

    all_nodes = {}
    pump_nodes = {}

    # parse input file
    with open(IN_FILE) as f:
        for line in f:
            line = line.strip()
            name = line[6:8]
            line = line.split("; ")
            rate = int(line[0].split("=")[-1])
            neighbours = [x[-2:] for x in line[1].split(", ")]
            all_nodes[name] = Node(name, rate, neighbours)

    # build list of pump nodes
    for node_name in all_nodes:
        if all_nodes[node_name].rate > 0:
            pump_nodes[node_name] = all_nodes[node_name]

    # calculate distance from start to each pump node
    start_node = "AA"
    for target_node in pump_nodes:
        evaluate_route(all_nodes, start_node, target_node)

    # calculate distance from each pump node to each other pump node
    # this could be optimized - each pair gets evaluated twice
    for node in pump_nodes:
        for other_node in pump_nodes:
            if node is not other_node:
                evaluate_route(all_nodes, node, other_node)

    print(walk_path(all_nodes, pump_nodes, "AA", 0, 0, 0))

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.2f}s")
