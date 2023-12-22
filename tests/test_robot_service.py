import unittest
from custom_types import Coordinates, Command, CommandsList
from robot_service import (
    parse_body_instruct_robot_generate_response,
    parse_body,
    execute_robot_instructions,
    move_robot,
    update_position,
)


class TestRobotMovement(unittest.TestCase):
    def test_parse_body(self):
        body = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
            ],
        }

        commands, start_position = parse_body(body)

        self.assertEqual(len(commands), 2)
        self.assertEqual(start_position, [10, 22])

    def test_execute_robot_instructions(self):
        start_position = [0, 0]
        commands = [
            {"direction": "east", "steps": 2},
            {"direction": "north", "steps": 1},
        ]

        result = execute_robot_instructions(start_position, commands)

        self.assertEqual(result, 4)

    def test_parse_body_instruct_robot_generate_response(self):
        body = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
            ],
        }

        response = parse_body_instruct_robot_generate_response(body)

        self.assertIn("timestamp", response)
        self.assertIn("duration", response)
        self.assertIn("result", response)
        self.assertIn("commands", response)

    def test_parse_and_instruct_robot_1(self):
        JSON_BODY = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
            ],
        }

        self.assertEqual(
            parse_body_instruct_robot_generate_response(JSON_BODY)["result"], 4
        )

    def test_parse_and_instruct_robot_back_to_start(self):
        JSON_BODY = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
                {"direction": "south", "steps": 1},
                {"direction": "west", "steps": 2},
            ],
        }

        self.assertEqual(
            parse_body_instruct_robot_generate_response(JSON_BODY)["result"], 4
        )

    def test_move_robot_2(self):
        JSON_BODY = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
                {"direction": "south", "steps": 1},
                {"direction": "west", "steps": 3},
                {"direction": "north", "steps": 10},
            ],
        }
        self.assertEqual(
            parse_body_instruct_robot_generate_response(JSON_BODY)["result"], 15
        )

    def test_parse_and_instruct_robot_long_distance(self):
        JSON_BODY = {
            "start": {"x": 10, "y": 22},
            "commands": [
                {"direction": "east", "steps": 2},
                {"direction": "north", "steps": 1},
                {"direction": "south", "steps": 1},
                {"direction": "west", "steps": 3},
                {"direction": "north", "steps": 100000},
                {"direction": "south", "steps": 100000},
                {"direction": "west", "steps": 100000},
                {"direction": "north", "steps": 1},
                {"direction": "east", "steps": 100000},
            ],
        }
        self.assertEqual(
            parse_body_instruct_robot_generate_response(JSON_BODY)["result"], 300005
        )

    def test_move_robot(self):
        visited_vertices = set()
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 1}
        move_robot(visited_vertices, current_position, command)

        self.assertIn((0, 1), visited_vertices)

    def test_move_robot_error(self):
        visited_vertices = set()
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 1}
        move_robot(visited_vertices, current_position, command)

        self.assertNotIn((0, 2), visited_vertices)

    def test_update_position_north(self):
        current_position: Coordinates = [0, 2]
        direction: Coordinates = [0, 1]

        self.assertEqual(update_position(current_position, direction), [0, 3])

    def test_update_position_south(self):
        current_position: Coordinates = [0, 2]
        direction: Coordinates = [0, -1]

        self.assertEqual(update_position(current_position, direction), [0, 1])

    def test_update_position_east(self):
        current_position: Coordinates = [0, 2]
        direction: Coordinates = [1, 0]

        self.assertEqual(update_position(current_position, direction), [1, 2])

    def test_update_position_west(self):
        current_position: Coordinates = [0, 2]
        direction: Coordinates = [-1, 0]

        self.assertEqual(update_position(current_position, direction), [-1, 2])


if __name__ == "__main__":
    unittest.main()
