import psycopg2
import os
from custom_types import ExecutionResult


url = os.getenv("DATABASE_URL")
url = url.replace("'", "")
url = url.replace('"', "")

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
                try:
                    create_record_table(cursor)
                except Exception as e:
                    return return_error(e)
                try:
                    insert_record(cursor, record)
                except Exception as e:
                    return return_error(e)

                response = verify_insertion(cursor)
                return response

    except Exception as e:
        print(f"Error: {e}")
        return {"message": f"Error: {e}"}, 500


def create_record_table(cursor):
    cursor.execute(CREATE_RECORD_TABLE)


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
        id, time_of_insertion, commands, result, duration = inserted_row
        return {
            "id": id,
            "TimeOfInsertion": time_of_insertion,
            "Commands": commands,
            "Result": result,
            "Duration": duration,
            "message": "Record inserted successfully.",
        }, 201
    else:
        return {"message": "Oops! Something went wrong during insertion."}, 500
