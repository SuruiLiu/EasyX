from flask import Blueprint, jsonify
from dao.timesheet_dao import get_metadata_by_tid

bp_timesheet_query = Blueprint("timesheet_query", __name__)

@bp_timesheet_query.get("/timesheet/<int:tid>")
def get_timesheet_metadata(tid: int):
    """Return `timesheet.meta_data` as JSON by `tid`.

    Purpose:
        Read-only endpoint that delegates to the DAO to fetch `meta_data`.
        Responds with 200 and the JSON when found; otherwise 404.

    Example:
        # Success:
        curl -i http://localhost:5001/timesheet/1
        # -> HTTP/1.0 200 OK
        # -> {"note":"seed row 1"}

        # Not found:
        curl -i http://localhost:5001/timesheet/9999
        # -> HTTP/1.0 404 NOT FOUND
        # -> {"error":"Timesheet not found"}

    Returns:
        Flask Response:
            - 200 OK + application/json (the `meta_data` JSON) if found.
            - 404 Not Found + {"error": "..."} if no such `tid`.
    """
    metadata = get_metadata_by_tid(tid)
    if metadata is None:
        return jsonify({"error": "Timesheet not found"}), 404
    return jsonify(metadata), 200
