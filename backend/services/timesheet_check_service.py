# backend/services/timesheet_check_service.py
# -*- coding: utf-8 -*-
"""
Timesheet checking service
-------------------------

Compares Extracted vs Expected data and returns a boolean per **table row**:
- Week Worked
- Monday Hours … Sunday Hours
- Total Hours
- Signatures
- Additional Text

Notes:
- Daily hours are *validated for reasonableness* (>=0 and <= MAX_DAILY_HOURS_DEFAULT)
  and parsability only. They do **not** need to equal Expected.
- Total Hours must equal the sum of daily hours (±HOUR_TOLERANCE), must not exceed
  Expected total, and must be > 0.
- Signatures pass unless Expected explicitly sets `require_signature: true`.
- Additional Text always passes (by current spec).
"""

from typing import Dict, Any
from backend.config.config import MAX_DAILY_HOURS_DEFAULT, HOUR_TOLERANCE
import re

# Map short keys in extracted/expected.hours to full UI labels
DAY_LABELS = [
    ("Mon", "Monday Hours"),
    ("Tue", "Tuesday Hours"),
    ("Wed", "Wednesday Hours"),
    ("Thu", "Thursday Hours"),
    ("Fri", "Friday Hours"),
    ("Sat", "Saturday Hours"),
    ("Sun", "Sunday Hours"),
]


def _to_hours(v) -> float:
    """
    Normalize a value to a float number of hours.

    Accepts:
      - int/float (e.g., 8, 7.5)
      - strings like "8", "8h", "8hrs", "7.5hrs"
    Raises:
      ValueError if unparsable or None.
    """
    if v is None:
        raise ValueError("Empty hour value")
    if isinstance(v, (int, float)):
        return float(v)

    s = str(v).strip().lower()
    m = re.match(r"^\s*([0-9]+(?:\.[0-9]+)?)", s)
    if not m:
        raise ValueError(f"Unparsable hour: {v}")
    return float(m.group(1))


def _sum_hours(hours_map: Dict[str, Any]) -> float:
    """Sum hours for the full Mon–Sun set; missing day counts as 0."""
    total = 0.0
    for short_key, _label in DAY_LABELS:
        total += _to_hours(hours_map.get(short_key, "0"))
    return total


def check_timesheet_rows(payload: Dict[str, Any]) -> Dict[str, bool]:
    """
    Validate timesheet data row by row.

    Input shape (dicts are fine; dataclasses optional):
      {
        "extracted": {
          "week_worked": "2025-08-11..2025-08-17",
          "hours": {"Mon":"8hrs","Tue":"7.5hrs",...},
          "total_hours": "40hrs",
          "signatures": true/false (optional),
          "additional_text": ".../optional",
          "employee_name": "...",
          "po_number": "..."
        },
        "expected": {
          "week_worked": "2025-08-11..2025-08-17",
          "hours": {"Mon":"8hrs",...},   # reference schedule only
          "total_hours": "40hrs",
          "employee_name": "...",
          "po_number": "..."
          # "require_signature": true  # optional flag, if ever used
        }
      }

    Returns: booleans per table row (keys match UI labels exactly).
    """
    extracted = payload.get("extracted", {}) or {}
    expected = payload.get("expected", {}) or {}

    ext_hours = extracted.get("hours", {}) or {}
    exp_hours = expected.get("hours", {}) or {}

    # --- Week Worked: must match exactly
    week_pass = (str(extracted.get("week_worked", "")).strip()
                 == str(expected.get("week_worked", "")).strip())

    # --- Daily Hours: validate presence/parsability and numeric bounds
    # We do not require equality with expected day-by-day.
    day_checks: Dict[str, bool] = {}
    for short_key, label in DAY_LABELS:
        try:
            h = _to_hours(ext_hours[short_key])  # KeyError -> except
            day_checks[label] = (0.0 <= h <= MAX_DAILY_HOURS_DEFAULT)
        except Exception:
            # Any issue (missing, negative, unparsable, > cap) => False,
            # but we still emit the label to avoid KeyError in callers.
            day_checks[label] = False

    # --- Total Hours:
    # 1) equals sum of daily (± tolerance)
    # 2) <= expected total
    # 3) > 0
    try:
        ext_total = _to_hours(extracted.get("total_hours"))
    except Exception:
        ext_total = -1.0  # force failure

    # expected total: prefer explicit total; fallback to sum of expected days
    try:
        exp_total = _to_hours(expected.get("total_hours"))
    except Exception:
        try:
            exp_total = _sum_hours(exp_hours)
        except Exception:
            exp_total = 0.0

    # recompute daily sum from extracted days
    try:
        daily_sum = _sum_hours(ext_hours)
    except Exception:
        daily_sum = float("nan")

    total_consistent = abs(daily_sum - ext_total) < HOUR_TOLERANCE
    total_not_exceed = (ext_total <= exp_total)
    total_gt_zero = (ext_total > 0)
    total_pass = bool(total_consistent and total_not_exceed and total_gt_zero)

    # --- Signatures:
    # default: not required => always true
    require_sig = bool(expected.get("require_signature", False))
    signatures_pass = bool(extracted.get("signatures", False)) if require_sig else True

    # --- Additional Text: always true (per current spec)
    additional_text_pass = True

    # --- Final dictionary: keys match the UI
    return {
        "Week Worked": week_pass,
        **day_checks,               # Monday … Sunday
        "Total Hours": total_pass,
        "Signatures": signatures_pass,
        "Additional Text": additional_text_pass,
    }


__all__ = ["check_timesheet_rows"]


