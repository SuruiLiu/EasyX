# backend/models/timesheet.py
from dataclasses import dataclass
from typing import Dict
from sqlalchemy import BigInteger, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from . import Base

class Timesheet(Base):
    __tablename__ = "timesheet"

    tid = Column(BigInteger, primary_key=True, autoincrement=True)
    meta_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(32), nullable=False, default="in-progress")

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
