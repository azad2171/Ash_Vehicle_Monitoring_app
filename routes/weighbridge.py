from flask import Blueprint, request, jsonify
from database import db
from models.trip import Trip

weighbridge_bp = Blueprint("weighbridge", __name__, url_prefix="/weighbridge")


@weighbridge_bp.route("/in", methods=["POST"])
def weighbridge_in():
    data = request.get_json()

    if not data or "trip_id" not in data or "empty_weight" not in data:
        return {"error": "trip_id and empty_weight required"}, 400

    trip = Trip.query.get(data["trip_id"])
    if not trip:
        return {"error": "Trip not found"}, 404

    if trip.empty_weight is not None:
        return {"error": "Empty weight already recorded"}, 409

    trip.empty_weight = float(data["empty_weight"])
    db.session.commit()

    return jsonify(
        {
            "message": "Empty weight recorded",
            "trip_id": trip.id,
            "empty_weight": trip.empty_weight,
        }
    )


@weighbridge_bp.route("/out", methods=["POST"])
def weighbridge_out():
    data = request.get_json()

    if not data or "trip_id" not in data or "loaded_weight" not in data:
        return {"error": "trip_id and loaded_weight required"}, 400

    trip = Trip.query.get(data["trip_id"])
    if not trip:
        return {"error": "Trip not found"}, 404

    if trip.empty_weight is None:
        return {"error": "Empty weight not recorded"}, 400

    if trip.loaded_weight is not None:
        return {"error": "Loaded weight already recorded"}, 409

    trip.loaded_weight = float(data["loaded_weight"])
    trip.ash_quantity = round(trip.loaded_weight - trip.empty_weight, 2)

    db.session.commit()

    return jsonify(
        {
            "message": "Loaded weight recorded",
            "trip_id": trip.id,
            "loaded_weight": trip.loaded_weight,
            "ash_quantity": trip.ash_quantity,
        }
    )
