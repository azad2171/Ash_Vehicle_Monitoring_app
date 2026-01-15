from models.truck import Truck
from database import db
from utils.qr import generate_qr_code


def create_truck_with_qr(truck_number: str) -> Truck:
    truck_number = truck_number.strip().upper()

    existing = Truck.query.filter_by(truck_number=truck_number).first()
    if existing:
        raise ValueError("Truck already exists")

    # 1️⃣ Create truck
    truck = Truck(truck_number=truck_number)
    db.session.add(truck)
    db.session.commit()  # get ID

    # 2️⃣ Generate QR
    qr_payload = f"TRUCK:{truck.id}"
    qr_path = generate_qr_code(qr_payload, filename=truck_number.replace(" ", "_"))

    # 3️⃣ Save QR info
    truck.qr_code = qr_payload
    truck.qr_image_path = qr_path
    db.session.commit()

    return truck
