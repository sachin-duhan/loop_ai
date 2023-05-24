#! /usr/bin/python3

__author__ = "Sachin duhan"

import os
import base64
import logging
import threading

from uuid import uuid4
from flask_cors import CORS
from flask import Flask, jsonify, request
from dotenv import load_dotenv

from app.jobs.report import Report
from app.common.redis import Redis
from app.constants import REDIS_JOBS_TABLE
from app.jobs import JobStatus
from app.constants import REPORT_OUTPUT_PATH
from app.common.logger import init_logger

init_logger()
load_dotenv()

# initiate flask
app = Flask(__name__)

CORS(app)
PORT = os.getenv("port", 5000)

LOGGER = logging.getLogger(__name__)

@app.route('/', methods=['get'])
def health_check():
    return jsonify({
        "status": "Running..."
    })

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
            "message": "ok"
        }
        if response["status"] == JobStatus.RUNNING:
            response['message'] = 'Processing report, please retry after sometime.'
            return jsonify(response), 200
        elif response['status'] == JobStatus.FAILED:
            response['message'] = "Failed to create report, please try again."
            return jsonify(response), 400
        else:
            response["status"] = JobStatus.COMPLETED
            report_file = os.path.join(REPORT_OUTPUT_PATH, f"{str(report_id)}.csv")

            if not os.path.exists(report_file):
                response['message'] = "Report not found, something went wrong."
                return jsonify(response), 500

            with open(report_file, "rb") as report_file:
                response["report"] = base64.b64encode(report_file.read()).decode("utf-8")
                LOGGER.success(f"Delivered report {report_id}")
                report_file.close()

        status_code = 200 if response["status"] != JobStatus.FAILED else 500
        return jsonify(response), status_code


@app.errorhandler(Exception)
def internal_server_error(e):
    return jsonify({"msg": "Internal server error"}), 500


@app.errorhandler(500)
def internal_server_error_500(e):
    return jsonify({"msg": "Internal server error"}), 500


def run():
    LOGGER.info("Starting loop.xyx server...")
    app.run(debug=os.getenv("env", "dev") == "dev")

if __name__ == "__main__": run()