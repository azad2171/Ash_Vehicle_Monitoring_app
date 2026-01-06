from flask import Blueprint, render_template, request
from services.metrics_service import get_dashboard_metrics
from models.trip import Trip
from models.truck import Truck
from database import db
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def dashboard_view():
    # Filters from query parameters
    truck_filter = request.args.get("truck_number", "")
    status_filter = request.args.get("status", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    trips_query = Trip.query.join(Truck)

    if truck_filter:
        trips_query = trips_query.filter(Truck.truck_number.contains(truck_filter))

    if status_filter.lower() == "active":
        trips_query = trips_query.filter(Trip.gate_out_time.is_(None))
    elif status_filter.lower() == "completed":
        trips_query = trips_query.filter(Trip.gate_out_time.isnot(None))

    if start_date:
        try:
            dt_start = datetime.fromisoformat(start_date)
            trips_query = trips_query.filter(Trip.gate_in_time >= dt_start)
        except:
            pass

    if end_date:
        try:
            dt_end = datetime.fromisoformat(end_date)
            trips_query = trips_query.filter(Trip.gate_in_time <= dt_end)
        except:
            pass

    trips = trips_query.order_by(Trip.gate_in_time.desc()).all()
    metrics = get_dashboard_metrics()

    return render_template(
        "dashboard.html",
        total_trips=metrics["total_trips"],
        active_trucks_inside=metrics["active_trucks_inside"],
        average_turnaround_minutes=metrics["average_turnaround_minutes"],
        total_ash_transported=metrics["total_ash_transported"],
        trips=trips,
    )
