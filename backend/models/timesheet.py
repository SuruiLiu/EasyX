# backend/models/timesheet.py
from sqlalchemy import BigInteger, Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from . import Base

class Timesheet(Base):
    __tablename__ = "timesheet"

    tid = Column(BigInteger, primary_key=True, autoincrement=True)
    meta_data = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    status = Column(String(32), nullable=False, default="in-progress")