from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db
from models.truck import Truck
from models.trip import Trip

gate_bp = Blueprint("gates", __name__, url_prefix="/gate")


@gate_bp.route("/in", methods=["POST"])
def gate_in():
    data = request.get_json()

    if not data or "qr_data" not in data:
        return {"error": "qr_data is required"}, 400

    qr_data = data["qr_data"]

    # Expected format: TRUCK:<id>
    try:
        truck_id = int(qr_data.split(":")[1])
    except:
        return {"error": "Invalid QR code"}, 400

    truck = Truck.query.get(truck_id)
    if not truck:
        return {"error": "Truck not found"}, 404

    # Prevent multiple open trips
    open_trip = Trip.query.filter_by(
        truck_id=truck.id, gate_out_time=None).first()

    if open_trip:
        return {"error": "Truck already inside plant"}, 409

    trip = Trip(truck_id=truck.id, gate_in_time=datetime.utcnow())

    db.session.add(trip)
    db.session.commit()

    return jsonify(
        {
            "message": "Gate IN recorded",
            "trip_id": trip.id,
            "gate_in_time": trip.gate_in_time.isoformat(),
        }
    ), 201


@gate_bp.route("/out", methods=["POST"])
def gate_out():
    data = request.get_json()

    if not data or "qr_data" not in data:
        return {"error": "qr_data is required"}, 400

    qr_data = data["qr_data"]

    try:
        truck_id = int(qr_data.split(":")[1])
    except:
        return {"error": "Invalid QR code"}, 400

    trip = Trip.query.filter_by(truck_id=truck_id, gate_out_time=None).first()

    if not trip:
        return {"error": "No active trip found"}, 404

    trip.gate_out_time = datetime.utcnow()
    delta = trip.gate_out_time - trip.gate_in_time
    trip.turnaround_minutes = round(delta.total_seconds() / 60, 2)

    db.session.commit()

    return jsonify(
        {
            "message": "Gate OUT recorded",
            "trip_id": trip.id,
            "turnaround_minutes": trip.turnaround_minutes,
        }
    )
