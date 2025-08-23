
from dataclasses import dataclass
from typing import Dict

@dataclass
class TimesheetExtracted:
    week_worked: str
    hours: Dict[str, str]   # {"Mon": "8hrs", ...}
    total_hours: str
    signatures: bool = True
    additional_text: str = "No"
    employee_name: str = ""
    po_number: str = ""

@dataclass
class TimesheetExpected:
    week_worked: str
    hours: Dict[str, str]
    total_hours: str
    employee_name: str
    po_number: str
    require_signature: bool = False
