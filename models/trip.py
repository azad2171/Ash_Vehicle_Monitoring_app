from datetime import datetime
from database import db


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    truck_id = db.Column(db.Integer, db.ForeignKey("truck.id"), nullable=False)

    trip_type = db.Column(
        db.String(20), nullable=True, default="BULKERS"
    )  # BAGGING/BULKERS/RAKE
    gate_in_time = db.Column(db.DateTime, nullable=False)
    gate_out_time = db.Column(db.DateTime)
    empty_weight = db.Column(db.Float)
    loaded_weight = db.Column(db.Float)
    ash_quantity = db.Column(db.Float)
    turnaround_minutes = db.Column(db.Float)

    # active/completed/no_demand
    status = db.Column(db.String(20), nullable=True)
    remarks = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    truck = db.relationship("Truck", backref="trips")
