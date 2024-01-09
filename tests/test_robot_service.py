import unittest
from custom_types import Coordinates, Command
from robot_service import (
    parse_body_instruct_robot_generate_response,
    parse_body,
    execute_robot_instructions,
    move_robot,
    update_position,
    generate_trajectory,
    generate_trajectory_2,
)
from test_helpers import LONG_JSON_BODY


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

    def test_execute_robot_instructions_extensive(self):
        result = parse_body_instruct_robot_generate_response(LONG_JSON_BODY)

        self.assertEqual(result, 4)

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

    def test_move_robot_records_correct_vertices(self):
        ## Here we test to ensure corerct spaces are counted as visited
        visited_vertices = set()
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 2}
        move_robot(visited_vertices, current_position, command)

        self.assertIn((0, 1), visited_vertices)
        self.assertIn((0, 2), visited_vertices)

    def test_move_robot_unvisited_spaces(self):
        ## Here we test to ensure no incorerct spaces are counted as visited
        visited_vertices = set()
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 1}
        move_robot(visited_vertices, current_position, command)

        self.assertNotIn((0, 2), visited_vertices)
        self.assertNotIn((0, -1), visited_vertices)
        self.assertNotIn((1, 0), visited_vertices)
        self.assertNotIn((1, 1), visited_vertices)
        self.assertNotIn((1, -1), visited_vertices)
        self.assertNotIn((-1, 0), visited_vertices)
        self.assertNotIn((-1, -1), visited_vertices)
        self.assertNotIn((-1, 1), visited_vertices)

        self.assertIn((0, 1), visited_vertices)

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

    def test_generate_trajectory(self):
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 2}
        result = generate_trajectory(current_position, command)
        self.assertEqual(result, [(0, 0), (0, 1), (0, 2)])

    def test_generate_trajectory_2(self):
        current_position: Coordinates = [0, 0]
        command: Command = {"direction": "north", "steps": 2}
        result = generate_trajectory_2(current_position, command)
        self.assertEqual(result, [(0, 0), (0, 1), (0, 2)])


if __name__ == "__main__":
    unittest.main()
