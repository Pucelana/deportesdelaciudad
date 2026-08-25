from flask import Blueprint, send_from_directory
import os

service_worker_bp = Blueprint("service_worker", __name__)


@service_worker_bp.route("/service-worker.js")
def service_worker():
    return send_from_directory(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "service-worker.js",
        mimetype="application/javascript"
    )