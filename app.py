from flask import Flask, request, jsonify
from robot_service import *
from custom_types import ExecutionResult
from record_service import save_result

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, Docker!"


@app.post("/tibber-developer-test/enter-path")
def main():
    data = request.get_json()
    try:
        result: ExecutionResult = parse_body_instruct_robot_generate_response(data)
        try:
            response = save_result(result)
        except Exception as e:
            message = {
                "error": "There was a problem inserting the record into the database: "
                f"{e}"
            }
            return (
                message,
                500,
            )
        return jsonify(response), 201
    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500
