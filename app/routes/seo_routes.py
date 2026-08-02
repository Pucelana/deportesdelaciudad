from flask import Blueprint, send_from_directory

seo_bp = Blueprint("seo", __name__)

@seo_bp.route("/robots.txt")
def robots():
    return send_from_directory("static", "robots.txt")