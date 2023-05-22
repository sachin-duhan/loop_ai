# https://loopxyz.notion.site/Take-home-interview-Store-Monitoring-12664a3c7fdf472883a41457f0c9347d

import os
import base64
import threading

from uuid import uuid4
from flask_cors import CORS
from flask import Flask, jsonify, request

from app.jobs.report import Report
from app.common.redis import Redis
from app.constants import REDIS_JOBS_TABLE
from app.types import JobStatus
from app.constants import LOG_PATH
from app.common.logger import init_logger
from dotenv import load_dotenv

init_logger()
load_dotenv()

# initiate flask
app = Flask(__name__)

CORS(app)
PORT = os.getenv("port", 5000)


@app.route("/trigger_report", methods=["GET"])
def trigger_report():
    report_id = str(uuid4())
    trigger_report_thread = threading.Thread(target=Report().process, args=[report_id])
    trigger_report_thread.start()

    return (
        jsonify({"report_id": report_id, "status": f"localhost:{PORT}/get_report"}),
        200,
    )


@app.route("/get_report", methods=["POST"])
def get_report():
    body = request.get_json()
    report_id = body["report_id"]

    with Redis() as redis_client:
        response = {
            "status": redis_client.hget(REDIS_JOBS_TABLE, report_id).decode(),
            "report": None,
        }
        if response["status"] == JobStatus.RUNNING.value:
            return jsonify(response)
        elif not os.path.exists(os.path.join(LOG_PATH, report_id + ".csv")):
            response["status"] = "Report does not exist"
            return jsonify(response)
        else:
            response["status"] = JobStatus.COMPLETED.value
            with open(f"{str(report_id)}.csv", "rb") as report_file:
                response["report"] = base64.b64encode(report_file.read()).decode(
                    "utf-8"
                )

        status_code = 200 if response["status"] != JobStatus.FAILED.value else 500
        return jsonify(response), status_code


@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify({"msg": "Internal server error"}), 500


@app.errorhandler(500)
def internal_server_error_500(e):
    return jsonify({"msg": "Internal server error"}), 500


app.run(debug=os.getenv("env", "dev") == "dev")
