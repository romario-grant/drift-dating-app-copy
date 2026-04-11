from flask import Blueprint, jsonify

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Drift Dating API is running with PostgreSQL"}), 200