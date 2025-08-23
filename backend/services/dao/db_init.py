# backend/services/db_init.py
import time
import sqlalchemy
from sqlalchemy import select, func
# from ..models import Base, engine, SessionLocal
# from ..models.timesheet import Timesheet
from models import Base, engine, SessionLocal
from models.timesheet import Timesheet

def init_db_and_seed(max_retries=20, delay=1.5):
    for attempt in range(1, max_retries+1):
        try:
            Base.metadata.create_all(bind=engine)
            with SessionLocal() as session:
                count = session.scalar(select(func.count()).select_from(Timesheet))
                if not count:
                    row = Timesheet(meta_data={"note": "first row seeded on startup"}, status="in-progress")
                    session.add(row)
                    session.commit()
            print("DB init & seed done")
            return
        except sqlalchemy.exc.OperationalError as e:
            print(f"[DB not ready] retry {attempt}/{max_retries} ... {e}")
            time.sleep(delay)
    raise RuntimeError("Database never became ready")