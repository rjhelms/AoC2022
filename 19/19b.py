import re
from enum import IntEnum
import operator
from time import perf_counter
from math import ceil

IN_FILE = "19/input.txt"

TOTAL_TIME = 32


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
    best = resources[Resource.GEODE]

    this_path_build_candidates = build_candidates.copy()

    # trim the build candidates list
    for robot_idx in build_candidates:
        if robot_idx != Resource.GEODE:
            # got this check from Reddit:
            # if resources on hand + will be produced are greater than the highest
            # amount possibly needed in the remaining time, remove from build list
            if (robots[robot_idx] * ticks_remaining) + resources[robot_idx] >= (
                ticks_remaining * max_cost[robot_idx]
            ):
                this_path_build_candidates.remove(robot_idx)

    # for each item in build candidates
    for robot_idx in this_path_build_candidates:
        result = 0
        this_path_ticks_remaining = ticks_remaining
        this_path_resources = resources

        # trying to be clever and not iterate all the steps
        # I think 4 floating point divisions might be slower than iterating <32 times

        # calculate time 'til able to build this robot
        ticks_in_step = this_path_ticks_remaining
        resources_needed = tuple(
            map(operator.sub, recipe[1][robot_idx], this_path_resources)
        )
        ticks_needed = [0, 0, 0, 0]
        for idx, resource in enumerate(resources_needed):
            if resource <= 0:  # don't need this resource
                continue
            if robots[idx] == 0:  # no robots producing needed resource
                ticks_needed[idx] = this_path_ticks_remaining
                continue
            ticks_needed[idx] = ceil(resource / robots[idx])

        ticks_in_step = max(ticks_needed)

        ticks_in_step += 1  # plus the tick to build the thing

        # is it possible to build this thing?
        if ticks_in_step < this_path_ticks_remaining:
            # if so, get the resources from these ticks
            new_resources = tuple([x * ticks_in_step for x in robots])
            this_path_resources = tuple(
                map(operator.add, this_path_resources, new_resources)
            )
            # purchase the robot
            purchase_robot = [0, 0, 0, 0]
            purchase_robot[robot_idx] = 1
            this_path_robots = tuple(map(operator.add, robots, purchase_robot))
            this_path_resources = tuple(
                map(operator.sub, this_path_resources, recipe[1][robot_idx])
            )
            # and recurse
            this_path_ticks_remaining -= ticks_in_step
            result = search_purchase(
                recipe,
                this_path_resources,
                this_path_robots,
                max_cost,
                this_path_build_candidates,
                this_path_ticks_remaining,
            )
        else:
            # if can't built, just sit for remaining ticks
            new_resources = tuple([x * this_path_ticks_remaining for x in robots])
            this_path_resources = tuple(
                map(operator.add, this_path_resources, new_resources)
            )
            result = this_path_resources[Resource.GEODE]

        # check if this is the best path down this tree
        if result > best:
            best = result

    # and return best score up a level
    return best


if __name__ == "__main__":
    start_time = perf_counter()

    recipes = []
    quality = 1
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

    # only need to check the first 3 blueprints in part b
    for recipe in recipes[:3]:
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
        quality *= geodes

    print(quality)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
