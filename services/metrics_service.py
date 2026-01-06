from sqlalchemy import func
from database import db
from models.trip import Trip


def get_dashboard_metrics():
    total_trips = Trip.query.count()

    active_trips = Trip.query.filter(Trip.gate_out_time.is_(None)).count()

    avg_turnaround = db.session.query(func.avg(Trip.turnaround_minutes)).scalar()

    total_ash = db.session.query(func.sum(Trip.ash_quantity)).scalar()

    return {
        "total_trips": total_trips,
        "active_trucks_inside": active_trips,
        "average_turnaround_minutes": round(avg_turnaround, 2) if avg_turnaround else 0,
        "total_ash_transported": round(total_ash, 2) if total_ash else 0,
    }
