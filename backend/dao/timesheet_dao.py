from typing import Optional, Any, Dict, List
from sqlalchemy import select
from persistence.session import SessionLocal
from models.timesheet_orm import Timesheet

# ---------- helpers ----------
_DAY_ABBR = {
    "monday": "Mon",
    "tuesday": "Tues",   
    "wednesday": "Wed",
    "thursday": "Thur",
    "friday": "Fri",
    "saturday": "Sat",
    "sunday": "Sun",
}

def _hhmm_to_hrs(s: str) -> str:
    """Convert 'H:MM' (e.g., '7:30') to '7.5hrs'. Empty/zero -> '0hrs'."""
    if not s or s == "0:00":
        return "0hrs"
    try:
        h, m = s.split(":")
        val = int(h) + int(m) / 60.0
        # Pretty formatting: integers like 8.0 -> '8hrs'; otherwise '7.5hrs'
        return f"{int(val)}hrs" if abs(val - round(val)) < 1e-9 else f"{val:g}hrs"
    except Exception:
        # if already like '8hrs' or '7.5hrs', pass through
        return s if s.endswith("hrs") else f"{s}"


def _extract_minimal_payload(meta: Dict[str, Any]) -> Dict[str, Any]:
    """Build the small 'extracted' dict from the large meta_data JSON."""
    # employee & PO
    employee_name = meta.get("employee", {}).get("name", "")
    po_number = meta.get("base", {}).get("po_number", "")

    # hours by day – prefer totals_row.by_day, fallback to work_entries totals
    hours: Dict[str, str] = {}
    by_day = meta.get("totals_row", {}).get("by_day") or {}
    if by_day:
        # values like '7:30' -> '7.5hrs'
        for k, v in by_day.items():
            hours[k] = _hhmm_to_hrs(v)
    else:
        for w in meta.get("work_entries", []) or []:
            abbr = _DAY_ABBR.get(str(w.get("weekday", "")).lower(), None)
            if not abbr:
                continue
            hhmm = w.get("total_daily_hours", "") or ""
            hours[abbr] = _hhmm_to_hrs(hhmm)

    # total hours – prefer decimal if present, else convert "H:MM"
    weekly_total = meta.get("weekly_total", {}) or {}
    total_hours = None
    if "total_decimal_hours" in weekly_total:
        val = weekly_total.get("total_decimal_hours")
        if isinstance(val, (int, float)):
            total_hours = f"{val:g}hrs"
    if not total_hours:
        total_hours = _hhmm_to_hrs(weekly_total.get("total_hours", "") or "")

    # week range from min/max date_iso in work_entries
    dates: List[str] = [w.get("date_iso") for w in meta.get("work_entries", []) or [] if w.get("date_iso")]
    dates = sorted(dates)
    week_worked = f"{dates[0]}..{dates[-1]}" if dates else ""

    # optional fields if your pipeline fills them
    additional_text = meta.get("additional_text")  # keep None if missing
    signatures = meta.get("signatures")           # keep None if missing

    extracted = {
        "week_worked": week_worked,
        "hours": hours,
        "total_hours": total_hours or "0hrs",
        "employee_name": employee_name,
        "po_number": po_number,
    }
    if signatures is not None:
        extracted["signatures"] = bool(signatures)
    if additional_text is not None:
        extracted["additional_text"] = str(additional_text)

    return extracted
# ---------- /helpers ----------



def get_metadata_by_tid(tid: int) -> Optional[Dict[str, Any]]:
    """Fetch a *small* 'extracted' subset from `timesheet.meta_data`.

    Purpose:
        Query the `timesheet` row by `tid`, then shrink the large JSON to the
        fields your validator needs:
            - week_worked: "YYYY-MM-DD..YYYY-MM-DD"
            - hours: {"Mon":"8hrs", "Tues":"7.5hrs", ...}
            - total_hours: "40.5hrs" (or "40hrs")
            - employee_name, po_number
            - signatures/additional_text (optional; included only if present)

    Example: >>> get_metadata_by_tid(1)
        {'week_worked': '2025-08-11..2025-08-17', 'hours': {'Mon': '7.5hrs', ...}, ...}

    Returns:
        Optional[Dict[str, Any]]: The minimal 'extracted' dict, or None if not found.
    """
    with SessionLocal() as session:
        meta: Optional[Dict[str, Any]] = session.execute(
            select(Timesheet.meta_data).where(Timesheet.tid == tid)
        ).scalar_one_or_none()

    if meta is None:
        return None

    return _extract_minimal_payload(meta)
    
    


