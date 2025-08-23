# Models package
# backend/models/__init__.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://easyx:easyxpass@postgres:5432/easyxdb"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

# from .timesheet import Timesheet  # in case new model is not in import
# __all__ = ["engine", "SessionLocal", "Base", "Timesheet"]