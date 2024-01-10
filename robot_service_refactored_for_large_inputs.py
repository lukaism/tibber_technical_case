from typing import Dict, Tuple, Union
import time
from datetime import datetime
from custom_types import Coordinates, Command, CommandsList, ExecutionResult, Trajectory
import sys


DIRECTION_CHANGES: Dict[str, Coordinates] = {
    "east": [1, 0],
    "west": [-1, 0],
    "north": [0, 1],
    "south": [0, -1],
}

"""
This Python code directs a robot to explore a grid, recording unique positions stored as tuples. It tracks time and reports the total number of visited locations. 
"""


def parse_body_instruct_robot_generate_response(
    body: Dict[str, Union[Coordinates, CommandsList]]
) -> ExecutionResult:
    """
    Parses the input body, instructs a robot with commands, and generates a response.

    Args:
        body (Dict[str, Union[Coordinates, CommandsList]]): The input body containing
            the starting position and a list of commands for the robot.

    Returns:
        ExecutionResult: A dictionary containing the timestamp, duration of execution,
            result (total number of visited locations), and the number of commands.

    Example:
    >>> parse_body_instruct_robot_generate_response({
    ...     "start": {"x": 0, "y": 0},
    ...     "commands": [
    ...         {"direction": "east", "steps": 2},
    ...         {"direction": "north", "steps": 1},
    ...     ],
    ... })
    {'timestamp': '2024-01-05T00:00:00', 'duration': 0.0, 'result': 4, 'commands': 2}
    """

    commands, start_position = parse_body(body)
    result, elapsed_time = instruct_robot_and_time_it(start_position, commands)

    response = {
        "timestamp": datetime.now().isoformat(),
        "duration": elapsed_time,
        "result": result,
        "commands": len(commands),
    }
    return response


def parse_body(
    body: Dict[str, Union[Coordinates, CommandsList]]
) -> Tuple[CommandsList, Coordinates]:
    commands = body["commands"]
    start = body["start"]
    start_position = [start["x"], start["y"]]

    return commands, start_position


def instruct_robot_and_time_it(
    start_position: Coordinates, commands: CommandsList
) -> Tuple[int, float]:
    start_time = time.perf_counter()
    result = execute_robot_instructions(start_position, commands)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return result, elapsed_time


def execute_robot_instructions(
    start_position: Coordinates, commands: CommandsList
) -> int:
    """
    Executes the given commands and returns the total number of visited locations.

    Args:
        start_position (Coordinates): The starting position of the robot.
        commands (CommandsList): A list of commands for the robot.

    Returns:
        int: The total number of visited locations.

    Example:
    >>> execute_robot_instructions([0, 0], [{"direction": "east", "steps": 2}])
    3


    Explanation:
    - As storing all visited vertices proves memory intensive and time consuming the aim of this program is to add all the robot's steps and substract all the previously visited vertices.
    - The challenging part is doing so without storing visited vertices, for that two types of intersections have been defined: perpendicular and colinear.
    - The next part consists in calculating all the resulting points of executing a command without the intermediate vertices.
    - The function iterates through each command in the list, updating the robot's position and storing the trajectory.
    - Given that the robot moves only verticaly or horizontaly a trajectory is defined with 3 values:
        -vector around the axis
        -value of the axis than remains the same
        -the type of trajectory, "horizontal" or "vertical"
    -an example of trajectory from (0,5) to (1000,5) would be [[0,1000],5,"horizontal"]
    -an example of trajectory from (10,5) to (10,50) would be [[5,50],10,"vertical"]
    - To sum up for each command, a trajectory is going to be generated, the current position is going to be updated and a new set is going to be created with all
    the intersections happening with the previous trajectories.
    - The trajectories are stored in two different arrays, vertical_trajectories and horizontal_trajectories.
    - The main idea being trying to find perpendicular intersections with the oposite type of trajectories and colinear intersections with the same type of trajectories.
    - The number of intersections is going to be stored for each command.
    - The final result is the difference between the total walked spots and the total number of intersections.

    """
    vertical_trajectories = []
    horizontal_trajectories = []
    total_already_visited = 0
    total_visited_spots = 0
    current_position = start_position
    for command in commands:
        number_of_intersections = move_robot(
            vertical_trajectories,
            horizontal_trajectories,
            current_position,
            command,
        )
        # the extra +1 counting steps aims to take in considaration the vertex where the robot is situated before executing a command, it balances out as it counts as an intersection exept for the first command.
        total_visited_spots += command["steps"] + 1
        total_already_visited += number_of_intersections

    return total_visited_spots - total_already_visited


def move_robot(
    vertical_trajectories,
    horizontal_trajectories,
    current_position: Coordinates,
    command: Command,
) -> int:
    intersections = set()
    next_position = get_next_position(current_position, command)

    if command["direction"] == "north" or command["direction"] == "south":
        trajectory = create_vertical_trajectory(current_position, next_position)
        if len(horizontal_trajectories) > 0:
            get_perpendicular_intersections(
                trajectory, horizontal_trajectories, intersections
            )
        if len(vertical_trajectories) > 0:
            get_colinear_intersections(trajectory, vertical_trajectories, intersections)
        vertical_trajectories.append(trajectory)
        update_position(current_position, next_position)

    else:
        trajectory = create_horizontal_trajectory(current_position, next_position)
        if len(vertical_trajectories) > 0:
            get_perpendicular_intersections(
                trajectory, vertical_trajectories, intersections
            )
        if len(horizontal_trajectories) > 0:
            get_colinear_intersections(
                trajectory, horizontal_trajectories, intersections
            )
        horizontal_trajectories.append(trajectory)
        update_position(current_position, next_position)

    number_of_intersections = len(intersections)
    del intersections
    return number_of_intersections


def update_position(current_position: Coordinates, next_position: Coordinates):
    current_position[0] = next_position[0]
    current_position[1] = next_position[1]


def get_next_position(current_position: Coordinates, command: Command) -> Coordinates:
    direction = DIRECTION_CHANGES[command["direction"]]
    direction = [item * command["steps"] for item in direction]

    next_position = current_position[:]
    next_position[0] = next_position[0] + direction[0]
    next_position[1] = next_position[1] + direction[1]

    return next_position


def create_horizontal_trajectory(
    current_position: Coordinates, next_position: Coordinates
) -> Trajectory:
    vertices = sorted([current_position[0], next_position[0]])
    y_value = current_position[1]
    direction = "horizontal"

    trajectory = [vertices, y_value, direction]

    return trajectory


def create_vertical_trajectory(
    current_position: Coordinates, next_position: Coordinates
) -> Trajectory:
    vertices = sorted([current_position[1], next_position[1]])
    x_value = current_position[0]
    direction = "vertical"

    trajectory = [vertices, x_value, direction]

    return trajectory


def get_perpendicular_intersections(
    trajectory, perpendicular_trajectories, intersections
) -> None:
    for p_t in perpendicular_trajectories:
        if (
            p_t[0][0] <= trajectory[1] <= p_t[0][1]
            and trajectory[0][0] <= p_t[1] <= trajectory[0][1]
        ):
            if trajectory[2] == "horizontal":
                intersection = [p_t[1], trajectory[1]]
                intersections.add(tuple(intersection))
            else:
                intersection = [trajectory[1], p_t[1]]
                intersections.add(tuple(intersection))


def get_colinear_intersections(trajectory, trajectories, intersections) -> None:
    for t in trajectories:
        if t[1] == trajectory[1]:
            overlapping = get_overlapping_values(t[0], trajectory[0])
            values = [trajectory[1]] * len(overlapping)
            if trajectory[2] == "horizontal":
                array_of_coordinates = list(zip(overlapping, values))
            else:
                array_of_coordinates = list(zip(values, overlapping))
            intersections.update(array_of_coordinates)


def get_overlapping_values(range1, range2) -> list[int]:
    # Check for valid ranges
    if range1[0] > range1[1] or range2[0] > range2[1]:
        raise ValueError(
            "Invalid range: end point must be greater than or equal to start point"
        )

    # Check for intersection
    intersection_start = max(range1[0], range2[0])
    intersection_end = min(range1[1], range2[1])

    overlapping_values = list(range(intersection_start, intersection_end + 1))

    return overlapping_values
