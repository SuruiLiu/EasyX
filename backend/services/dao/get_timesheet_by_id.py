from models import SessionLocal
from models.timesheet import Timesheet

#use SQLAlchemy ORM to query psql
def get_metadata_by_tid(tid):
    with SessionLocal() as session:
        result = (
            session.
            query(Timesheet.meta_data) # SELECT timesheet.meta_data
            .filter(Timesheet.tid == tid) # WHERE timesheet.tid == tid
            .first()
        )
        # `.first()` returns None if no rows
        # if result is not None return its one and only element
        return result[0] if result else None