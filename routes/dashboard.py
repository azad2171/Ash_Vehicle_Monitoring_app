from flask import Blueprint, render_template, request
from models.trip import Trip
from models.truck import Truck
from services.metrics_service import get_dashboard_metrics
from datetime import datetime
from database import db
from services.daily_summary_service import get_daily_summary
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def dashboard_view():
    truck_filter = request.args.get("truck_number", "")
    status_filter = request.args.get("status", "")
    type_filter = request.args.get("trip_type", "")
    start_date = request.args.get("start_date", "")
    end_date = request.args.get("end_date", "")

    trips_query = Trip.query.join(Truck)

    if truck_filter:
        trips_query = trips_query.filter(Truck.truck_number.contains(truck_filter))
    if status_filter:
        trips_query = trips_query.filter(Trip.status == status_filter)
    if type_filter:
        trips_query = trips_query.filter(Trip.trip_type == type_filter)
    if start_date:
        try:
            trips_query = trips_query.filter(
                Trip.gate_in_time >= datetime.fromisoformat(start_date)
            )
        except:
            pass
    if end_date:
        try:
            trips_query = trips_query.filter(
                Trip.gate_in_time <= datetime.fromisoformat(end_date)
            )
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
        request=request,  # needed for filters
    )


@dashboard_bp.route("/daily-summary", methods=["GET"])
def daily_summary_view():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    summary = get_daily_summary(start_date, end_date)

    return render_template("daily_summary.html", summary=summary, request=request)
