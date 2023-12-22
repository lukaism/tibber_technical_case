import unittest
import psycopg2
import os
from unittest.mock import MagicMock
from record_service import (
    save_result,
    create_record_table,
    return_error,
    insert_record,
    verify_insertion,
)


def deleteInsertedRecord(id: int):
    url = os.getenv("DATABASE_URL")
    url = url.replace("'", "")
    url = url.replace('"', "")

    connection = psycopg2.connect(url)
    with connection as connection:
        with connection.cursor() as cursor:
            # Use a parameterized query to avoid SQL injection
            delete_query = "DELETE FROM records WHERE id = %s;"
            cursor.execute(delete_query, (id,))


class TestYourModule(unittest.TestCase):
    def setUp(self):
        # Create a mock for the psycopg2 connection
        self.mock_connection = MagicMock()
        self.mock_cursor = self.mock_connection.cursor.return_value

    def test_save_result_success(self):
        # Mock the psycopg2.connect method
        with unittest.mock.patch("psycopg2.connect", return_value=self.mock_connection):
            record = {
                "timestamp": "2023-01-01 12:00:00",
                "commands": 11,
                "result": 1,
                "duration": 2.5,
            }
            self.mock_cursor.fetchone.return_value = (
                1,
                "2023-01-01 12:00:00",
                10,
                1,
                2.5,
            )

            result = save_result(record)

        id = result[0]["id"]
        deleteInsertedRecord(id)
        self.assertEqual(result[1], 201)  # Check status code
        self.assertIn("id", result[0])  # Check if id is present in the response

    def test_save_result_table_creation_failure(self):
        with unittest.mock.patch("psycopg2.connect", return_value=self.mock_connection):
            self.mock_cursor.execute.side_effect = Exception("Table creation error")
            record = {
                "commands": 10,
                "result": 1,
                "duration": 2.5,
            }

            result = save_result(record)

        self.assertEqual(result[1], 500)  # Check status code


if __name__ == "__main__":
    unittest.main()
