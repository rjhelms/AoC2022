import re
from enum import IntEnum
import operator
from time import perf_counter

IN_FILE = "19/input.txt"

TOTAL_TIME = 24


class Resource(IntEnum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


def can_purchase_robot(recipe, resources, robot_idx):
    robot_cost = recipe[1][robot_idx]
    can_purchase = True
    for resource_idx, resource_cost in enumerate(robot_cost):
        if resources[resource_idx] < resource_cost:
            can_purchase = False
    return can_purchase


# depth first search
def search_purchase(
    recipe, resources, robots, max_cost, build_candidates, ticks_remaining
):
    best = 0

    this_path_build_candidates = build_candidates.copy()

    # trim the build candidates list
    for robot_idx in build_candidates:
        if robot_idx != Resource.GEODE and robots[robot_idx] >= max_cost[robot_idx]:
            this_path_build_candidates.remove(robot_idx)

    # for each item in build candidates
    for robot_idx in this_path_build_candidates:

        this_path_ticks_remaining = ticks_remaining
        this_path_resources = resources

        # tick through until have resources (if ever)
        while (
            not can_purchase_robot(recipe, this_path_resources, robot_idx)
            and this_path_ticks_remaining
        ):
            this_path_resources = tuple(map(operator.add, this_path_resources, robots))
            this_path_ticks_remaining -= 1

        # time's up, so check the score for this case
        if this_path_ticks_remaining < 1:
            # check if this is the best path
            if this_path_resources[Resource.GEODE] > best:
                best = this_path_resources[Resource.GEODE]
            break

        # otherwise do the purchase tick
        purchase_robot = [0, 0, 0, 0]
        purchase_robot[robot_idx] = 1
        this_path_robots = tuple(map(operator.add, robots, purchase_robot))
        this_path_resources = tuple(
            map(operator.sub, this_path_resources, recipe[1][robot_idx])
        )
        this_path_resources = tuple(map(operator.add, this_path_resources, robots))
        this_path_ticks_remaining -= 1

        # if there's time after the purchase, recurse
        if this_path_ticks_remaining > 0:
            result = search_purchase(
                recipe,
                this_path_resources,
                this_path_robots,
                max_cost,
                this_path_build_candidates,
                this_path_ticks_remaining,
            )
        else:
            # otherwise end here
            result = this_path_resources[Resource.GEODE]

        # check if this is the best path down this tree
        if result > best:
            best = result

    # and return best score up a level
    return best


if __name__ == "__main__":
    start_time = perf_counter()

    recipes = []
    quality = 0
    with open(IN_FILE) as f:
        for line in f:
            ints = [int(x) for x in re.findall(r"\b\d+\b", line)]

            # integers on each line:
            # 0: blueprint #
            # 1: ore cost of ore robot
            # 2: ore cost of clay robot
            # 3: ore cost of obsidian robot
            # 4: clay cost of obsidian robot
            # 5: ore cost of geode robot
            # 6: obsidian cost of geode robot

            recipe = (
                ints[0],  # blueprint ID
                (
                    (ints[1], 0, 0, 0),  # cost of ore robot
                    (ints[2], 0, 0, 0),  # cost of clay robot
                    (ints[3], ints[4], 0, 0),  # cost of obsidian robot
                    (ints[5], 0, ints[6], 0),  # cost of geode robot
                ),
            )
            recipes.append(recipe)

    for recipe in recipes:
        resources = (0, 0, 0, 0)
        robots = (1, 0, 0, 0)
        max_cost = [0, 0, 0, 0]
        for robot in Resource:
            for resource in Resource:
                if recipe[1][robot][resource] > max_cost[resource]:
                    max_cost[resource] = recipe[1][robot][resource]

        build_candidates = [i for i in Resource]
        geodes = search_purchase(
            recipe,
            resources,
            robots,
            max_cost,
            build_candidates,
            TOTAL_TIME,
        )
        print(f"{recipe[0]}: {geodes} geodes")
        quality += recipe[0] * geodes

    print(quality)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
