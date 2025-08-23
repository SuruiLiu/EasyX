from flask import Blueprint, jsonify, request
from services.dao.get_timesheet_by_id import get_metadata_by_tid

timesheet_bp = Blueprint('timesheet', __name__)

@timesheet_bp.route('/timesheet/<int:tid>', methods=['GET'])
def get_timesheet(tid):
    try:
        metadata = get_metadata_by_tid(tid)
        if metadata is not None:
            return jsonify(metadata), 200 # dict/list OK; jsonify ensures application/json
        return jsonify({"error": "Timesheet not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
