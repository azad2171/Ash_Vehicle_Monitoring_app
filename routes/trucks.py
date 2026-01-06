from flask import Blueprint, request, jsonify
from database import db
from models.truck import Truck
from services.qr_service import generate_qr_code

truck_bp = Blueprint("trucks", __name__, url_prefix="/trucks")


@truck_bp.route("/register", methods=["POST"])
def register_truck():
    data = request.get_json()

    if not data or "truck_number" not in data:
        return {"error": "truck_number is required"}, 400

    truck_number = data["truck_number"]

    existing = Truck.query.filter_by(truck_number=truck_number).first()
    if existing:
        return {"error": "Truck already registered"}, 409

    truck = Truck(truck_number=truck_number)
    db.session.add(truck)
    db.session.commit()

    qr_data = f"TRUCK:{truck.id}"
    qr_path = generate_qr_code(qr_data, f"truck_{truck.id}.png")

    truck.qr_code = qr_path
    db.session.commit()

    return jsonify(
        {"id": truck.id, "truck_number": truck.truck_number, "qr_code": qr_path}
    ), 201
