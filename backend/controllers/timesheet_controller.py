from flask import Blueprint, request, jsonify
from backend.services.timesheet_check_service import check_timesheet_rows

bp_timesheet = Blueprint("timesheet", __name__)

@bp_timesheet.post("/timesheet/check")
def check_timesheet():
    payload = request.get_json(force=True, silent=True) or {}
    return jsonify(check_timesheet_rows(payload)), 200
