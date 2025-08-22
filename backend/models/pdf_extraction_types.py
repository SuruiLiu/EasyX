"""
PDF Extraction Types
Define JSON format structure for PDF extraction
"""

from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class BaseInfo:
    """Basic information"""
    po_number: str
    client: str
    supervisor: str

@dataclass
class EmployeeInfo:
    """Employee information"""
    name: str
    company: str

@dataclass
class TimePeriod:
    """Time period information"""
    start: str
    finish: str
    time: str

@dataclass
class ExtraInOut:
    """Extra in/out time"""
    morning: str
    afternoon: str

@dataclass
class WorkEntry:
    """Work entry"""
    weekday: str
    date_original: str
    date_iso: str
    morning: TimePeriod
    afternoon: TimePeriod
    extra_in_out: ExtraInOut
    total_daily_hours: str
    total_daily_decimal: float

@dataclass
class WeeklyTotal:
    """Weekly total"""
    total_hours: str
    total_decimal_hours: float

@dataclass
class TaskPerDay:
    """Task per day time"""
    Mon: str
    Tues: str
    Wed: str
    Thur: str
    Fri: str
    Sat_Sun: str

@dataclass
class Task:
    """Task information"""
    task_name: str
    per_day: TaskPerDay
    total_hours: str
    decimal_hours: float

@dataclass
class TotalsRow:
    """Totals row"""
    label: str
    by_day: Dict[str, str]
    total_hours: str
    total_decimal_hours: float

@dataclass
class PdfExtractionMeta:
    """PDF extraction metadata"""
    base: BaseInfo
    employee: EmployeeInfo
    work_entries: List[WorkEntry]
    weekly_total: WeeklyTotal
    tasks: List[Task]
    totals_row: TotalsRow
    date: str

# JSON format example
META_JSON_EXAMPLE = {
    "base": {
        "po_number": "123456",
        "client": "Goverment",
        "supervisor": "James"
    },
    "employee": {
        "name": "Surui Liu",
        "company": "Employer Pty Ltd"
    },
    "work_entries": [
        {
            "weekday": "Monday",
            "date_original": "11-Aug-25",
            "date_iso": "2025-08-11",
            "morning": { "start": "9:30", "finish": "12:30", "time": "3:00" },
            "afternoon": { "start": "13:30", "finish": "18:00", "time": "4:30" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "7:30",
            "total_daily_decimal": 7.5
        },
        {
            "weekday": "Tuesday",
            "date_original": "12-Aug-25",
            "date_iso": "2025-08-12",
            "morning": { "start": "9:30", "finish": "12:30", "time": "3:00" },
            "afternoon": { "start": "13:30", "finish": "19:00", "time": "5:30" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "8:30",
            "total_daily_decimal": 8.5
        },
        {
            "weekday": "Wednesday",
            "date_original": "13-Aug-25",
            "date_iso": "2025-08-13",
            "morning": { "start": "9:30", "finish": "12:30", "time": "3:00" },
            "afternoon": { "start": "13:30", "finish": "18:00", "time": "4:30" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "7:30",
            "total_daily_decimal": 7.5
        },
        {
            "weekday": "Thursday",
            "date_original": "14-Aug-25",
            "date_iso": "2025-08-14",
            "morning": { "start": "9:30", "finish": "12:30", "time": "3:00" },
            "afternoon": { "start": "13:30", "finish": "20:00", "time": "6:30" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "9:30",
            "total_daily_decimal": 9.5
        },
        {
            "weekday": "Friday",
            "date_original": "15-Aug-25",
            "date_iso": "2025-08-15",
            "morning": { "start": "9:30", "finish": "12:30", "time": "3:00" },
            "afternoon": { "start": "13:30", "finish": "18:00", "time": "4:30" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "7:30",
            "total_daily_decimal": 7.5
        },
        {
            "weekday": "Saturday",
            "date_original": "16-Aug-25",
            "date_iso": "2025-08-16",
            "morning": { "start": "", "finish": "", "time": "0:00" },
            "afternoon": { "start": "", "finish": "", "time": "0:00" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "0:00",
            "total_daily_decimal": 0.0
        },
        {
            "weekday": "Sunday",
            "date_original": "17-Aug-25",
            "date_iso": "2025-08-17",
            "morning": { "start": "", "finish": "", "time": "0:00" },
            "afternoon": { "start": "", "finish": "", "time": "0:00" },
            "extra_in_out": { "morning": "0:00", "afternoon": "0:00" },
            "total_daily_hours": "0:00",
            "total_daily_decimal": 0.0
        }
    ],
    "weekly_total": {
        "total_hours": "40:30",
        "total_decimal_hours": 40.5
    },
    "tasks": [
        {
            "task_name": "Task1",
            "per_day": {
                "Mon": "7:30",
                "Tues": "8:30",
                "Wed": "7:30",
                "Thur": "9:30",
                "Fri": "7:30",
                "Sat/Sun": ""
            },
            "total_hours": "40:30",
            "decimal_hours": 40.5
        }
    ],
    "totals_row": {
        "label": "Total Hours",
        "by_day": {
            "Mon": "7:30",
            "Tues": "8:30",
            "Wed": "7:30",
            "Thur": "9:30",
            "Fri": "7:30",
            "Sat": "0:00",
            "Sun": "0:00"
        },
        "total_hours": "40:30",
        "total_decimal_hours": 40.5
    },
    "date": "8/15/2025"
}
