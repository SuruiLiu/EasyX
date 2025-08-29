"""ORM mapping for the 'timesheet' table.

This mapping mirrors db/init_tables.sql:
    - tid SERIAL PRIMARY KEY
    - meta_data JSONB
    - created_at TIMESTAMPTZ DEFAULT now()
    - status TEXT
"""
from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from persistence.session import Base

class Timesheet(Base):
    """Timesheet ORM model.

    Purpose:
        Map the PostgreSQL `timesheet` table to a Python class so that the app
        can query it via SQLAlchemy ORM.

    Example:
        >>> from sqlalchemy import select
        >>> from persistence.session import SessionLocal
        >>> from models.timesheet_orm import Timesheet
        >>> with SessionLocal() as s:
        ...     row = s.execute(
        ...         select(Timesheet.meta_data).where(Timesheet.tid == 1)
        ...     ).first()
        ...     data = row[0] if row else None  # JSON dict or None

    Returns:
        This class itself does not return values. Using it in a query returns
        rows/columns (e.g., a JSON dict for `meta_data`) or ORM instances.
    """
    __tablename__ = "timesheet"

    # init_tables.sql: tid SERIAL PRIMARY KEY  -> Integer + autoincrement
    tid = Column(Integer, primary_key=True, autoincrement=True)

    # init_tables.sql: meta_data JSONB（not declared NOT NULL）→ nullable=True
    meta_data = Column(JSONB, nullable=True)

    # init_tables.sql: created_at TIMESTAMPTZ DEFAULT now()
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=True)

    # init_tables.sql: status TEXT（not declared default/not null）
    status = Column(String, nullable=True)
