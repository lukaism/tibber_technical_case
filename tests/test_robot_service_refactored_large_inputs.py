import unittest
from custom_types import Coordinates, Command
from robot_service_refactored_for_large_inputs import (
    parse_body_instruct_robot_generate_response,
    parse_body,
    execute_robot_instructions,
)
from test_helpers import LONG_JSON_BODY


class TestRobotMovementRefactor(unittest.TestCase):
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

    def test_execute_robot_instructions_extensive(self):
        # This test is being bypassed as it's a heavy one and takes some seconds.
        return
        self.assertEqual(
            parse_body_instruct_robot_generate_response(LONG_JSON_BODY)["result"],
            993737501,
        )

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

    def test_move_robot_farther(self):
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
                {"direction": "north", "steps": 10},
                {"direction": "south", "steps": 10},
                {"direction": "west", "steps": 10},
                {"direction": "north", "steps": 1},
                {"direction": "east", "steps": 10},
            ],
        }
        self.assertEqual(
            parse_body_instruct_robot_generate_response(JSON_BODY)["result"], 35
        )

    def test_parse_and_instruct_robot_longer_distance(self):
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


if __name__ == "__main__":
    unittest.main()
