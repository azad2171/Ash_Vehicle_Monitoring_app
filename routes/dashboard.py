from flask import Blueprint, render_template
from services.metrics_service import get_dashboard_metrics

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/", methods=["GET"])
def dashboard_view():
    metrics = get_dashboard_metrics()
    return render_template(
        "dashboard.html",
        total_trips=metrics["total_trips"],
        active_trucks_inside=metrics["active_trucks_inside"],
        average_turnaround_minutes=metrics["average_turnaround_minutes"],
        total_ash_transported=metrics["total_ash_transported"],
    )
