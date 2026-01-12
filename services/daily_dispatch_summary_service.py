from sqlalchemy import func
from database import db
from models.trip import Trip


def get_dispatch_summary(target_date):
    rows = (
        db.session.query(
            Trip.trip_type,
            func.count(Trip.id).label("nos"),
            func.coalesce(func.sum(Trip.ash_quantity), 0).label("mt"),
        )
        .filter(func.date(Trip.gate_out_time) == target_date)
        .group_by(Trip.trip_type)
        .all()
    )

    summary = {
        "BAGGING": {"nos": 0, "mt": 0},
        "BULKERS": {"nos": 0, "mt": 0},
        "RAKE": {"nos": 0, "mt": 0},
    }

    total_nos = 0
    total_mt = 0

    for r in rows:
        summary[r.trip_type]["nos"] = r.nos
        summary[r.trip_type]["mt"] = round(r.mt, 2)
        total_nos += r.nos
        total_mt += r.mt

    return summary, total_nos, round(total_mt, 2)
