import psycopg2
import os
from custom_types import ExecutionResult
from utils import parse_env_variable


url = os.getenv("DATABASE_URL")
url = parse_env_variable(url)

connection = psycopg2.connect(url)


CREATE_RECORD_TABLE = """
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    "Timestamp" TIMESTAMP,
    "Commands" INTEGER,
    "Result" INTEGER,
    "Duration" FLOAT
);
"""

INSERT_RECORD = """
INSERT INTO records ("Timestamp", "Commands", "Result", "Duration")
VALUES (%s, %s, %s, %s) RETURNING id, "Timestamp", "Commands", "Result", "Duration";
"""


def save_result(record: ExecutionResult):
    try:
        with connection:
            with connection.cursor() as cursor:
                try_create_record_table(cursor)
                try_insert_record(cursor, record)

                response = verify_insertion(cursor)
                return response

    except Exception as e:
        raise Exception(e) from None


def create_record_table(cursor):
    cursor.execute(CREATE_RECORD_TABLE)


def try_create_record_table(cursor):
    try:
        create_record_table(cursor)
    except Exception as e:
        raise Exception(e) from None


def try_insert_record(cursor, record: ExecutionResult):
    try:
        insert_record(cursor, record)
    except Exception as e:
        raise Exception(e) from None


def return_error(e: Exception):
    return {"message": f"Error: {e}"}, 500


def insert_record(cursor, record: ExecutionResult):
    cursor.execute(
        INSERT_RECORD,
        (
            record["timestamp"],
            record["commands"],
            record["result"],
            record["duration"],
        ),
    )


def verify_insertion(cursor):
    inserted_row = cursor.fetchone()
    if inserted_row:
        id, timestamp, commands, result, duration = inserted_row
        return {
            "id": id,
            "Timestamp": timestamp,
            "Commands": commands,
            "Result": result,
            "Duration": duration,
            "message": "Record inserted successfully.",
        }, 201
    else:
        return {"message": "Oops! Something went wrong during insertion."}, 500
