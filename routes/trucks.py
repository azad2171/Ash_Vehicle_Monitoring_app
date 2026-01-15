from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from database import db
from models.truck import Truck
from models.trip import Trip
from services.qr_service import generate_qr_code
from datetime import datetime
import uuid

truck_bp = Blueprint("trucks", __name__, url_prefix="/trucks")


from services.truck_service import create_truck_with_qr


@truck_bp.route("/register", methods=["POST"])
def register_truck_api():
    data = request.get_json()

    if not data or "truck_number" not in data:
        return {"error": "truck_number is required"}, 400

    try:
        truck = create_truck_with_qr(data["truck_number"])
    except ValueError as e:
        return {"error": str(e)}, 409

    return jsonify(
        {
            "id": truck.id,
            "truck_number": truck.truck_number,
            "qr_payload": truck.qr_code,
            "qr_image": truck.qr_image_path,
        }
    ), 201


@truck_bp.route("/trucks/register", methods=["GET", "POST"])
def register_truck_ui():
    if request.method == "POST":
        truck_number = request.form["truck_number"]

        try:
            truck = create_truck_with_qr(truck_number)
        except ValueError as e:
            return str(e), 400

        return redirect(url_for("trucks.view_truck", truck_id=truck.id))

    return render_template("register_truck.html")


@truck_bp.route("/trucks/trip/add", methods=["GET", "POST"])
def add_trip():
    from models.truck import Truck
    from models.silo import Silo
    from models.party import Party
    from datetime import datetime

    trucks = Truck.query.all()
    silos = Silo.query.filter_by(active=True).all()
    parties = Party.query.filter_by(active=True).all()

    prefill_truck_id = request.args.get("truck_id")

    if request.method == "POST":
        trip = Trip(
            truck_id=request.form["truck_id"],
            trip_type=request.form["trip_type"],
            silo_id=request.form["silo_id"],
            party_id=request.form["party_id"],
            ash_quantity=float(request.form["ash_quantity"]),
            gate_in_time=datetime.now(),
            gate_out_time=datetime.now(),
            status="completed",
        )
        db.session.add(trip)
        db.session.commit()

        return redirect(url_for("dashboard.daily_balance_view"))

    return render_template(
        "add_trip.html",
        trucks=trucks,
        silos=silos,
        parties=parties,
        prefill_truck_id=prefill_truck_id,
    )


@truck_bp.route("/trucks/<int:truck_id>")
def view_truck(truck_id):
    truck = Truck.query.get_or_404(truck_id)
    return render_template("view_truck.html", truck=truck)


@truck_bp.route("/trucks", methods=["GET"])
def list_trucks():
    trucks = Truck.query.order_by(Truck.truck_number).all()
    return render_template("list_trucks.html", trucks=trucks)
