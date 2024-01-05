from typing import Dict, Tuple, Union
import time
from datetime import datetime
from custom_types import Coordinates, Command, CommandsList, ExecutionResult


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
    Executes the given commands and returns the total number of visited locations using a set as we just have to measure unique visited positions.

    Args:
        start_position (Coordinates): The starting position of the robot.
        commands (CommandsList): A list of commands for the robot.

    Returns:
        int: The total number of visited locations.

    Example:
    >>> execute_robot_instructions([0, 0], [{"direction": "east", "steps": 2}])
    3
    """

    visited_vertices = set()
    visited_vertices.add(tuple(start_position))
    current_position = start_position

    for command in commands:
        move_robot(visited_vertices, current_position, command)

    return len(visited_vertices)


def move_robot(
    visited_vertices: set, current_position: Coordinates, command: Command
) -> None:
    for _ in range(command["steps"]):
        direction = DIRECTION_CHANGES[command["direction"]]
        current_position = update_position(current_position, direction)
        visited_vertices.add(tuple(current_position))


def update_position(
    current_position: Coordinates, direction: Coordinates
) -> Coordinates:
    """
    Updates the current position based on the given direction.

    Args:
        current_position (Coordinates): The current position of the robot.
        direction (Coordinates): The direction to move (change in coordinates).

    Returns:
        Coordinates: The new position of the robot.

    Example:
    >>> update_position([0, 0], [1, 0])
    [1, 0]
    """

    new_position = [
        current_position[0] + direction[0],
        current_position[1] + direction[1],
    ]
    return new_position
