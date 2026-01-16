from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from services.stock_service import deduct_stock  # we’ll define this
from models.silo import Silo
from models.party import Party
from datetime import datetime
from database import db
from models.truck import Truck
from models.trip import Trip

gate_bp = Blueprint("gates", __name__, url_prefix="/gate")


@gate_bp.route("/gate/in", methods=["GET", "POST"])
def gate_in():
    trucks = Truck.query.all()
    silos = Silo.query.filter_by(active=True).all()
    parties = Party.query.filter_by(active=True).all()

    prefill_truck_id = request.args.get("truck_id")

    if request.method == "POST":
        truck_id = int(request.form["truck_id"])

        # ❌ Block duplicate open trips
        existing = Trip.query.filter_by(truck_id=truck_id, status="OPEN").first()

        if existing:
            return "Truck already inside premises", 400

        trip = Trip(
            truck_id=truck_id,
            trip_type=request.form["trip_type"],
            silo_id=request.form["silo_id"],
            party_id=request.form["party_id"],
            gate_in_time=datetime.now(),
            status="OPEN",
        )

        db.session.add(trip)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template(
        "gate_in.html",
        trucks=trucks,
        silos=silos,
        parties=parties,
        prefill_truck_id=prefill_truck_id,
    )


@gate_bp.route("/gate/out", methods=["GET", "POST"])
def gate_out():
    open_trips = Trip.query.filter_by(status="OPEN").all()

    if request.method == "POST":
        trip_id = int(request.form["trip_id"])
        ash_qty = float(request.form["ash_quantity"])

        trip = Trip.query.get_or_404(trip_id)

        # 🔒 Stock validation (placeholder – enforced later)
        deduct_stock(trip.silo_id, ash_qty)

        trip.ash_quantity = ash_qty
        trip.gate_out_time = datetime.now()
        trip.status = "COMPLETED"

        db.session.commit()

        return redirect(url_for("dashboard.daily_balance_view"))

    return render_template("gate_out.html", open_trips=open_trips)
