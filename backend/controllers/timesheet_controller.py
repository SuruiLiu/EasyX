from flask import Blueprint, request, jsonify
from services.timesheet_check_service import check_timesheet_rows

bp_timesheet = Blueprint("timesheet", __name__)

@bp_timesheet.post("/timesheet/check")
def check_timesheet():
    payload = request.get_json(force=True, silent=True) or {}
    print("RESULT FROM SERVICE:", check_timesheet_rows(payload))  # 加这一行
    return jsonify(check_timesheet_rows(payload)), 200
