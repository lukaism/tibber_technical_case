import unittest
import psycopg2
import os
from utils import parse_env_variable
from record_service import (
    save_result,
    try_insert_record,
    verify_insertion,
)


def deleteInsertedRecord(id: int):
    url = os.getenv("DATABASE_URL")
    url = parse_env_variable(url)

    connection = psycopg2.connect(url)
    with connection as connection:
        with connection.cursor() as cursor:
            # Use a parameterized query to avoid SQL injection
            delete_query = "DELETE FROM records WHERE id = %s;"
            cursor.execute(delete_query, (id,))


class TestYourModule(unittest.TestCase):
    def test_save_result_success(self):
        record = {
            "timestamp": "2023-01-01 12:00:00",
            "commands": 11,
            "result": 1,
            "duration": 2.5,
        }
        result = save_result(record)

        id = result[0]["id"]
        deleteInsertedRecord(id)
        self.assertEqual(result[1], 201)
        self.assertIn("id", result[0])

    def test_save_result_table_creation_failure(self):
        record = {
            "commands": 10,
            "result": 1,
            "duration": 2.5,
        }

        result = save_result(record)
        self.assertEqual(result[1], 500)

    def test_insert_record_correct(self):
        url = os.getenv("DATABASE_URL")
        url = parse_env_variable(url)

        record = {
            "timestamp": "2023-01-01 12:00:00",
            "commands": 11,
            "result": 1,
            "duration": 2.5,
        }
        connection = psycopg2.connect(url)
        with connection as connection:
            with connection.cursor() as cursor:
                try_insert_record(cursor, record)
                result = verify_insertion(cursor)

        id = result[0]["id"]
        deleteInsertedRecord(id)
        self.assertEqual(result[1], 201)

    def test_insert_record_error(self):
        url = os.getenv("DATABASE_URL")
        url = parse_env_variable(url)

        record = {
            "timestamp": "2023-01-01 12:00:00",
            "result": 1,
            "duration": 2.5,
        }
        connection = psycopg2.connect(url)
        with connection as connection:
            with connection.cursor() as cursor:
                result = try_insert_record(cursor, record)

        self.assertEqual(result[1], 500)


if __name__ == "__main__":
    unittest.main()
