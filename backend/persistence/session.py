"""Database engine and session factory.

Purpose:
    Provide a single SQLAlchemy `engine`, a session factory `SessionLocal`,
    and the ORM base class `Base` for the application. This module handles
    connection setup only. Schema creation and seed data are handled by
    /db/init_tables.sql (invoked by start.sh).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.config import Config

# Fallback to SQLite only for local testing when DATABASE_URL is not provided.
DATABASE_URL = Config.DATABASE_URL or "sqlite:///easyx.db"

# Global Engine (pool_pre_ping guards against stale connections).
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # Automatic disconnection detection
    future=True
)

# Session factory. Use: `with SessionLocal() as session: ...
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True
)

# ORM mapping base. Do NOT call Base.metadata.create_all() in the app.
Base = declarative_base()
