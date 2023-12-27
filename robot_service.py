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


def parse_body_instruct_robot_generate_response(
    body: Dict[str, Union[Coordinates, CommandsList]]
) -> ExecutionResult:
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


def instruct_robot_and_time_it(start_position: Coordinates, commands: CommandsList):
    start_time = time.perf_counter()
    result = execute_robot_instructions(start_position, commands)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return result, elapsed_time


def execute_robot_instructions(
    start_position: Coordinates, commands: CommandsList
) -> int:
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
    current_position[0] = current_position[0] + direction[0]
    current_position[1] = current_position[1] + direction[1]

    return current_position
