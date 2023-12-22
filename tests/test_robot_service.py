import unittest
from robot_service import (
    parse_body_instruct_robot_generate_response,
    parse_body,
    execute_robot_instructions,
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

        self.assertEqual(
            result, 4
        )  # Assuming the robot will visit four unique positions

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

    def test_move_robot_1(self):
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

    def test_move_robot_1_and_return(self):
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

    def test_move_robot_long_distance(self):
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
