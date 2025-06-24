from flask import Blueprint, request
import csv
import os
import logging

random_bp = Blueprint('random', __name__)
PATH_PREFIX='csv'

log = logging.getLogger("main")

def csv_to_json(file_path: str) -> dict:
    current_dir = os.path.dirname(__file__)
    with open(f"{current_dir}/{PATH_PREFIX}/{file_path}") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)


@random_bp.route("/companies")
def get_companies():
    limit = request.args.get("limit", None)
    limit = int(limit) if limit else None
    log.info(f"Request headers: {request.headers}")
    return csv_to_json(f"MOCK_DATA_companies.csv")[:limit]

