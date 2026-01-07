from sqlalchemy import func, case
from models.trip import Trip
from database import db


def get_daily_summary(start_date=None, end_date=None):
    query = db.session.query(
        func.date(Trip.gate_in_time).label("date"),
        func.sum(case((Trip.trip_type == "BAGGING", 1), else_=0)).label("bagging_nos"),
        func.sum(case((Trip.trip_type == "BAGGING", Trip.ash_quantity), else_=0)).label(
            "bagging_mt"
        ),
        func.sum(case((Trip.trip_type == "BULKERS", 1), else_=0)).label("bulkers_nos"),
        func.sum(case((Trip.trip_type == "BULKERS", Trip.ash_quantity), else_=0)).label(
            "bulkers_mt"
        ),
        func.sum(case((Trip.trip_type == "RAKE", 1), else_=0)).label("rake_nos"),
        func.sum(case((Trip.trip_type == "RAKE", Trip.ash_quantity), else_=0)).label(
            "rake_mt"
        ),
    ).group_by(func.date(Trip.gate_in_time))

    if start_date:
        query = query.filter(Trip.gate_in_time >= start_date)
    if end_date:
        query = query.filter(Trip.gate_in_time <= end_date)

    results = query.order_by(func.date(Trip.gate_in_time)).all()

    summary = []
    for r in results:
        remark = ""
        if (
            (r.bagging_nos or 0) == 0
            and (r.bulkers_nos or 0) == 0
            and (r.rake_nos or 0) == 0
        ):
            remark = "No demand from consumer"

        summary.append(
            {
                "date": r.date,
                "bagging_nos": r.bagging_nos or 0,
                "bagging_mt": round(r.bagging_mt or 0, 2),
                "bulkers_nos": r.bulkers_nos or 0,
                "bulkers_mt": round(r.bulkers_mt or 0, 2),
                "rake_nos": r.rake_nos or 0,
                "rake_mt": round(r.rake_mt or 0, 2),
                "remarks": remark,
            }
        )

    return summary
