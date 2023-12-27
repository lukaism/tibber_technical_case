import unittest
import psycopg2
import os
from utils import parse_env_variable
from record_service import (
    save_result,
    try_insert_record,
    verify_insertion,
)

CORRECT_RECORD = {
    "timestamp": "2023-01-01 12:00:00",
    "commands": 11,
    "result": 1,
    "duration": 2.5,
}

INCORRECT_RECORD = {
    "commands": 10,
    "result": 1,
    "duration": 2.5,
}


def deleteInsertedRecord(id: int):
    url = os.getenv("DATABASE_URL")
    url = parse_env_variable(url)

    connection = psycopg2.connect(url)
    with connection as connection:
        with connection.cursor() as cursor:
            delete_query = "DELETE FROM records WHERE id = %s;"
            cursor.execute(delete_query, (id,))


class TestYourModule(unittest.TestCase):
    def setUp(self) -> None:
        url = os.getenv("DATABASE_URL")
        self.url = parse_env_variable(url)
        self.connection = psycopg2.connect(self.url)

    def test_save_result_success(self):
        result = save_result(CORRECT_RECORD)

        id = result[0]["id"]
        deleteInsertedRecord(id)
        self.assertEqual(result[1], 201)
        self.assertIn("id", result[0])

    def test_save_result_failure(self):
        with self.assertRaises(Exception) as context:
            save_result(INCORRECT_RECORD)
        self.assertIsNotNone(context.exception)
        self.assertEqual(str(context.exception), "'timestamp'")

    def test_insert_record_correct(self):
        with self.connection as connection:
            with connection.cursor() as cursor:
                try_insert_record(cursor, CORRECT_RECORD)
                result = verify_insertion(cursor)

        id = result[0]["id"]
        deleteInsertedRecord(id)
        self.assertEqual(result[1], 201)

    def test_insert_record_error(self):
        with self.assertRaises(Exception) as context:
            with self.connection as connection:
                with connection.cursor() as cursor:
                    try_insert_record(cursor, INCORRECT_RECORD)

        self.assertIsNotNone(context.exception)
        self.assertEqual(str(context.exception), "'timestamp'")


if __name__ == "__main__":
    unittest.main()
