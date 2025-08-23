import math
import pytest

from backend.services.timesheet_check_service import check_timesheet_rows

# ---------- Helpers: sample payloads ----------

def base_payload():
    """A valid, passing baseline payload."""
    return {
        "extracted": {
            "week_worked": "2025-08-11..2025-08-17",
            "hours": {
                "Mon": "8hrs", "Tue": "8hrs", "Wed": "8hrs",
                "Thu": "8hrs", "Fri": "8hrs", "Sat": "0hrs", "Sun": "0hrs"
            },
            "total_hours": "40hrs",
            "signatures": True,
            "additional_text": "N/A",
            "employee_name": "John Doe",
            "po_number": "PO#EZX-2025-08-001"
        },
        "expected": {
            "week_worked": "2025-08-11..2025-08-17",
            "hours": {
                "Mon": "8hrs", "Tue": "8hrs", "Wed": "8hrs",
                "Thu": "8hrs", "Fri": "8hrs", "Sat": "0hrs", "Sun": "0hrs"
            },
            "total_hours": "40hrs",
            "employee_name": "John Doe",
            "po_number": "PO#EZX-2025-08-001"
        }
    }

# ---------- Tests ----------

def test_all_pass_when_valid_payload():
    """Happy path: every row returns True."""
    payload = base_payload()
    res = check_timesheet_rows(payload)
    # Week + 7 days + Total + Signatures + Additional Text = 11 rows
    assert set(res.keys()) == {
        "Week Worked",
        "Monday Hours", "Tuesday Hours", "Wednesday Hours", "Thursday Hours",
        "Friday Hours", "Saturday Hours", "Sunday Hours",
        "Total Hours", "Signatures", "Additional Text"
    }
    assert all(res.values())


def test_week_mismatch_fails_only_week_row():
    payload = base_payload()
    payload["extracted"]["week_worked"] = "2025-08-18..2025-08-24"
    res = check_timesheet_rows(payload)

    assert res["Week Worked"] is False
    # Others remain True
    for k, v in res.items():
        if k != "Week Worked":
            assert v is True


def test_daily_invalid_format_causes_that_day_false_only():
    payload = base_payload()
    payload["extracted"]["hours"]["Tue"] = "oops"  # unparsable
    res = check_timesheet_rows(payload)

    assert res["Tuesday Hours"] is False
    # other days unaffected
    for day in ["Monday Hours", "Wednesday Hours", "Thursday Hours",
                "Friday Hours", "Saturday Hours", "Sunday Hours"]:
        assert res[day] is True
    # total still consistent? Tue counted as invalid -> daily parsing error makes that day's row false,
    # but total row still depends on extracted.total and sum parsing; our service sums with parser too.
    # Because Tue unparsable -> sum fails -> total should fail.
    assert res["Total Hours"] is False


def test_daily_over_max_hours_fails_that_day():
    payload = base_payload()
    payload["extracted"]["hours"]["Wed"] = "13hrs"  # > 12 default cap
    res = check_timesheet_rows(payload)

    assert res["Wednesday Hours"] is False
    # Total also becomes invalid because sum includes 13
    assert res["Total Hours"] is False


def test_total_exceeds_expected_fails_total_only():
    payload = base_payload()
    payload["extracted"]["hours"]["Sat"] = "4"            # make sum 44
    payload["extracted"]["total_hours"] = "44"
    # expected total still 40
    res = check_timesheet_rows(payload)

    # Daily rows still valid (0..12)
    for day in ["Saturday Hours"]:
        assert res[day] is True
    # Total fails because extracted_total > expected_total
    assert res["Total Hours"] is False
    # Others pass
    assert res["Week Worked"] is True
    assert res["Signatures"] is True
    assert res["Additional Text"] is True


def test_total_zero_whole_week_invalid():
    payload = base_payload()
    payload["extracted"]["hours"] = {d: "0" for d in
                                     ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]}
    payload["extracted"]["total_hours"] = "0"
    res = check_timesheet_rows(payload)

    # Daily rows pass (0 is allowed)
    for day in ["Monday Hours","Tuesday Hours","Wednesday Hours","Thursday Hours",
                "Friday Hours","Saturday Hours","Sunday Hours"]:
        assert res[day] is True
    # Total must be > 0
    assert res["Total Hours"] is False


def test_total_not_equal_to_sum_fails():
    payload = base_payload()
    # Keep daily 8,8,8,8,8,0,0 => sum 40, but lie total to 39.9
    payload["extracted"]["total_hours"] = "39.9"
    res = check_timesheet_rows(payload)
    assert res["Total Hours"] is False


def test_missing_a_day_fails_that_day_and_total():
    payload = base_payload()
    del payload["extracted"]["hours"]["Thu"]   # missing key
    res = check_timesheet_rows(payload)

    assert res["Thursday Hours"] is False
    # total uses sum over days -> missing day leads to parse path that sets False for that day,
    # and sum likely mismatches total -> Total fails
    assert res["Total Hours"] is False


def test_negative_hours_fails_that_day_and_total():
    payload = base_payload()
    payload["extracted"]["hours"]["Mon"] = "-1"
    res = check_timesheet_rows(payload)

    assert res["Monday Hours"] is False
    assert res["Total Hours"] is False


def test_signature_always_true_when_not_required():
    payload = base_payload()
    payload["extracted"]["signatures"] = False  # extracted says no
    # expected does NOT have require_signature, so rule passes
    res = check_timesheet_rows(payload)
    assert res["Signatures"] is True


def test_signature_required_fails_when_missing():
    payload = base_payload()
    # Simulate a version where expected carries the flag
    payload["expected"]["require_signature"] = True
    payload["extracted"]["signatures"] = False
    res = check_timesheet_rows(payload)

    assert res["Signatures"] is False
    # others still ok
    assert res["Week Worked"] is True
    for day in ["Monday Hours","Tuesday Hours","Wednesday Hours","Thursday Hours",
                "Friday Hours","Saturday Hours","Sunday Hours"]:
        assert res[day] is True
    assert res["Total Hours"] is True
    assert res["Additional Text"] is True


@pytest.mark.parametrize("label, key, val, expected_bool", [
    ("Monday Hours",    "Mon", "0",       True),
    ("Tuesday Hours",   "Tue", "0.25h",   True),
    ("Wednesday Hours", "Wed", "11.99",   True),
    ("Thursday Hours",  "Thu", "12",      True),
    ("Friday Hours",    "Fri", "12.01",   False),  # just over the cap
    ("Saturday Hours",  "Sat", "-0.01",   False),  # negative
])
def test_parametrized_daily_bounds(label, key, val, expected_bool):
    payload = base_payload()
    payload["extracted"]["hours"][key] = val
    # Adjust total to keep consistency where applicable
    # Recompute total from days in a simple way for tests
    def to_num(x):
        return float(str(x).lower().split("h")[0])
    daily = payload["extracted"]["hours"]
    try:
        total = sum(to_num(daily[d]) for d in ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
    except Exception:
        total = payload["extracted"]["total_hours"]  # will make Total fail if unparsable
    payload["extracted"]["total_hours"] = str(total)

    res = check_timesheet_rows(payload)
    assert res[label] is expected_bool
